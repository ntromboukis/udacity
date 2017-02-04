from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Store, Base, CatalogItem, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Tim Target", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# catalog for Tim's Target
store1 = Store(user_id=1, name="Tim's Target", category="clothing", photo="/static/clothing.jpg")

session.add(store1)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name="Down Jacket", description="Built to stand the elements",
                     price="$299", store=store1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Blue Jeans", description="Jeans for every occasion",
                     price="$37.50", store=store1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Socks", description="You'll only ever need this one pair",
                     price="$13.99", store=store1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Rolex Submariner", description="Hand crafted excellence",
                     price="$10,999.99", store=store1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Winter Boots", description="Made to outlast NYC snowstorms",
                     price="$99", store=store1)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(user_id=1, name="Snow gloves", description="Don't leave home without them!",
                     price="$29.99", store=store1)

session.add(catalogItem6)
session.commit()

# catalog for Super Stir Fry
store2 = Store(user_id=1, name="Super Fly Shoes", category="shoes", photo="/static/shoe.jpg")

session.add(store2)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Air Jordans", description="You won't dunk like him, but you'll get street cred",
                     price="$179.99", store=store2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Puma track shoes",
                     description="Run as fast as you want", price="$75", store=store2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Timberland Work boots", description="For the really tough days",
                     price="$95", store=store2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Crocs", description="For when you need to tend your garden",
                     price="$19", store=store2)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Ugg Slippers", description="Curl up by the fire",
                     price="$90", store=store2)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(user_id=1, name="Dress shoes", description="Don't miss a meeting",
                     price="$120", store=store2)

session.add(catalogItem6)
session.commit()


# catalog for Panda Garden
store1 = Store(user_id=1, name="Tim's Sporting Goods", category="sporting", photo="/static/sports.jpg")

session.add(store1)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Wooden Baseball Bat", description="All wood design for that classic feel",
                     price="$28.99", store=store1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Metal Baseball Bat", description="Hit it out of the park",
                     price="$36.99", store=store1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Baseball glove", description="Make that catch",
                     price="$39.95", store=store1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Football", description="Score the touchdown",
                     price="$26.99", store=store1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Hockey Stick", description="Dental plan not included",
                     price="$29.50", store=store1)

session.add(catalogItem5)
session.commit()






User2 = User(name="Jim Jones", email="bigJim@udacity.com",
             picture='http://farmhousestudios.net/images/jim_cartoon1.jpg')
session.add(User1)
session.commit()

# catalog for Tim's Target
store1 = Store(user_id=1, name="Jim's Bullseye", category="clothing", photo="/static/clothing.jpg")

session.add(store1)
session.commit()

catalogItem1 = CatalogItem(user_id=1, name="Down Jacket", description="Built to stand the elements",
                     price="$298", store=store1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Blue Jeans", description="Jeans for every occasion",
                     price="$37.49", store=store1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Socks", description="You'll only ever need this one pair",
                     price="$13.98", store=store1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Rolex Submariner", description="Hand crafted excellence",
                     price="$10,999.98", store=store1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Winter Boots", description="Made to outlast NYC snowstorms",
                     price="$98", store=store1)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(user_id=1, name="Snow gloves", description="Don't leave home without them!",
                     price="$29.98", store=store1)

session.add(catalogItem6)
session.commit()

# catalog for Super Stir Fry
store2 = Store(user_id=1, name="Jim's Super Shoes", category="shoes", photo="/static/shoe.jpg")

session.add(store2)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Air Jordans", description="You won't dunk like him, but you'll get street cred",
                     price="$179.98", store=store2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Puma track shoes",
                     description="Run as fast as you want", price="$74", store=store2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Timberland Work boots", description="For the really tough days",
                     price="$94", store=store2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Crocs", description="For when you need to tend your garden",
                     price="$18", store=store2)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Ugg Slippers", description="Curl up by the fire",
                     price="$89", store=store2)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(user_id=1, name="Dress shoes", description="Don't miss a meeting",
                     price="$119", store=store2)

session.add(catalogItem6)
session.commit()


# catalog for Panda Garden
store1 = Store(user_id=1, name="Jim's Sporting Goods", category="sporting", photo="/static/sports.jpg")

session.add(store1)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Wooden Baseball Bat", description="All wood design for that classic feel",
                     price="$28.98", store=store1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Metal Baseball Bat", description="Hit it out of the park",
                     price="$36.98", store=store1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Baseball glove", description="Make that catch",
                     price="$39.94", store=store1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Football", description="Score the touchdown",
                     price="$26.98", store=store1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(user_id=1, name="Hockey Stick", description="Dental plan not included",
                     price="$29.49", store=store1)

session.add(catalogItem5)
session.commit()

print "added catalog items!"
