/*global $:false, jQuery:false */
var counters = {};
var abnormal = false;
var keyboard_active = false;
var img_displayed = false;
var doughnut = {};
var pie = {};
var arc = {};
var cell_types = {};
var size = 200;
var editing_keyboard = false;
var first_count = true;
var edit_cell_id = -1;
var selected_element = {};
var date_now = new Date(Date.now()).toISOString();
var keyboard_map = {"label": "Default", "is_primary": true, "created": date_now,
                    "last_modified": date_now, "mappings": []};
var key_history = [];

$(document).ready(function() {
    "use strict";
    var count_total;
    $("#myCounts").tablesorter();

    $('.keyboard-label').editable({
        url: function(params) {
            var keyboard = load_specific_keyboard(params.pk);
            keyboard.label = params.value;
            save_keyboard(keyboard);
        }
    });
    
    $.getJSON("/api/cell_types/", function(data) {
        cell_types = {};
        $.each(data, function(key, cell) {
            cell.count = 0;
            cell.abnormal = 0;
            cell.box = [];
            cell_types[cell.id] = cell;
        });
        load_keyboard();
    });

    $('#edit_button').on('click', edit_keyboard);
    register_resets();

    $('#openkeyboard').on('click', open_keyboard);

    $('#fuzz, #close_button').click(function () {
        var total, cell;
        var percent = {};
        var abnormal = {};
        var per = "";

        if (editing_keyboard) {
            return;
        }

        if (keyboard_active) {
            keyboard_active = false;
            total = 0;

            for (cell in cell_types) {
                if (cell_types.hasOwnProperty(cell)) {
                    $("#id_"+cell+"-normal_count").prop("value", cell_types[cell].count);
                    $("#id_"+cell+"-abnormal_count").prop("value", cell_types[cell].abnormal);
                    total += cell_types[cell].count;
                    total += cell_types[cell].abnormal;
                }
            }

            for (cell in cell_types) {
                if (cell_types.hasOwnProperty(cell)) { 
                    // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
                    percent[cell] = (cell_types[cell].count + cell_types[cell].abnormal) / total * 100;
                    if(cell_types[cell].count + cell_types[cell].abnormal !== 0) {
                        abnormal[cell] = cell_types[cell].abnormal / (cell_types[cell].count + cell_types[cell].abnormal) * 100;
                        abnormal[cell] = parseFloat(abnormal[cell]).toFixed(0) + "%";
                    } else {
                        abnormal[cell] = "N/A";
                    }
                    per += '<tr><td class="celltypes">' + cell_types[cell].name + '</td><td class="ignore" style="width: 20px; background-color:'+ cell_types[cell].colour +'"></td><td>'+cell_types[cell].count+'</td><td class="abnormal_count">'+cell_types[cell].abnormal+'</td><td>' + parseFloat(percent[cell]).toFixed(0) + "%</td><td>"+abnormal[cell]+"</td></tr>";
                }
            }

            if(total > 0) {
                //XXX: hack! The cell ids might change
                var erythroid = cell_types[8].count + cell_types[8].abnormal;
                var myeloid = 0;
                var myeloid_cells = [1, 2, 3, 4, 6, 7, 10];
                for (var i = 0; i < myeloid_cells.length; i++) {
                    myeloid += cell_types[myeloid_cells[i]].count;
                    myeloid += cell_types[myeloid_cells[i]].abnormal;
                }
                var meratio = parseFloat(myeloid / erythroid).toFixed(2);
                var stats_text = '<h3>Count statistics</h3><table class="statistics">';
                stats_text += '<tr><td colspan="2" class="celltypes">Total cells</td><td>' + total + '</td><td class="noborder" colspan="2"></td></tr>';
                stats_text += '<tr><td colspan="2" class="celltypes">ME ratio *</td><td>' + meratio + '</td><td class="noborder" colspan="2"></td></tr>';
                stats_text += '<tr><th colspan="2" style="width: 30%"></th>';
                stats_text += '<th style="width: 16%">Normal</th>';
                stats_text += '<th style="width: 16%">Abnormal</th>';
                stats_text += '<th style="width: 16%">% Total</th>';
                stats_text += '<th style="width: 22%">% of CellType Abnormal</th></tr>';
                stats_text += per;
                stats_text += '</table>';
                stats_text += '<p>* Note: Myeloid/erythroid ratio does not include blast count.</p>';
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

            if (first_count === true) {
                $('#openkeyboard').text('Continue counting');
                $('#openkeyboard').removeClass('btn-danger').addClass('btn-success');
                $("<div class='btn btn-large btn-danger reset_button restart_button' style='margin-left: 5px'>Reset counters</div>").insertAfter('#openkeyboard');
                register_resets();
                first_count = false;
            }
        }
    });

    //Adjust height of overlay to fill screen when browser gets resized
    $(window).bind("resize", function (){
        $("#fuzz").css("height", $(document).height());
        //$("#total").text($("#counterbox").width());
        //$("#fuzz").css("top", $(window).top());

        if (keyboard_active) {
            resize_keyboard($("div#content").width());
        }
    });

    jQuery(document).bind('keydown', function (e) {
        var key, code, shift_pressed, el, i, enter=false;
        var alpha = false, up = false, down = false;

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
                if (enter) {
                    deselect_element(selected_element);
                    select_element(selected_element.next());
                    return;
                }
                else if (down) {
                    deselect_element(selected_element);
                    select_element(selected_element.next());
                    return false;
                }
                else if (up) {
                    deselect_element(selected_element);
                    el = selected_element.prev();
                    if (!$(el).html()) {
                        el = $("div#celllist").find("li").last();
                    }
                    select_element(el);
                    return false;
                } else if (alpha) {
                    if (cell_types.hasOwnProperty(edit_cell_id.toString())) {
                        if($("#multi_key").is(':checked')) {
                            /* DENIES ABILITY TO MAP MULTIPLE KEYS TO THE SAME CELL TYPE
                             * Iterate through all key mappings, looking for any which map to the current cell_id.
                             * If found, delete them. N.B. we decrement the iterator if we've spliced to avoid
                             * issues with the length of the array and correct iteration position.
                             */
                            for (i = 0; i < keyboard_map.mappings.length; i++) {
                                if (keyboard_map.mappings[i].cellid == edit_cell_id) {
                                    keyboard_map.mappings.splice(i, 1);
                                    i--;
                                }
                            }
                            /* Remove any previous mappings for the key we're trying to add - prevents assigning
                             * two celltypes to a given key.
                             */
                            for (i = 0; i < keyboard_map.mappings.length; i++) {
                                if (keyboard_map.mappings[i].key == key.toLowerCase()) {
                                    keyboard_map.mappings.splice(i, 1);
                                    i--;
                                }
                            }

                            /* Add the new mapping for this keypress */
                            keyboard_map.mappings.push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});

                            if($("#auto_advance").is(':checked')) {
                                deselect_element(selected_element);
                                select_element(selected_element.next());
                            }

                        } else {
                            /* We allow multiple mappings to the same cell_id , here we check if the key has been
                             * previously mapped, and if so, we remove any mappings for that key.
                             */
                            for (i = 0; i < keyboard_map.mappings.length; i++) {
                                if (keyboard_map.mappings[i].key == key.toLowerCase()) {
                                    keyboard_map.mappings.splice(i, 1);
                                    i--;
                                }
                            }

                            /* Add the new mapping */
                            keyboard_map.mappings.push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});

                            /* Now we need to check that we have indeed mapped a key. If we haven't, it means we are
                             * creating a new map for a previously unmapped key, and therefore should just insert it
                             * into the mappings array.
                             */
                            var is_mapped = false;
                            for (i = 0; i < keyboard_map.mappings.length; i++) {
                                if (keyboard_map.mappings[i].key == key.toLowerCase() &&
                                    keyboard_map.mappings[i].cellid == edit_cell_id) {
                                    is_mapped = true;
                                }
                            }
                            if (is_mapped === false) {
                                keyboard_map.mappings.push({'cellid': parseInt(edit_cell_id), 'key': key.toLowerCase()});
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
                for (i = 0; i < keyboard_map.mappings.length; i++) {
                    if (keyboard_map.mappings[i].key.toUpperCase() == key) {
                        var cell_id = keyboard_map.mappings[i].cellid;
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
                        /* Close any open dialogues before opening*/
                        $(".ui-dialog-content").dialog("close");
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

            if (code === 8) {
                /* Time to remove the key from the key_history and decrement count
                *  Last key should be an array containing:
                *  {c_id:n, c_type:normal/abnormal} */
                e.preventDefault();
                var last_key = key_history.pop();
                if (typeof last_key !== "undefined") {
                    var c_id = last_key.c_id;
                    var c_type = last_key.c_type;
                    if (cell_types[c_id][c_type] > 0) {
                        cell_types[c_id][c_type]--;
                    }
                    /* Generate the appropriate span name to find */
                    var span_field = "span." + c_type;
                    if (span_field === "span.count"){
                        span_field += "val";
                    }
                    for (i=0; i<cell_types[c_id].box.length; i++){
                        $(cell_types[c_id].box[i]).find(span_field).text(cell_types[c_id][c_type]);
                    }
                    /* Re-initiate visualisation if key_history has been deleted completely */
                    if (key_history.length === 0) {
                        init_visualisation("#doughnut");
                    }
                } else {
                    /* Nothing to delete */
                    key_history = [];
                }
            } else {
                for (i = 0; i < keyboard_map.mappings.length; i++) {
                    if (keyboard_map.mappings[i].key.toUpperCase() == key && !(shift_pressed)) {
                        var id = keyboard_map.mappings[i].cellid;

                        // Add highlighting to keyboard
                        // Remove all currently active highlights (stops a queue developing)
                        for (i=0; i<cell_types[id].box.length; i++){
                            $(cell_types[id].box[i]).stop(true, true).css("background-color", '#ffffff');
                        }

                        // Add highlight to typed key
                        $(cell_types[id].box).effect("highlight", {}, 200);

                        if (abnormal === true) {
                            cell_types[id].abnormal++;
                            for(i = 0; i < cell_types[id].box.length; i++){
                                $(cell_types[id].box[i]).find("span.abnormal").text(cell_types[id].abnormal);
                            }
                            key_history.push({c_id: id, c_type: 'abnormal'});
                        } else {
                            cell_types[id].count++;
                            for (i=0; i<cell_types[id].box.length; i++){
                                $(cell_types[id].box[i]).find("span.countval").text(cell_types[id].count);
                            }
                            key_history.push({c_id: id, c_type: 'count'});
                        }
                        /* No further need to iterate through list */
                        break;
                    }
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
        }
    });
});

function resize_keyboard(width) {
    /* Does nothing */
}

function register_resets() {
    "use strict";
    $('.reset_button').on('click', function() {
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
}

function reset_counters() {
    "use strict";
    for (var cell in cell_types) {
        if (cell_types.hasOwnProperty(cell)) {
            cell_types[cell].count = 0;
            cell_types[cell].abnormal = 0;
        }
    }
    key_history = [];
    update_keyboard();
    init_visualisation("#doughnut");
    update_visualisation();
    open_keyboard();
}

function open_keyboard() {
    $('#fuzz').fadeIn('slow', function () {
        resize_keyboard($("div#content").width());
        $('#counterbox').slideDown('slow', function () {
            $("#fuzz").css("height", $(document).height());
            keyboard_active = true;
        });
    });
    var count_total = 0;
    for (var prop in counters) {
        if (counters.hasOwnProperty(prop)) {
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
}

function load_keyboard() {
    "use strict";
    $.getJSON("/api/keyboards/default/", function(data) {
        keyboard_map = data;
        update_keyboard();
        init_visualisation("#doughnut");
        update_visualisation();
    });
}

function load_specific_keyboard(keyboard_id) {
    "use strict";
    var keyboard = {};
    $.ajax({
        url: '/api/keyboards/' + keyboard_id + '/',
        type: 'GET',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        async: false,
        success: function(data) {
            keyboard = data;
        }
    });
    return keyboard;
}

function set_keyboard_primary(keyboard_id) {
    "use strict";
    var keyboard = load_specific_keyboard(keyboard_id);
    keyboard.is_primary = true;
    save_keyboard(keyboard);
    return false;
}

function delete_specific_keyboard(keyboard_id) {
    "use strict";
    var keyboard = load_specific_keyboard(keyboard_id);
    $.ajax({
        url: '/api/keyboards/' + keyboard.id + '/',
        type: 'DELETE',
        data: JSON.stringify(keyboard),
        contentType: "application/json; charset=utf-8",
        async: false
    });
}

function update_keyboard() {
    "use strict";
    var i, j;
    var keyboard_keys = $("#keysbox").find("div.box1");

    for (var cell in cell_types) {
        if (cell_types.hasOwnProperty(cell)) {
            cell_types[cell].box = [];
        }
    }

    for (i = 0; i < keyboard_keys.length; i++) {
        var item = $(keyboard_keys[i]);
        var key = item.attr("id");
            
        item.empty();
        item.append("<p>"+key+"</p>");

        for (j = 0; j < keyboard_map.mappings.length; j++) {

            if (keyboard_map.mappings[j].key === key) {
                var cell_id = keyboard_map.mappings[j].cellid;
                var cell_data = cell_types[cell_id];
                cell_data.box.push(item);
                var name = cell_data.abbr;

                item.append("<div class=\"name\">"+name+"</div>");
                item.append("<div class=\"count\"><span class=\"countval\">"+cell_types[cell_id].count+"</span> (<span class=\"abnormal abnormal_count\">"+cell_types[cell_id].abnormal+"</span>)</div>");

                // Attach cell colour to key
                item.find("p").css("background-color", cell_data.colour);
            }
        }
    }
}

function edit_keyboard() {
    "use strict";

    if (editing_keyboard) {
        return;
    }
    var cell;
    var list = "<ul>";

    for (cell in cell_types) {
        if (cell_types.hasOwnProperty(cell)) {
            list += "<li><div class=\"element\"><div class=\"edit_colour_swatch\" id=\"swatch_"+cell+"\"></div>"+cell_types[cell].name+"</div><div class=\"cellid\" style=\"display: none;\">"+cell+"</div></li>";
        }
    }
    list += "</ul>";

    $("div#celllist").empty();
    $("div#celllist").append(list);

    for (cell in cell_types) {
        if (cell_types.hasOwnProperty(cell)) {
            $("div#swatch_"+cell).css("background-color", cell_types[cell].colour);
        }
    }

    $("div#celllist").find("div.element").click(function() {
        edit_cell_id = $(this).find("div.cellid").text();
        $("div#celllist").find("li").css("background", "");
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
    if(typeof notloggedin !== 'undefined') {
        save_text = "Close";
        cancel_text = "Revert";
        save_keys = false;
    }

    var d = $("div#editkeymapbox").dialog({
        close: function() {
            if (save_keys) {
                load_keyboard();
            }
            end_keyboard_edit();
        },
        open: function() {
            //remove focus from the default button
            $('.ui-dialog :button').blur();
        },
        resizable: false,
        buttons: [ {text: save_text,
                    click: function() {
                        if (save_keys) {
                            save_keyboard();
                        } else {
                            end_keyboard_edit();
                        }
                    }
                    },
                    {text: 'Save as New',
                     click: function() {
                         if (save_keys) {
                             delete(keyboard_map['id']);
                             save_keyboard();
                         } else {
                             end_keyboard_edit();
                         }
                     }
                    },
                    {text: cancel_text,
                     click: function() {
                         if (!save_keys) {
                             load_keyboard();
                         }
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

function save_keyboard(keyboard) {
    "use strict";

    if (typeof keyboard === 'undefined') {
        keyboard = keyboard_map;
    }

    if ("id" in keyboard) {
        $.ajax({
            url: '/api/keyboards/' + keyboard.id + '/',
            type: 'PUT',
            data: JSON.stringify(keyboard),
            contentType: "application/json; charset=utf-8",
            async: false,
            success: function(msg) {
                end_keyboard_edit();
            }
        });
    } else {
        $.ajax({
            url: '/api/keyboards/',
            type: 'POST',
            data: JSON.stringify(keyboard),
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
        var id = keyboard_map.id;
    }
    var date = new Date(Date.now()).toISOString();
    keyboard_map = {"label": "Default", "is_primary": true, "created": date,
                    "last_modified": date, "mappings": []};
    if (typeof id !== 'undefined') {
        keyboard_map.id = id;
    }
    update_keyboard();
}

function csrfSafeMethod(method) {
    "use strict";
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    "use strict";
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
        "use strict";
        var csrftoken = $.cookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});