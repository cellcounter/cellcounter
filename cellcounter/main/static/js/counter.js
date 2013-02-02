/*global $:false, jQuery:false */
//counters = new Array();
//$box = new Array();
var counters = {};
var abnormal = false;
var undo = false;
var keyboard_active = false;
var img_displayed = false;
var keyboard_map = { 'u': {'name': 'neutro'} };
var doughnut = {};
var pie = {};
var arc = {};
var cell_types = [];
var size = 200;
var editing_keyboard = false;
var edit_cell_id = -1;
var selected_element = {};

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

    $('#fuzz').click(function () {
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
                    per += '<tr><td style="width: 20%" class="celltypes">' + cell_types[cell].name + '</td><td>'+cell_types[cell].count+'</td><td>'+cell_types[cell].abnormal+'</td><td style="width: 50%">' + parseFloat(percent[cell]).toFixed(0) + "% ("+abnormal[cell]+")</td></tr>";
                }
            }

            if(total > 0) {
                //XXX: hack! The cell ids might change
                var erythroid = cell_types[8].count + cell_types[8].abnormal;
                var myeloid = 0;
                var myeloid_cells = [1, 2, 3, 4, 6, 7];
                for(var i in myeloid_cells) {
                    myeloid += cell_types[myeloid_cells[i]].count;
                    myeloid += cell_types[myeloid_cells[i]].abnormal;
                }
                var meratio = parseFloat(myeloid / erythroid).toFixed(2);
                var stats_text = '<h3>Count statistics</h3><table class="statistics">';
                stats_text += '<tr><td>Total cells</td><td>' + total + '</td><td colspan="2"></td></tr>';
                stats_text += '<tr><td>ME ratio</td><td>' + meratio + '</td><td colspan="2"></td></tr>';
                stats_text += '<tr><th></th><th>Normal</th><th>Abnormal</th><th>Percentage (abnormal)</th></tr>';
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
        //$("#fuzz").css("top", $(window).top());
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
                            // clear all other keys mapped to this cellid
                            for(var k in keyboard_map) {
                                if(keyboard_map[k].cellid == edit_cell_id)
                                    delete keyboard_map[k];
                            }
                            keyboard_map[key.toLowerCase()] = {}; //wtf: fix upper/lower case!
                            keyboard_map[key.toLowerCase()].cellid = edit_cell_id;
                            if($("#auto_advance").is(':checked')) {
                                deselect_element(selected_element);
                                select_element(selected_element.next());
                            }
                        }
                        else {
                            if(keyboard_map[key.toLowerCase()]!=undefined && 
                               keyboard_map[key.toLowerCase()].cellid == edit_cell_id) {
                                    delete keyboard_map[key.toLowerCase()];
                            }
                            else {
                                keyboard_map[key.toLowerCase()] = {}; //wtf: fix upper/lower case!
                                keyboard_map[key.toLowerCase()].cellid = edit_cell_id;
                                if($("#auto_advance").is(':checked')) {
                                    deselect_element(selected_element);
                                    select_element(selected_element.next());
                                }
                            }
                        }
                        update_keyboard();
                    }
                }
                return;
            }

            if (shift_pressed) {
                for (var prop in keyboard_map) {
                    if (keyboard_map.hasOwnProperty(prop)) {
                        if(prop.toUpperCase() === key) {
                                var randomid = keyboard_map[prop].cellid;
                                var slug = cell_types[randomid].slug;
                                var fullname = cell_types[randomid].name;

                                var $dialog = $('<div></div>')
                                    .load('/images/celltype/'+slug+'/')
                                    .dialog({
                                        autoOpen: false,
                                        title: fullname,
                                        width: 840,
                                        height: 600
                                    });
                                $dialog.dialog('open');
                        }
                    }
                }
            } else if (img_displayed) {
                $("div#imagebox").css("display", "none");
                img_displayed = false;
                return;
            }

            //count_total = 0;
            for (var mapped_key in keyboard_map) {
                if (keyboard_map.hasOwnProperty(mapped_key))  {
                    var id = keyboard_map[mapped_key].cellid;
                    if (mapped_key.toUpperCase() === key && !(shift_pressed)) {

                        // Add highlighting to keyboard
                        //$(cell_types[id].box).stop(true, true); //effect("highlight", {}, 200);
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
                    }
                }
                //count_total += cell_types[id].count;
                //count_total += cell_types[id].abnormal;
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
    $.getJSON("/accounts/keyboard/", function(data) {

        keyboard_map = data;
        
        update_keyboard();

        init_visualisation("#doughnut");

        update_visualisation();
    });
}

