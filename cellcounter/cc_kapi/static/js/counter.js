/*global $:false, jQuery:false */
//counters = new Array();
//$box = new Array();
var counters = {};
var abnormal = false;
var undo = false;
var keyboard_active = false;
var img_displayed = false;
var doughnut = {};
var pie = {};
var arc = {};
var cell_types = [];
var size = 200;
var editing_keyboard = false;
var edit_cell_id = -1;
var selected_element = {};
var date_now = new Date(Date.now()).toISOString()
var keyboard_map = {"label": "Default", "is_primary": true, "created": date_now,
                    "last_modified": date_now, "mappings": new Array()};

$(document).ready(function() {
    "use strict";
    var key, name, img, count_total;
    $("#myCounts").tablesorter();
    
    $.getJSON("/api/cell_types/", function(data) {
        cell_types = data;
        //console.log(cell_types);
        //for(var i=0; i<cell_types.length; i++) {
        for(var x in cell_types) {
            cell_types[x].count = 0;
            cell_types[x].abnormal = 0;
            cell_types[x].box = [];
        }

        load_keyboard();
    
    });

    $('#edit_button').on('click', edit_keyboard);
    $('#reset_button').on('click', function() {
        $( "#dialog-confirm" ).dialog({
            resizable: false,
            modal: true,
            buttons: {
            "Reset all counters": function() {
                reset_counters();
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
            }
        });
    });

    $('#openkeyboard').click(function () {
        $('#fuzz').fadeIn('slow', function () {
            resize_keyboard($("div#content").width());
            $('#counterbox').slideDown('slow', function () {
                $("#fuzz").css("height", $(document).height());
                keyboard_active = true;
            });
        });
        count_total = 0;
        for (var prop in counters) {
            if (counters.hasOwnProperty(prop))  {
                count_total += counters[prop].abnormal;
                count_total += counters[prop].count;
            }
        }
        $("#total").text(count_total);
        $('div#statistics').empty();
        $("#visualise2").css("display", "none");
        $("#savefilebutton").css("display", "none");
        init_visualisation("#doughnut");
        update_visualisation();
    });

    $('#fuzz, #close_button').click(function () {
        var total, percent, per;

        if(editing_keyboard)
            return;
        
        if (keyboard_active) {
            keyboard_active = false;
            total = 0;

            // Put counts into the ModelForms, increment total
            for (var cell in cell_types) {
                if (cell_types.hasOwnProperty(cell)) {
                    $("#id_"+cell+"-normal_count").prop("value", cell_types[cell].count);
                    $("#id_"+cell+"-abnormal_count").prop("value", cell_types[cell].abnormal);
                    total += cell_types[cell].count;
                    total += cell_types[cell].abnormal;
                }
            }
       
            var percent = {};
            var abnormal = {};
            var per = "";
       
            for (var cell in cell_types) {
                if (cell_types.hasOwnProperty(cell)) { 
                    // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
                    percent[cell] = (cell_types[cell].count + cell_types[cell].abnormal) / total * 100;
                    if(cell_types[cell].count + cell_types[cell].abnormal != 0) {
                        abnormal[cell] = cell_types[cell].abnormal / (cell_types[cell].count + cell_types[cell].abnormal) * 100;
                        abnormal[cell] = parseFloat(abnormal[cell]).toFixed(0) + "%";
                    }
                    else
                        abnormal[cell] = "N/A";
                    per += '<tr><td class="celltypes">' + cell_types[cell].name + '</td><td class="ignore" style="width: 20px; background-color:'+ cell_types[cell].colour +'"></td><td>'+cell_types[cell].count+'</td><td>'+cell_types[cell].abnormal+'</td><td>' + parseFloat(percent[cell]).toFixed(0) + "%</td><td>"+abnormal[cell]+"</td></tr>";
                }
            }

            if(total > 0) {
                //XXX: hack! The cell ids might change
                var erythroid = cell_types[8].count + cell_types[8].abnormal;
                var myeloid = 0;
                var myeloid_cells = [1, 2, 3, 4, 6, 7];
                for (var i = 0; i < myeloid_cells.length; i++) {
                    myeloid += cell_types[myeloid_cells[i]].count;
                    myeloid += cell_types[myeloid_cells[i]].abnormal;
                }
                var meratio = parseFloat(myeloid / erythroid).toFixed(2);
                var stats_text = '<h3>Count statistics</h3><table class="statistics">';
                stats_text += '<tr><td colspan="2" class="celltypes">Total cells</td><td>' + total + '</td><td class="noborder" colspan="2"></td></tr>';
                stats_text += '<tr><td colspan="2" class="celltypes">ME ratio</td><td>' + meratio + '</td><td class="noborder" colspan="2"></td></tr>';
                stats_text += '<tr><th colspan="2" style="width: 30%"></th>';
                stats_text += '<th style="width: 16%">Normal</th>';
                stats_text += '<th style="width: 16%">Abnormal</th>';
                stats_text += '<th style="width: 16%">% Total</th>';
                stats_text += '<th style="width: 22%">% of CellType Abnormal</th></tr>';
                stats_text += per;
                stats_text += '</table>';
                $('div#statistics').empty().append(stats_text);
                $("#visualise2").css("display", "block");
                init_visualisation("#doughnut2");
                update_visualisation();
                $("#total2").text(total);
                $("#savefilebutton").css("display", "block");
                add_save_file_button();
            }

            $('#counterbox').slideUp('slow', function () {
                $('#fuzz').fadeOut('slow', function () {
                });
            });
        }
    });

    //Adjust height of overlay to fill screen when browser gets resized
    $(window).bind("resize", function (){
        $("#fuzz").css("height", $(document).height());
        //$("#total").text($("#counterbox").width());
        //$("#fuzz").css("top", $(window).top());

        if(keyboard_active)
            resize_keyboard($("div#content").width());
    });
    //$("#fuzz").css("height", $(document).height());

    //$(document).keypress(function(e) {
    jQuery(document).bind('keydown', function (e) {
        var key, code, shift_pressed, el, count_total, enter=false;
        var alpha = false, up = false, down = false;
        //Event.stop(e);
        if (keyboard_active) {
            key = String.fromCharCode(e.which).toUpperCase();
            code = e.which;
            shift_pressed = e.shiftKey;
            if (/[a-z]/i.test(key) && !shift_pressed) {
                alpha = true;
            }
            if (code === 188) {
                key = ","; // XXX: WTF
            }
            if (code === 173) {
                key = "-"; // XXX: WTF
            }
            if (key === " ") {
                abnormal = true;
                //Event.stop(e);
                return false;
                //$("div#imagebox").css("background-image", "");
            }
            else if (code === 8) {
                undo = true;
                return false;
            }
            else if (code === 13) {
                enter = true;
            }
            else if(code === 38) {
                up = true;
            }
            else if(code === 40) {
                down = true;
            }

            if(editing_keyboard) {
                if(enter) {
                    deselect_element(selected_element);
                    select_element(selected_element.next());
                    return;
                }
                else if(down) {
                    deselect_element(selected_element);
                    select_element(selected_element.next());
                    return false;
                }
                else if(up) {
                    deselect_element(selected_element);
                    var el = selected_element.prev();
                    if(!$(el).html()) el = $("div#celllist").find("li").last();
                    select_element(el);
                    return false;
                }
                else if(alpha) {
                    if(cell_types.hasOwnProperty(edit_cell_id)) {

                        if($("#multi_key").is(':checked')) {
                            /* DENIES ABILITY TO MAP MULTIPLE KEYS TO THE SAME CELL TYPE
                             * Iterate through all key mappings, looking for any which map to the current cell_id.
                             * If found, delete them. N.B. we decrement the iterator if we've spliced to avoid
                             * issues with the length of the array and correct iteration position.
                             */
                            for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                                if (keyboard_map['mappings'][i]['cellid'] == edit_cell_id) {
                                    keyboard_map['mappings'].splice(i, 1);
                                    i--;
                                }
                            }
                            /* Remove any previous mappings for the key we're trying to add - prevents assigning
                             * two celltypes to a given key.
                             */
                            for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                                if (keyboard_map['mappings'][i]['key'] == key.toLowerCase()) {
                                    keyboard_map['mappings'].splice(i, 1);
                                    i--;
                                }
                            }

                            /* Add the new mapping for this keypress */
                            keyboard_map['mappings'].push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});

                            if($("#auto_advance").is(':checked')) {
                                deselect_element(selected_element);
                                select_element(selected_element.next());
                            }

                        } else {
                            /* We allow multiple mappings to the same cell_id , here we check if the key has been
                             * previously mapped, and if so, we remove any mappings for that key.
                             */
                            for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                                if (keyboard_map['mappings'][i]['key'] == key.toLowerCase()) {
                                    keyboard_map['mappings'].splice(i, 1);
                                    i--;
                                }
                            }

                            /* Add the new mapping */
                            keyboard_map['mappings'].push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});

                            /* Now we need to check that we have indeed mapped a key. If we haven't, it means we are
                             * creating a new map for a previously unmapped key, and therefore should just insert it
                             * into the mappings array.
                             */
                            var is_mapped = false;
                            for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                                if (keyboard_map['mappings'][i]['key'] == key.toLowerCase() &&
                                    keyboard_map['mappings'][i]['cellid'] == edit_cell_id) {
                                    is_mapped = true;
                                }
                            }
                            if (is_mapped === false) {
                                keyboard_map['mappings'].push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});
                            }

                            if($("#auto_advance").is(':checked')) {
                                deselect_element(selected_element);
                                select_element(selected_element.next());
                            }
                        }
                        update_keyboard();
                    }
                }
                return;
            }

            if (shift_pressed) {
                /* We now show the image overlay to the user with the selected celltype images */
                for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                    if (keyboard_map['mappings'][i]['key'].toUpperCase() == key) {
                        var cell_id = keyboard_map['mappings'][i]['cellid'];
                        var slug = cell_types[cell_id].slug;
                        var fullname = cell_types[cell_id].name;

                        var $dialog = $('<div></div>')
                            .load('/images/celltype/'+slug+'/')
                            .dialog({
                                autoOpen: false,
                                title: fullname,
                                width: 900,
                                height: 700
                            });
                        $dialog.dialog('open');
                        /* No further need to iterate through list */
                        break;
                    }
                }

            } else if (img_displayed) {
                $("div#imagebox").css("display", "none");
                img_displayed = false;
                return;
            }

            /* We are now counting, and mapping keypresses to the outcome */
            //count_total = 0;

            for (var i = 0; i < keyboard_map['mappings'].length; i++) {
                if (keyboard_map['mappings'][i]['key'].toUpperCase() == key && !(shift_pressed)) {
                    var id = keyboard_map['mappings'][i]['cellid'];

                    // Add highlighting to keyboard
                    // Remove all currently active highlights (stops a queue developing)
                    for(var i=0; i<cell_types[id].box.length; i++){
                        $(cell_types[id].box[i]).stop(true, true).css("background-color", '#ffffff');
                    }

                    // Add highlight to typed key
                    $(cell_types[id].box).effect("highlight", {}, 200);

                    if(abnormal === true) {
                        if(undo) {
                            if(cell_types[id].abnormal > 0) {
                                cell_types[id].abnormal--;
                                for(var i=0; i<cell_types[id].box.length; i++){
                                    $(cell_types[id].box[i]).find("span.abnormal").text(cell_types[id].abnormal);
                                }
                            }
                        } else {
                            cell_types[id].abnormal++;
                            for(var i=0; i<cell_types[id].box.length; i++){
                                $(cell_types[id].box[i]).find("span.abnormal").text(cell_types[id].abnormal);
                            }
                        }
                    } else if(undo) {
                        if(cell_types[id].count > 0) {
                            cell_types[id].count--;
                            for(var i=0; i<cell_types[id].box.length; i++){
                                $(cell_types[id].box[i]).find("span.countval").text(cell_types[id].count);
                            }
                        }
                    } else {
                        cell_types[id].count++;
                        for(var i=0; i<cell_types[id].box.length; i++){
                            $(cell_types[id].box[i]).find("span.countval").text(cell_types[id].count);
                        }
                    }
                    /* No further need to iterate through list */
                    break;
                }
            }
            update_visualisation();
        }
    });

    jQuery(document).bind('keyup', function (e){
        var key, code;
        if (keyboard_active) {
            code = e.which;
            key = String.fromCharCode(code).toUpperCase();
            if (code === 173) {
                key = "-";// XXX: WTF
            }
            if (key === " ") {
                abnormal = false;
            }
            if (code === 8) {
                undo = false;
            }
        }
    });
});

