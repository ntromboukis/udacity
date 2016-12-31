var map;

// Markers
var initialMarkers = [
    {
        name : 'Bathtub Gin',
        location : '132 9th Ave, New York, NY 10011',
        lat: 40.743585,
        long: -74.003283,
        description :
        'Walk into the Stone Street coffee  <br> ' +
        'house and go through the door <br> ' +
        ' straight ahead.'
    },
    {
        name : "Angel's Share",
        lat: 40.729779,
        long: -73.989161,
        location : '8 Stuyvesant St, New York, NY 10003',
        description :
        'Climb the stairs to Japanese restaurant <br> ' +
        'Village Yokocho, and enter through the  <br> ' +
        'unmarked wooden door in the back left.'
    },
    {
        name : 'The Blind Barber',
        lat: 40.727147,
        long: -73.980140,
        location : '339 E 10th St, New York, NY 10009',
        description :
        'Pass the bouncer with the eye patch then  <br> ' +
        'walk through the erie barber shop and through  <br> ' +
        'the wooden barn door. Make sure to enjoy a  <br> ' +
        'drink in the back library.'
    },
    {
        name : 'Attaboy',
        location : '134 Eldridge St, New York, NY 10002',
        lat: 40.719118,
        long: -73.991360,
        description :
        'Knock or ring the buzzer (look for a window  <br> ' +
        'marked with M&H Tailors and Alterations) and  <br> ' +
        'pray they have space for you.'
    },
    {
        name : 'The Back Room',
        lat: 40.718763,
        long: -73.986993,
        location : '102 Norfolk St, New York, NY 10002',
        description :
        'Descend the stairs of the “Lower East Side Toy Company,” <br> ' +
        'wind through the back alley, then head back up some <br> ' +
        'stairs to the entrance.'
    }
]


// ViewModel
var ViewModel = function() {
    var self = this;

    this.markerList = ko.observableArray([]);

    initialMarkers.forEach( function(markerItem) {
        self.markerList.push( new Marker(markerItem) );
    });


    this.openNav = function() {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
    };

    this.closeNav = function() {
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft= "0";
        document.body.style.backgroundColor = "white";
    };

    this.navState = ko.observable(true);
    this.navBtn = ko.observable('&#8801;');

    this.toggleNav = ko.pureComputed({
        read: function () {
            return self.navBtn();
        },
        write: function () {
            if (self.navState() === true) {
                self.navBtn('&times;');
                self.openNav();
                self.navState(false);
                return self.navBtn;
            } else {
                self.navBtn('&#8801;');
                self.closeNav();
                self.navState(true);
                return self.navBtn;
            }
        },
        owner: self
    });

    this.query = ko.observable('');

    this.filteredList = ko.computed(function() {
        var filter = self.query().toLowerCase();
        if (filter == null) {
            return self.markerList();
        } else {
            return ko.utils.arrayFilter(self.markerList(), function(e) {
                if(e.name().toLowerCase().indexOf(filter) >= 0) {
                    e.selected(true);
                    e.mapMarker.setVisible(true);
                    return true;
                } else {
                    e.selected(false);
                    e.mapMarker.setVisible(false);
                    return false;
                }
            })
        }
    }, self);

};


// Model
var Marker = function(markerItem) {
    var self = this;

    this.name = ko.observable(markerItem.name);
    this.location = ko.observable(markerItem.location);
    this.lat = ko.observable(markerItem.lat);
    this.long = ko.observable(markerItem.long);
    this.description = ko.observable(markerItem.description);
    this.url = ko.observable('');
    this.hereNow = ko.observable('');
    this.phoneNumber = ko.observable('');
    this.selected = ko.observable(true);

    var clientID = '2JDYUEZROUCLCQUILMDN52ZPKF4CXAKF2SMWZ2YNOMZXXBJT';
    var clientSecret = 'L1RIAHQSCAQ20R31O1RXMIZP4ZGAREDHZ33VPLFJ3IPLLCCV';

    var foursquareURL = 'https://api.foursquare.com/v2/venues/search?ll='+ self.lat() +
    ',' + self.long() + '&client_id=' + clientID + '&client_secret=' + clientSecret +
    '&v=20160118' + '&query=' + self.name();

    $.getJSON(foursquareURL, function(data) {
        var result = data.response.venues[0];

        self.hereNow(result.hereNow.summary);
        self.phoneNumber(result.contact.formattedPhone);
    }).fail(function (){
        alert("Danger, Will Robinson! Danger!");
    });

    this.contentString = ko.computed(function() {
        return '<a href="' + self.url() + '" target="_blank">'+ self.name() +'</a>' +
               '<div>' + self.hereNow() + '</div>'+
               '<div>' + self.phoneNumber() + '</div><br>'+
               '<div><b>How to get in:</b><div>' +
               '<div>' + self.description() + '</div>'
    })

    this.infoWindow = new google.maps.InfoWindow({
        content: self.contentString()
    });

    this.mapMarker = new google.maps.Marker({
        position: {
        lat: self.lat(),
        lng: self.long()
        },
        animation: google.maps.Animation.DROP,
        map: map,
        title: self.name()
    });

    this.mapMarker.addListener('click', function() {
        self.infoWindow.setContent(self.contentString());
        self.infoWindow.open(map, self.mapMarker);
        self.mapMarker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(function() {
            self.mapMarker.setAnimation(null);
        }, 700);
    });

    this.mapMarker.setMap(map);

    // Animates mapMarker when marker clicked from list
    this.animateClick = function(markerListItem) {
        google.maps.event.trigger(self.mapMarker, 'click');
    };

};


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: {lat: 40.734065, lng: -73.993326}
    });

    ko.applyBindings(new ViewModel());
};

function googleError() {
    alert("Google Maps has failed to load for some reason or another.")
};