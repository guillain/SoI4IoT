/***
 Target: Ajax functions
 Version: 0.1
 Date: 2017/01/18
 Mail: guillain@gmail.com
 Copyright 2017 GPL - Guillain
***/

/* USER */
/* newUserSub click */
  $(function() {
    $('a#newUserSub').bind('click', function() {
        $.ajax({
            url: 'newUserSub',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* updateUser click */
  $(function() {
    $('a#updateUser').bind('click', function() {
        $.ajax({
            url: 'updateUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* DEVICE */
/* newDeviceSub click */
  $(function() {
    $('a#newDeviceSub').bind('click', function() {
        $.ajax({
            url: 'newDeviceSub',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* updateDevice click */
  $(function() {
    $('a#updateDevice').bind('click', function() {
        $.ajax({
            url: 'updateDevice',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* TRACKING */
/* newTrackingSub click */
  $(function() {
    $('a#newTrackingSub').bind('click', function() {
        $.ajax({
            url: 'newTrackingSub',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* updateTracking click */
  $(function() {
    $('a#updateTracking').bind('click', function() {
        $.ajax({
            url: 'updateTracking',
            data: $('form').serialize(),
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });
    });
  });

/* ADD FEATURES */
/* display additionnal info when onmouse */
function onmouseoveragent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'block';

    hint.style.top = Math.max(el.offsetTop - hint.offsetHeight,0) + "px";
    hint.style.left = el.offsetLeft + "px";
};
function onmouseoutagent(el) {
    var hint = el.querySelector("div.hideme");
    hint.style.display = 'none';
};

/* Body load function */
function bodyOnload(){
}

/* Get GPS position */
function sendHTMLgps(){
    var x = document.getElementById("gps");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(recPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}
function recPosition(position) {
    var x = document.getElementById("gps");
    var longitude = position.coords.longitude;
    var latitude = position.coords.latitude;
    var loginurl = document.getElementById("login") + '';
    var sURLVariables = loginurl.split('=');
    var login = sURLVariables[1];
    alert("Position has been recorded for the user " + login + "\n* Lat.: " + latitude + "\n* Long.: " + longitude);

    $.ajax({
            url: 'recGPS',
            data: { 'login':login, 'latitude':latitude, 'longitude':longitude},
            type: 'POST',
            success: function(data) {
                $("#result").text(data);
            },
            error: function(error) {
                $("#result").text(error);
            }
        });

}


