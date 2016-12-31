var map;

// Markers
var initialMarkers = [
    {
        name : 'Bathtub Gin',
        location : '132 9th Ave, New York, NY 10011',
        lat: 40.743585,
        long: -74.003283,
        description : 'Walk into the Stone Street coffee house and go through the door straight ahead.'
    },
    {
        name : 'Angel&#39;s Share',
        lat: 40.729779,
        long: -73.989161,
        location : '8 Stuyvesant St, New York, NY 10003',
        description : 'Climb the stairs to Japanese restaurant Village Yokocho, and enter through the unmarked wooden door in the back left.'
    },
    {
        name : 'The Blind Barber',
        lat: 40.727147,
        long: -73.980140,
        location : '339 E 10th St, New York, NY 10009',
        description : 'Pass the bouncer with the eye patch then walk through the erie barber shop and through the wooden barn door. Make sure to enjoy a drink in the back library.'
    },
    {
        name : 'Attaboy',
        location : '134 Eldridge St, New York, NY 10002',
        lat: 40.719118,
        long: -73.991360,
        description : 'Knock or ring the buzzer (look for a window marked with M&H Tailors and Alterations) and pray they have space for you.'
    },
    {
        name : 'The Back Room',
        lat: 40.718763,
        long: -73.986993,
        location : '102 Norfolk St, New York, NY 10002',
        description : 'Descend the stairs of the “Lower East Side Toy Company,” wind through the back alley, then head back up some stairs to the entrance.'
    }
]


// ViewModel
var ViewModel = function() {
    var self = this;

    this.markerList = ko.observableArray([]);

    initialMarkers.forEach( function(markerItem) {
        self.markerList.push( new Marker(markerItem) );
    });

    this.openNav = resultListView.openNav();
    this.closeNav = resultListView.closeNav();

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
    this.phoneNumber = ko.observable('');

    this.contentString = ko.computed(function() {
        return '<div><b>' + self.name() + '</b><div>' +
               '<div>' + self.description() + '</div>' +
               '<div>' + self.url() + '</div>' +
               '<div>' + self.phoneNumber() + '</div>'
    })

    this.infowindow = new google.maps.InfoWindow({
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
        self.infowindow.open(map, mapMarker);
        self.mapMarker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(function() {
            self.mapMarker.setAnimation(null);
        }, 2800);
    });

    this.mapMarker.setMap(map);

    // Animates mapMarker when marker clicked from list
    this.animateClick = function(markerListItem) {
        google.maps.event.trigger(self.mapMarker, 'click');
    };

};


var resultListView= {

    openNav: function() {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
    },

    closeNav: function() {
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft= "0";
        document.body.style.backgroundColor = "white";
    }

}

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: {lat: 40.735325, lng: -73.994571}
    });

    ko.applyBindings(new ViewModel());
};

function googleError() {
    alert("Google Maps has failed to load for some reason or another. It is not your fault. Grab a beer.")
};