function update_keyboard() {
        var keyboard_keys = $("#terbox").find("div.box1");

        for(var x in cell_types) {
            cell_types[x].box = [];
        }

        for (var i = 0; i < keyboard_keys.length; i++) {

            var item = $(keyboard_keys[i]);
            var key = item.attr("id");
            
            item.empty();
            item.append("<p>"+key+"</p>");

            if(keyboard_map[key]!==undefined) {

                var key_data = keyboard_map[item.attr("id")];

                var id = key_data.cellid;

                var cell_data = cell_types[id];
                cell_data.box.push(item);
                var name = cell_data.abbr;

                item.append("<div class=\"name\">"+name+"</div>");
                item.append("<div class=\"count\"><span class=\"countval\">"+cell_types[id].count+"</span> (<span class=\"abnormal\">"+cell_types[id].abnormal+"</span>)</div>");
                
                // Attach cell colour to key
                item.find("p").css("background-color", cell_data.colour);
            }
        }
    }

function edit_keyboard() {
    "use strict";
    //var keyboard_keys = $("#terbox").find("div.box1");

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

    var d = $("div#editkeymapbox").dialog({
        close: function() {
            load_keyboard();
            end_keyboard_edit();
        },
        open: function() {
            //remove focus from the default button
            $('.ui-dialog :button').blur();
        },
        resizable: false,
        buttons: [ {text: "Save",
                    click: function() {
                        save_keyboard();
                    }
                    },
                    {text: "Cancel",
                    click: function() {
                        $("div#editkeymapbox").dialog("close");
                    }
                    }
                ],
        width: "348px"
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

    $.ajax({
        url: '/accounts/keyboard/',
        type: 'POST',
        data: JSON.stringify(keyboard_map),
        async: false,
        success: function(msg) {
            end_keyboard_edit();
        }
    });

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

    keyboard_map = {};
    update_keyboard();
}

function ironstain() {
    "use strict";
    if ($("#id_ironstain-stain_performed").prop("checked")) {
        $("#id_ironstain-ringed_sideroblasts").prop("disabled", false);
        $("#id_ironstain-iron_content").prop("disabled", false);
        $("#id_ironstain-comment").prop("disabled", false);
    } else {
        $("#id_ironstain-ringed_sideroblasts").prop("disabled", true);
        $("#id_ironstain-iron_content").prop("disabled", true);
        $("#id_ironstain-comment").prop("disabled", true);
    }
}

function granulopoiesis() {
    "use strict";
    if ($("#id_granulopoiesis-no_dysplasia").prop("checked")) {
        $("#id_granulopoiesis-hypogranular").prop("disabled", true);
        $("#id_granulopoiesis-hypogranular").prop("checked", false);
        $("#id_granulopoiesis-pelger").prop("disabled", true);
        $("#id_granulopoiesis-pelger").prop("checked", false);
        $("#id_granulopoiesis-nuclear_atypia").prop("disabled", true);
        $("#id_granulopoiesis-nuclear_atypia").prop("checked", false);
        $("#id_granulopoiesis-dohle_bodies").prop("disabled", true);
        $("#id_granulopoiesis-dohle_bodies").prop("checked", false);
   } else {
        $("#id_granulopoiesis-hypogranular").prop("disabled", false);
        $("#id_granulopoiesis-pelger").prop("disabled", false);
        $("#id_granulopoiesis-nuclear_atypia").prop("disabled", false);
        $("#id_granulopoiesis-dohle_bodies").prop("disabled", false);
    }
}

function erythropoiesis() {
    "use strict";
    if ($("#id_erythropoiesis-no_dysplasia").prop("checked")) {
        $("#id_erythropoiesis-nuclear_asynchrony").prop("disabled", true);
        $("#id_erythropoiesis-nuclear_asynchrony").prop("checked", false);
        $("#id_erythropoiesis-multinucleated_forms").prop("disabled", true);
        $("#id_erythropoiesis-multinucleated_forms").prop("checked", false);
        $("#id_erythropoiesis-ragged_haemoglobinisation").prop("disabled", true);
        $("#id_erythropoiesis-ragged_haemoglobinisation").prop("checked", false);
        $("#id_erythropoiesis-megaloblastic_change").prop("disabled", true);
        $("#id_erythropoiesis-megaloblastic_change").prop("checked", false);
    } else {
        $("#id_erythropoiesis-nuclear_asynchrony").prop("disabled", false);
        $("#id_erythropoiesis-multinucleated_forms").prop("disabled", false);
        $("#id_erythropoiesis-ragged_haemoglobinisation").prop("disabled", false);
        $("#id_erythropoiesis-megaloblastic_change").prop("disabled", false);
    }
}

function megakaryocytes() {
    "use strict";
    if ($("#id_megakaryocyte-no_dysplasia").prop("checked")) {
        $("#id_megakaryocyte-hypolobulated").prop("disabled", true);
        $("#id_megakaryocyte-hypolobulated").prop("checked", false);
        $("#id_megakaryocyte-fragmented").prop("disabled", true);
        $("#id_megakaryocyte-fragmented").prop("checked", false);
        $("#id_megakaryocyte-micromegakaryocytes").prop("disabled", true);
        $("#id_megakaryocyte-micromegakaryocytes").prop("checked", false);
    } else {
        $("#id_megakaryocyte-hypolobulated").prop("disabled", false);
        $("#id_megakaryocyte-fragmented").prop("disabled", false);
        $("#id_megakaryocyte-micromegakaryocytes").prop("disabled", false);
    }
}
