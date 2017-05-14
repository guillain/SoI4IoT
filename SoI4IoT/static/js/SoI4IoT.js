/***
 Target: Ajax functions
 Version: 0.1
 Date: 2017/01/18
 Mail: guillain@gmail.com
 Copyright 2017 GPL - Guillain
***/

/* dashboard function */
  $(function() {
    $('a#dashboardSub').bind('click', function() {
      $.ajax({
        url: "dashboard",
        data: $('form').serialize(),
        type: 'POST',
        success: function(data) {
          console.log(data);
          var buffer="";
          $.each(data, function(index, val){
            if (val.length == 0) {
              $('#dashboardRes').html('<li>No user found</li>');
            } else {
              $('#dashboardRes').html('<li>val</li>');
            }
          });
        },
        error: function(error) {
          console.log(error);
          $("#result").text(error);
        }
      });
    });
  });

/* newSub click */
  $(function() {
    $('a#newSub').bind('click', function() {
        $.ajax({
            url: 'newSub',
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

/* userSub click */
  $(function() {
    $('a#userSub').bind('click', function() {
        $.ajax({
            url: 'userSub',
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
