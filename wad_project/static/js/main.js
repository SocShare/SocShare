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

    document.getElementById("profilename").innerText = profile.getName();
}



$( document ).ready(function() {
    $("#searchbar").on('keyup', function (e) {
        if (e.keyCode === 13) {
            window.location.href='?search='+$("#searchbar").val();
        }
    });
});
