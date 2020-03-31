function togglesideBar() {
    document.getElementById('sidebar').classList.toggle("active");
}

function initGoogle() {
    gapi.load('auth2', function() {
        gapi.auth2.init().currentUser.listen(userchange);
    });
}

var auth_token;

function userchange(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    auth_token = googleUser.getAuthResponse().id_token; //THIS IS BACKEND VERIFICATION TOKEN
    console.log('backend: ' + auth_token);

    /* 
        TODO: Create a better method to set auth_token on event page
    */

    if ($('#authTokenComment').length) {
        $('#authTokenComment').val(auth_token);
    }

    document.getElementById("profilename").innerText = profile.getName();
}

// on document load

$( document ).ready(function() {
    $("#searchbar").on('keyup', function (e) {
        if (e.keyCode === 13) {
            window.location.href='?search='+$("#searchbar").val();
        }
    });
});

////maps stuff

var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 55.872490, lng: -4.289494},
      zoom: 17,
      streetViewControl: false,
      disableDefaultUI: true,
      styles: [
                {
                    featureType: "poi.business",
                    stylers: [{visibility: "off"}]
                },
                {
                    featureType: "poi.park",
                    elementType: "labels.text",
                    stylers: [{visibility: "off"}]
                }
            ],
    });
    continueMap();
}