function resize_keyboard(width) {

    /* Don't do anything as we're using media selectors in the CSS to control the keyboard sizing */

    /*if(width < 1024) {
        $("#keysbox").removeClass("largekeyboard");
        $("#keysbox").addClass("smallkeyboard");
    }
    else {
        $("#keysbox").removeClass("smallkeyboard");
        $("#keysbox").addClass("largekeyboard");
    }*/
}

function reset_counters() {
    for(var x in cell_types) {
        cell_types[x].count = 0;
        cell_types[x].abnormal = 0;
    }
    update_keyboard();
    init_visualisation("#doughnut");
    update_visualisation();
}

/*window.onkeydown=function(e){
if(e.keyCode==32){
return false;
}
}; */
function load_keyboard() {
    $.getJSON("/api/keyboard/", function(data) {
        keyboard_map = data;
        update_keyboard();
        init_visualisation("#doughnut");
        update_visualisation();
    });
}

function update_keyboard() {

    var keyboard_keys = $("#keysbox").find("div.box1");

    for(var x in cell_types) {
        cell_types[x].box = [];
    }

    for (var i = 0; i < keyboard_keys.length; i++) {

        var item = $(keyboard_keys[i]);
        var key = item.attr("id");
            
        item.empty();
        item.append("<p>"+key+"</p>");

        for (var j = 0; j < keyboard_map['mappings'].length; j++) {

            if (keyboard_map['mappings'][j]['key'] === key) {

                var cell_id = keyboard_map['mappings'][j]['cellid'];

                var cell_data = cell_types[cell_id];
                cell_data.box.push(item);
                var name = cell_data.abbr;

                item.append("<div class=\"name\">"+name+"</div>");
                item.append("<div class=\"count\"><span class=\"countval\">"+cell_types[cell_id].count+"</span> (<span class=\"abnormal\">"+cell_types[cell_id].abnormal+"</span>)</div>");

                // Attach cell colour to key
                item.find("p").css("background-color", cell_data.colour);
            }
        }
    }
}

