
    $(document).keypress(function(e) {
      if($keyboard_active) {
      $key = String.fromCharCode(e.which);

      if($key == " ") {
        $abnormal = true;
      }
      else {
        try {
          if($abnormal) {
            $key = $key + "_abnormal";
          }
          $count[$key]++;
          if($abnormal)
            $($box[$key]).find("span#abnormal").text($count[$key]);
          else
            $($box[$key]).find("span#countval").text($count[$key]);
        }
        catch(err) {
        }
        $abnormal = false;
      }
      }
    });

    $count = new Array();
    $box = new Array();
    $abnormal = false;
    $keyboard_active = false;

    $(document).ready(function() {
      $('.box1').each(
          function(){
              //access to element via $(this)
              $key = $(this).find('div#key').text();
              $count[$key] = 0;
              $count[$key + "_abnormal"] = 0;
              $box[$key] = $(this);
              $box[$key + "_abnormal"] = $(this);
          }
      );

$('#openkeyboard').click(function() {
  $('#fuzz').fadeIn('slow', function() {
    $('#counterbox').slideDown('slow', function() {
      // Animation complete.
      $keyboard_active = true;
    });
  });
});

  $('#fuzz').click(function() {
     if($keyboard_active) {
       $keyboard_active = false;
       $('#counterbox').slideUp('slow', function() {
         $('#fuzz').fadeOut('slow', function() {
         });
       });
     }
  });

//Adjust height of overlay to fill screen when browser gets resized
$(window).bind("resize", function(){
   $("#fuzz").css("height", $(window).height());
});

$('#submit').click(function() {
  $results = "output";
  for (var prop in $count) {
    if ($count.hasOwnProperty(prop)) { 
      // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
      $results = $results + prop + " -- " + $count[prop] + " ";
    }
  }
  $("#results").text($results);
});


    });
