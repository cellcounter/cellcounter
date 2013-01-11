
/* Counter JavaScript.
 *
 * Contains code to record the counts on key strokes.
 *
 */

$counters = {};
$abnormal = false;
$undo = false;
$keyboard_active = false;
$img_displayed = false;

$(document).ready(function() {
  // for each .count element defined in the html, add an associated counter
  $('.count').each(
    function(){
      //access to element via $(this)
      $key = $(this).find('div#key').text();
      $name = $(this).find('#name').text();
      $img = $(this).find('a#img').text();
      
      $counters[$name] = {};
      $counters[$name]["key"] = $key.toUpperCase();
      $counters[$name]["count"] = 0;
      $counters[$name]["abnormal"] = 0;
      $counters[$name]["box"] = $(this);
      $counters[$name]["img"] = $img;
      $counters[$name]["allowed"] = true;
    }
  );
  
  // open the keyboard when the #openkeyboard element is clicked
  $('#openkeyboard').click(function() {
    $('#fuzz').fadeIn('slow', function() {
      $('#counterbox').slideDown('slow', function() {
        // Animation complete.
        $("#fuzz").css("height", $(document).height());
        $keyboard_active = true;
      });
    });
  });
  
  // close the keyboard when the #fuzz (background) element is clicked
  $('#fuzz').click(function() {
    if($keyboard_active) {
      $keyboard_active = false;

      //generate statistics for instant display
      $output = {};
      $total = 0;
      for (var prop in $counters) {
        if ($counters.hasOwnProperty(prop)) { 
          // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
          $output[prop] = {}
          $output[prop]["normal"] = $counters[prop]["count"];
          $output[prop]["abnormal"] = $counters[prop]["abnormal"];

          $total += $counters[prop]["count"];
          $total += $counters[prop]["abnormal"];
        }
      }
      $results = $.toJSON($output);

      $percent = {};
      $per = "";
      for (var prop in $counters) {
        if ($counters.hasOwnProperty(prop)) { 
          // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
          $percent[prop] = ($counters[prop]["count"] + $counters[prop]["abnormal"]) / $total * 100;
          $per += '<tr><td style="width: 20%">' + prop + '</td><td style="width: 20%">' + parseFloat($percent[prop]).toFixed(2) + "%</td></tr>";
        }
      }

      if($total > 0) {
        $('div#statistics').empty().append('<h3>Count statistics</h3><table id="statistics">' + $per + '</table>');
      }

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
  });

  /*$('#submit').click(function() {
    $results = $.toJSON($output);
    $("#results").text($results);
  });*/

  $(document).keydown( function (e){
    if($keyboard_active) {
      // decode the key that was pressed
      $code = e.which;
      $key = String.fromCharCode($code).toUpperCase();

      console.log("key down");
      $shift_pressed = e.shiftKey;
      if($code == 188) $key = ","; // XXX: WTF
      if($code == 173) $key = "-"; // XXX: WTF

      if($key == " ") {
        $abnormal = true;
        return false; // stop key propogation (space is page-down)
      }
      else if($code == 8) {
        $undo = true;
        //alert("quitting");
        return false; // stop key propogation (delete is history back)
      }
      else {
        console.log("key pressed");
        if($shift_pressed) { // display cell type images
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
          // if an image is already being displayed, cancel that but don't record a count
          if($img_displayed) {
            $("div#imagebox").css("display", "none");
            $img_displayed = false;
            return;
          }
          
          // record the count in the appropriate counter, if one exists for the pressed key
          $count_total = 0;
          $abnormal_total = 0;
          for (var prop in $counters) {
            if($counters[prop]["key"] == $key) {
              if($counters[prop]["allowed"]) {
                $counters[prop]["allowed"] = false;
                if($abnormal) {
                  //alert(prop);
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
      console.log($key);
      console.log(String.fromCharCode($code));
      if($code == 173) $key = "-"; // XXX: WTF
      if($code == 188) $key = ","; // XXX: WTF
      
      if($key == " ")
        $abnormal = false;
      if($code == 8)
        $undo = false;
        
      // allow the key to be pressed again (repeat blocking code)
      for (var prop in $counters) {
        if($counters[prop]["key"] == $key) {
          $counters[prop]["allowed"] = true;
        }
      }

    }
  });

});