function edit_keyboard() {
    "use strict";
    //var keyboard_keys = $("#keysbox").find("div.box1");

    if(editing_keyboard) return;

    var list = "<ul>";

    for(var x in cell_types) {
        //list += "<li><div class=\"edit_colour_swatch\" id=\"swatch_"+x+"\"></div>"+cell_types[x].name+"<div class=\"cellid\" style=\"display: none;\">"+x+"</div></li>";
        list += "<li><div class=\"element\"><div class=\"edit_colour_swatch\" id=\"swatch_"+x+"\"></div>"+cell_types[x].name+"</div><div class=\"cellid\" style=\"display: none;\">"+x+"</div></li>";
    }
    
    list += "</ul>";

    $("div#celllist").empty();
    $("div#celllist").append(list);

    for(var x in cell_types) {
        $("div#swatch_"+x).css("background-color", cell_types[x].colour);
    }

    $("div#celllist").find("div.element").click(function() {
        edit_cell_id = $(this).find("div.cellid").text();
        $("div#celllist").find("li").css("background", "");
        //$(this).addClass("selectedtype");
        deselect_element(selected_element);
        selected_element = $(this).parent();
        select_element($(this).parent());
    });

    var el = $("div#celllist").find("li").first();
    select_element(el);

    $("#clearkeyboard").click(function() {
        clear_keyboard();
    });
    
    editing_keyboard = true;

    var save_text = "Save";
    var cancel_text = "Cancel";
    var save_keys = true;
    if(typeof notloggedin != 'undefined') {
        save_text = "Close";
        cancel_text = "Revert";
        save_keys = false;
    }

    var d = $("div#editkeymapbox").dialog({
        close: function() {
            if(save_keys)
                load_keyboard();
            end_keyboard_edit();
        },
        open: function() {
            //remove focus from the default button
            $('.ui-dialog :button').blur();
        },
        resizable: false,
        buttons: [ {text: save_text,
                    click: function() {
                        if(save_keys)
                            save_keyboard();
                        else
                            end_keyboard_edit();
                    }
                    },
                    {text: cancel_text,
                    click: function() {
                        if(!save_keys)
                            load_keyboard();
                        $("div#editkeymapbox").dialog("close");
                    }
                    }
                ],
        width: "368px"
    });
    $(d).dialog('widget')
        .position({ my: 'right top', at: 'right top', of: $("div#counterbox") });
}

