from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Store, CatalogItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2, random, string, json, requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    stores = session.query(Store).order_by(asc(Store.name))
    # return "The current session state is %s" % login_session['state']
    return render_template('stores.html', STATE=state, stores=stores)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        print "in 1st if"
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        print response
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    print request.data
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        print "in 1st try"
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
      print 'Access Token is None'
      response = make_response(json.dumps('Current user not connected.'), 401)
      response.headers['Content-Type'] = 'application/json'
      return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



# I couldn't get facebook to work. Not a huge deal but this is why this is
# commented out


# @app.route('/fbconnect', methods='POST')
# def fbconnect():
#     if request.args.get('state') != login_session['state']:
#         response = make_response(json.dumps('Invalid state parameter.'), 401)
#         return response
#     access_token = request.data

#     app_id = json.loads(open('fb_client_secrents.json', 'r').read())['web']['app_id']
#     app_secret = json.loads(open('fb_client_secrents.json', 'r').read())['web']['app_secret']
#     url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
#     h=httplib2.Http()
#     result = h.request(url, 'GET')[1]

#     userinfo_url = "https://graph.facebook.com/v2.2/me"
#     token = result.split("&")[0]

#     url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
#     h=httplib2.Http()
#     result = h.request(url, 'GET')[1]

#     data = json.loads(result)

#     user_id = getUserId(login_session['email'])
#     if not user_id:
#         user_id = createUser(login_session)
#     login_session['user_id'] = user_id
#     login_session['picture'] = data["data"]["url"]
#     login_session['provider'] = 'facebook'

#     output = ''
#     output += '<h1>Welcome, '
#     output += login_session['username']
#     output += '!</h1>'
#     output += '<img src="'
#     output += login_session['picture']
#     output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
#     flash("you are now logged in as %s" % login_session['username'])
#     print "done!"
#     return output

# @app.route('/fbdisconnect')
# def fbdisconnect():
#     facebook_id - login_session['facebook_id']
#     url = 'https://graph.facebook.com/%s/permissions' % facebook_id
#     h = httplib2.Http()
#     result = h.request(url, 'DELETE')[1]
#     return "you've been logged out"

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['user_id']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showStores'))
    else:
        flash("You were never loggin in!")
        return redirect(url_for('showStores'))

