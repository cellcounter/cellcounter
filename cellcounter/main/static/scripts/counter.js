
    //$counters = new Array();
    $counters = {};
    //$box = new Array();
    $abnormal = false;
    $undo = false;
    $keyboard_active = false;

    $(document).ready(function() {
      $('.count').each(
          function(){
              //access to element via $(this)
              $key = $(this).find('div#key').text();
		$name = $(this).find('font2').text();
              $img = $(this).find('a#img').text();
              $counters[$name] = {};
              $counters[$name]["key"] = $key.toUpperCase();
              $counters[$name]["count"] = 0;
              $counters[$name]["abnormal"] = 0;
              $counters[$name]["box"] = $(this);
              $counters[$name]["img"] = $img;

              //$count[$key] = 0;
              //$count[$key + "_abnormal"] = 0;
              //$box[$key] = $(this);
              //$box[$key + "_abnormal"] = $(this);
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
  $output = {}
  for (var prop in $counters) {
    if ($counters.hasOwnProperty(prop)) { 
      // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
      $output[prop] = {}
      $output[prop]["normal"] = $counters[prop]["count"];
      $output[prop]["abnormal"] = $counters[prop]["abnormal"];
    }
  }

  $results = $.toJSON($output);
  $("#results").text($results);
});

    //$(document).keypress(function(e) {
    jQuery(document).bind('keydown', function (e){
      if($keyboard_active) {
      $key = String.fromCharCode(e.which).toUpperCase();
      $code = e.which;
      $shift_pressed = e.shiftKey;
      //alert($key);

      if($key == " ") {
        $abnormal = true;
        $("div#imagebox").css("background-image", "");
      }
      else if($code == 8) {
        $undo = true;
      }
      else {
        for (var prop in $counters) {
          if($counters[prop]["key"] == $key) {
            if($shift_pressed) {
              //$($counters[prop]["box"]).find("span#abnormal").text($counters[prop]["img"]);
              $("div#imagebox").css("display", "absolute");
              $("div#imagebox").css("background-image", "url(" + $counters[prop]["img"] + ")");
            }
            else if($abnormal) {
              if($undo) {
                if($counters[prop]["abnormal"] > 0)
                  $counters[prop]["abnormal"]--;
              }
              else
                $counters[prop]["abnormal"]++;
              $($counters[prop]["box"]).find("span#abnormal").text($counters[prop]["abnormal"]);
            }
            else {
              if($undo) {
                if($counters[prop]["count"] > 0)
                  $counters[prop]["count"]--;
              }
              else
                $counters[prop]["count"]++;
              $($counters[prop]["box"]).find("span#countval").text($counters[prop]["count"]);
            }
          }
        }
        //$abnormal = false;
      }
      }
    });

    jQuery(document).bind('keyup', function (e){
      if($keyboard_active) {
        $code = e.which;
        $key = String.fromCharCode($code).toUpperCase();
        if($key == " ")
          $abnormal = false;
        if($code == 8)
          $undo = false;
      }
    });

    });
