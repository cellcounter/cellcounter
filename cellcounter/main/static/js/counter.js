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
        }

        $.getJSON("/accounts/keyboard/", function(data) {

            keyboard_map = data;

            var keyboard_keys = $("#terbox").find("div.box1");

            for (var i = 0; i < keyboard_keys.length; i++) {

                var item = $(keyboard_keys[i]);
                var key = item.attr("id");

                if(keyboard_map[key]!==undefined) {

                    var key_data = keyboard_map[item.attr("id")];

                    var id = key_data.cellid;

                    var cell_data = cell_types[id];
                    cell_data.box = item;
                    var name = cell_data.slug;

                    // Attach cell colour to key
                    item.find("p").css("background-color", cell_data.colour);

                    item.append("<div class=\"name\">"+name+"</div>");
                    item.append("<div class=\"count\"><span class=\"countval\">"+cell_types[id].count+"</span> (<span class=\"abnormal\">"+cell_types[id].abnormal+"</span>)</div>");
                }
            }

            init_visualisation();
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
        $("#total").text(count_total);
        }
        //edit_keyboard();
    });

    $('#fuzz').click(function () {
        var total, percent, per;
        
        if (keyboard_active) {
            keyboard_active = false;
            total = 0;

            // Put counts into the ModelForms, increment total
            /*for (var cell in cell_types) {
                if (counters.hasOwnProperty(cell)) {
                    $("#id_"+cell+"-normal_count").prop("value", counters[cell].count);
                    $("#id_"+cell+"-abnormal_count").prop("value", counters[cell].abnormal);
                    total += counters[cell].count;
                    total += counters[cell].abnormal;
                }
            }*/
       
            percent = {};
            per = "";
       
            /*for (var prop in counters) {
                if (counters.hasOwnProperty(prop)) { 
                    // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
                    percent[prop] = (counters[prop].count + counters[prop].abnormal) / total * 100;
                    per += '<tr><td style="width: 20%">' + prop + '</td><td style="width: 20%">' + parseFloat(percent[prop]).toFixed(2) + "%</td></tr>";
                }
            }*/

            if(total > 0) {
                $('div#statistics').empty().append('<h3>Count statistics</h3><table id="statistics">' + per + '</table>');
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
                        if(abnormal === true) {
                            if(undo) {
                                if(cell_types[id].abnormal > 0) {
                                    cell_types[id].abnormal--;
                                    $(cell_types[id].box).find("span.abnormal").text(cell_types[id].abnormal);
                                }
                            } else {
                                cell_types[id].abnormal++;
                                $(cell_types[id].box).find("span.abnormal").text(cell_types[id].abnormal);
                            }
                        } else if(undo) {
                            if(cell_types[id].count > 0) {
                                cell_types[id].count--;
                                $(cell_types[id].box).find("span.countval").text(cell_types[id].count);
                            }
                        } else {
                            cell_types[id].count++;
                            $(cell_types[id].box).find("span.countval").text(cell_types[id].count);
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

function edit_keyboard() {
    "use strict";
    var keyboard_keys = $("#terbox").find("div.box1");

    for (var i = 0; i < keyboard_keys.length; i++) {

        var item = $(keyboard_keys[i]);
        var key = item.attr("id");

        var name = "";
        if(keyboard_map[key]!==undefined) {
            var name = keyboard_map[key].name;
            //var key_data = keyboard_map[item.attr("id")];

            //var name = key_data.name;
        }
        item.append("<input name=\""+key+"\" type=\"text\" value=\""+name+"\" />");
    }
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
