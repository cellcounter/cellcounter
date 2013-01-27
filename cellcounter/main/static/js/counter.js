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

        $.getJSON("/accounts/keyboard/", function(data) {

            keyboard_map = data;
            
            update_keyboard();

            init_visualisation();
        });
    
    });

    $('#edit_button').on('click', edit_keyboard);

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
        $("#total").text(count_total);
        }
    });

    $('#fuzz').click(function () {
        var total, percent, per;
        
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
                $('div#statistics').empty().append('<h3>Count statistics</h3><table class="statistics"><tr><th></th><th>Normal</th><th>Abnormal</th><th>Percentage (abnormal)</th></tr>' + per + '</table>');
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
        var key, code, shift_pressed, el, count_total, abnormal_total;
        //Event.stop(e);
        if (keyboard_active) {
            key = String.fromCharCode(e.which).toUpperCase();
            code = e.which;
            shift_pressed = e.shiftKey;
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
            } else if (code === 8) {
                undo = true;
                return false;
            }

            if(editing_keyboard) {
                if(cell_types.hasOwnProperty(edit_cell_id)) {
                    console.log("mapping " + key + " to " + cell_types[edit_cell_id].name);
                    keyboard_map[key.toLowerCase()].cellid = edit_cell_id; //wtf: fix upper/lower case!
                    $("div#celllist").find("li").removeClass("selectedtype");
                    edit_cell_id = -1;
                    update_keyboard();
                }
                return;
            }

            if (shift_pressed) {
                for (var prop in keyboard_map) {
                    if (keyboard_map.hasOwnProperty(prop)) {
                        if(keyboard_map[prop].key === key) {
                            el = $("div#imagebox");
                            el.css("display", "block");
                            el.find("div#imgdisplay").css("background-image", "url(" + counters[prop].img + ")");
                            img_displayed = true;
                        }
                    }
                }
            } else if (img_displayed) {
                $("div#imagebox").css("display", "none");
                img_displayed = false;
                return;
            }

            count_total = 0;
            abnormal_total = 0;
            for (var mapped_key in keyboard_map) {
                if (keyboard_map.hasOwnProperty(mapped_key))  {
                    var id = keyboard_map[mapped_key].cellid;
                    if (mapped_key.toUpperCase() === key && !(shift_pressed)) {

                        // Add highlighting to keyboard
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
                count_total += cell_types[id].count;
                count_total += cell_types[id].abnormal;
            }
            $("#total").text(count_total);
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

/*window.onkeydown=function(e){
if(e.keyCode==32){
return false;
}
}; */

function update_keyboard() {
        var keyboard_keys = $("#terbox").find("div.box1");

        for(var x in cell_types) {
            cell_types[x].box = [];
        }

        for (var i = 0; i < keyboard_keys.length; i++) {

            var item = $(keyboard_keys[i]);
            var key = item.attr("id");

            if(keyboard_map[key]!==undefined) {

                var key_data = keyboard_map[item.attr("id")];

                var id = key_data.cellid;

                var cell_data = cell_types[id];
                cell_data.box.push(item);
                var name = cell_data.slug;

                item.empty();
                item.append("<p>"+key+"</p>");
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

    var list = "<ul>";

    for(var x in cell_types) {
        list += "<li>"+cell_types[x].name+"<div class=\"cellid\" style=\"display: none;\">"+x+"</div></li>";
    }
    
    list += "</ul>";

    $("div#celllist").empty();
    $("div#celllist").append(list);

    $("div#celllist").find("li").click(function() {
        console.log($(this).find("div.cellid").text());
        edit_cell_id = $(this).find("div.cellid").text();
        $("div#celllist").find("li").removeClass("selectedtype");
        $(this).addClass("selectedtype");
    });

    editing_keyboard = true;
    $("#edit_button").text("Save");
    $('#edit_button').on('click', save_keyboard);
}

function save_keyboard() {
    "use strict";

    $("div#celllist").empty();

    editing_keyboard = false;
    edit_cell_id = -1;
    $("#edit_button").text("Edit");
    $('#edit_button').on('click', edit_keyboard);
        
    /*$.ajax({
        type: "POST",
        url: "/accounts/keyboard/",
        data: $.toJSON(keyboard_map)
    });*/
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