function select_element(el) {
    "use strict";

    selected_element = $(el);

    if(!selected_element.html()) {
        selected_element = $("div#celllist").find("li").first();
        el = selected_element;
        selected_element = $(selected_element);
    }

    if(selected_element.html()) {
        edit_cell_id = $(el).find("div.cellid").text();
        $(el).addClass("selected");
    }
    else {
        edit_cell_id = -1;
    }
}

function deselect_element(el) {
    "use strict";

    $(el).removeClass("selected");
}

function save_keyboard() {
    "use strict";

    if ("id" in keyboard_map) {
        $.ajax({
            url: '/api/keyboard/' + keyboard_map['id'] + '/',
            type: 'PUT',
            data: JSON.stringify(keyboard_map),
            contentType: "application/json; charset=utf-8",
            async: false,
            success: function(msg) {
                end_keyboard_edit();
            }
        });
    } else {
        $.ajax({
            url: '/api/keyboard/',
            type: 'POST',
            data: JSON.stringify(keyboard_map),
            contentType: "application/json; charset=utf-8",
            async: false,
            success: function(msg) {
                end_keyboard_edit();
            }
        });
    }
}

function end_keyboard_edit() {
    "use strict";

    $("div#celllist").empty();

    editing_keyboard = false;
    edit_cell_id = -1;
    $("#edit_button").show();
    $("div#editkeymapbox").dialog("close");
}

function clear_keyboard() {
    "use strict";
    /* Clear keyboard needs to provide the correct keyboard_map structure
     * otherwise modification of a blank keyboard fails. Also maintain
     * object ID when clearing keyboards so we save to the right place.
      * N.B. .toISOString() requires a shim for IE<= 8 */
    if ('id' in keyboard_map) {
        var id = keyboard_map['id'];
    }
    var date = new Date(Date.now()).toISOString()
    keyboard_map = {"label": "Default", "is_primary": true, "created": date,
                    "last_modified": date, "mappings": new Array()};
    if (id) {
        keyboard_map['id'] = id;
    }
    update_keyboard();
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $.cookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});