# JSON APIs to view store Information
@app.route('/store/<int:store_id>/catalog/JSON')
def storeCatalogJSON(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    items = session.query(CatalogItem).filter_by(
        store_id=store_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/store/<int:store_id>/catalog/<int:catalog_id>/JSON')
def catalogItemJSON(store_id, catalog_id):
    Catalog_Item = session.query(CatalogItem).filter_by(id=catalog_id).one()
    return jsonify(Catalog_Item=Calatog_Item.serialize)


@app.route('/store/JSON')
def storesJSON():
    stores = session.query(Store).all()
    return jsonify(stores=[r.serialize for r in stores])


# Show all stores
@app.route('/')
@app.route('/store/')
def showStores():
    stores = session.query(Store).order_by(asc(Store.name))
    if 'username' not in login_session:
        return render_template('stores.html', stores = stores)
    else:
        return render_template('stores.html', stores=stores)


# Create a new store
@app.route('/store/new/', methods=['GET', 'POST'])
def newStore():
    if 'username' not in login_session:
        return redirect('/')
    if request.method == 'POST':
        formPhoto = request.form['photo']
        if formPhoto == "/static/shoe.jpg":
            formCategory = 'shoes'
        if formPhoto == "/static/sports.jpg":
            formCategory = 'sporting'
        if formPhoto == "/static/clothing.jpg":
            formCategory = 'clothing'
        newStore = Store(name=request.form['name'], user_id=login_session['user_id'], photo=formPhoto, category=formCategory)
        session.add(newStore)
        flash('New %s Store %s Successfully Created' % (newStore.category, newStore.name))
        session.commit()
        return redirect(url_for('showStores'))
    else:
        return render_template('newStore.html')


# Edit a store
@app.route('/store/<int:store_id>/edit/', methods=['GET', 'POST'])
def editStore(store_id):
    if 'username' not in login_session:
        return redirect('/')
    editedStore = session.query(
        Store).filter_by(id=store_id).one()
    creator = getUserInfo(editedStore.user_id)
    if creator.id != login_session['user_id']:
        flash("Sorry you are not the creator of %s" % editedStore.name)
        return render_template('publicStores.html')
    else:
        if request.method == 'POST':
            if request.form['name']:
                editedStore.name = request.form['name']
                flash('Store Successfully Edited %s' % editedStore.name)
                return redirect(url_for('showStores'))
        else:
            return render_template('editStore.html', store=editedStore)


# Delete a store
@app.route('/store/<int:store_id>/delete/', methods=['GET', 'POST'])
def deleteStore(store_id):
    if 'username' not in login_session:
        return redirect('/')
    storeToDelete = session.query(
        Store).filter_by(id=store_id).one()
    itemsToDelete = session.query(
        CatalogItem).filter_by(store_id=store_id).all()
    if storeToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this store. Please create your own store in order to delete.');}</script><body onload='myFinction()''>"
    if request.method == 'POST':
        session.delete(storeToDelete)
        for i in itemsToDelete:
            session.delete(i)
            flash('%s Successfully Deleted' % i.name)
        flash('%s Successfully Deleted' % storeToDelete.name)
        session.commit()
        return redirect(url_for('showStores', store_id=store_id))
    else:
        return render_template('deleteStore.html', store=storeToDelete)


# Show a store catalog
@app.route('/store/<int:store_id>/')
@app.route('/store/<int:store_id>/catalog/')
def showCatalog(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    creator = getUserInfo(store.user_id)
    items = session.query(CatalogItem).filter_by(
        store_id=store_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicCatalog.html', items = items, store = store, creator = creator)
    else:
        return render_template('catalog.html', items=items, store=store, creator = creator)


# Create a new catalog item
@app.route('/store/<int:store_id>/catalog/new/', methods=['GET', 'POST'])
def newCatalogItem(store_id):
    if 'username' not in login_session:
        return redirect('/')
    store = session.query(Store).filter_by(id=store_id).one()
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], store_id=store_id, user_id=store.user_id)
        session.add(newItem)
        session.commit()
        flash('New catalog %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showCatalog', store_id=store_id))
    else:
        return render_template('newCatalogItem.html', store_id=store_id)


# Edit a catalog item
@app.route('/store/<int:store_id>/catalog/<int:catalog_id>/edit', methods=['GET', 'POST'])
def editCatalogItem(store_id, catalog_id):
    if 'username' not in login_session:
        return redirect('/')
    editedItem = session.query(CatalogItem).filter_by(id=catalog_id).one()
    store = session.query(Store).filter_by(id=store_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Store Item Successfully Edited')
        return redirect(url_for('showCatalog', store_id=store_id))
    else:
        return render_template('editCatalogItem.html', store_id=store_id, catalog_id=catalog_id, item=editedItem)


# Delete a catalog item
@app.route('/store/<int:store_id>/catalog/<int:catalog_id>/delete', methods=['GET', 'POST'])
def deleteCatalogItem(store_id, catalog_id):
    if 'username' not in login_session:
        return redirect('/')
    store = session.query(Store).filter_by(id=store_id).one()
    itemToDelete = session.query(CatalogItem).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('catalog Item Successfully Deleted')
        return redirect(url_for('showCatalog', store_id=store_id))
    else:
        return render_template('deleteCatalogItem.html', item=itemToDelete)

@app.route('/store/<string:store_category>/', methods=['GET'])
def categorizedStore(store_category):
    stores = session.query(Store).filter_by(category=store_category).all()
    if store_category == 'sporting':
        return render_template('stores.html', stores=stores)
    if store_category == 'shoes':
        return render_template('stores.html', stores=stores)
    if store_category == 'clothing':
        return render_template('stores.html', stores=stores)


def getUserId(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user


def createUser(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
