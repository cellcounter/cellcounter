
    //$counters = new Array();
    $counters = {};
    //$box = new Array();
    $abnormal = false;
    $undo = false;
    $keyboard_active = false;
    $img_displayed = false;

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
      $("#fuzz").css("height", $(document).height());
      $keyboard_active = true;
    });
  });
});

  $('#fuzz').click(function() {
     if($keyboard_active) {
       $keyboard_active = false;

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
       $("input#counter").attr("value", $results);

       $('#counterbox').slideUp('slow', function() {
         $('#fuzz').fadeOut('slow', function() {
         });
       });
     }
  });

//Adjust height of overlay to fill screen when browser gets resized
$(window).bind("resize", function(){
   $("#fuzz").css("height", $(document).height());
   //$("#fuzz").css("top", $(window).top());
});
   //$("#fuzz").css("height", $(document).height());

$('#submit').click(function() {
  $results = $.toJSON($output);
  $("#results").text($results);
});

    //$(document).keypress(function(e) {
    jQuery(document).bind('keydown', function (e){
        //Event.stop(e);
      if($keyboard_active) {
      $key = String.fromCharCode(e.which).toUpperCase();
      $code = e.which;
      $shift_pressed = e.shiftKey;
      if($code == 188) $key = ","; // XXX: WTF
      if($code == 173) $key = "-"; // XXX: WTF

      if($key == " ") {
        $abnormal = true;
        //Event.stop(e);
        return false;
        //$("div#imagebox").css("background-image", "");
      }
      else if($code == 8) {
        $undo = true;
        return false;
      }
      else {
        if($shift_pressed) {
          for (var prop in $counters) {
            if($counters[prop]["key"] == $key) {
              $el = $("div#imagebox");
              $el.css("display", "block");
              $el.find("div#imgdisplay").css("background-image", "url(" + $counters[prop]["img"] + ")");
              $img_displayed = true;
            }
          }
        }
        else {
          if($img_displayed) {
              $("div#imagebox").css("display", "none");
              $img_displayed = false;
              return;
          }
          $count_total = 0;
          $abnormal_total = 0;
          for (var prop in $counters) {
          if($counters[prop]["key"] == $key) {
            if($abnormal) {
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
          $count_total += $counters[prop]["abnormal"];
          $count_total += $counters[prop]["count"];

          }
        $("#total").text($count_total);

        }
      }
      }
    });

    jQuery(document).bind('keyup', function (e){
      if($keyboard_active) {
        $code = e.which;
        $key = String.fromCharCode($code).toUpperCase();
        if($code == 173) $key = "-"; // XXX: WTF

        if($key == " ")
          $abnormal = false;
        if($code == 8)
          $undo = false;
      }
    });

    });

/*window.onkeydown=function(e){
if(e.keyCode==32){
return false;
}
}; */