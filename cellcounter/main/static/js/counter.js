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
var data = [];
    var size = 200;

$(document).ready(function() {
    "use strict";
    var key, name, img, count_total;
    $("#myCounts").tablesorter();

    $.getJSON("/accounts/keyboard/", function(data) {

        keyboard_map = data;

        var keyboard_keys = $("#terbox").find("div.box1");

        for (var i = 0; i < keyboard_keys.length; i++) {

            var item = $(keyboard_keys[i]);
            var key = item.attr("id");

            if(keyboard_map[key]!==undefined) {
                item.removeClass("c1");
                item.addClass("c2");

                var key_data = keyboard_map[item.attr("id")];

                var name = key_data.name;
                counters[name] = {};
                counters[name].key = key.toUpperCase();
            
                counters[name].count = 0; //parseInt($("#id_"+name+"-normal_count").prop("value"));
                counters[name].abnormal = 0; //parseInt($("#id_"+name+"-abnormal_count").prop("value"));
                counters[name].box = item;
                counters[name].colour = key_data.colour;

                item.append("<div class=\"name\">"+name+"</div>");
                item.append("<div class=\"count\"><span class=\"countval\">"+counters[name].count+"</span> (<span class=\"abnormal\">"+counters[name].abnormal+"</span>)</div>");
                counters[name].img = "";
            }
        }

        init_visualisation();
    });

        /*
        name = item.name;
        key = item.key;

        counters[name] = {};
        counters[name].key = key.toUpperCase();

        $("")
        counters[name].count = parseInt($("#id_"+name+"-normal_count").prop("value"));
        counters[name].abnormal = parseInt($("#id_"+name+"-abnormal_count").prop("value"));
        counters[name].box = $(this);
        counters[name].img = img;
        */

    /*$('.count').each(function () {
        //access to element via $(this)
        key = $(this).find('div#key').text();
        name = $(this).find('font2').text();
        img = $(this).find('a#img').text();
        counters[name] = {};
        counters[name].key = key.toUpperCase();
        counters[name].count = parseInt($("#id_"+name+"-normal_count").prop("value"));
        counters[name].abnormal = parseInt($("#id_"+name+"-abnormal_count").prop("value"));
        counters[name].box = $(this);
        counters[name].img = img;

        $(counters[name].box).find("span#countval").text(counters[name].count);
        $(counters[name].box).find("span#abnormal").text(counters[name].abnormal);
    });*/

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
            for (var cell in counters) {
                if (counters.hasOwnProperty(cell)) {
                    $("#id_"+cell+"-normal_count").prop("value", counters[cell].count);
                    $("#id_"+cell+"-abnormal_count").prop("value", counters[cell].abnormal);
                    total += counters[cell].count;
                    total += counters[cell].abnormal;
                }
            }
       
            percent = {};
            per = "";
       
            for (var prop in counters) {
                if (counters.hasOwnProperty(prop)) { 
                    // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
                    percent[prop] = (counters[prop].count + counters[prop].abnormal) / total * 100;
                    per += '<tr><td style="width: 20%">' + prop + '</td><td style="width: 20%">' + parseFloat(percent[prop]).toFixed(2) + "%</td></tr>";
                }
            }

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
                for (var prop in counters) {
                    if (counters.hasOwnProperty(prop)) {
                        if(counters[prop].key === key) {
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
            for (var prop in counters) {
                if (counters.hasOwnProperty(prop))  {
                    if (counters[prop].key === key && !(shift_pressed)) {
                        if(abnormal === true) {
                            if(undo) {
                                if(counters[prop].abnormal > 0) {
                                    counters[prop].abnormal--;
                                    $(counters[prop].box).find("span.abnormal").text(counters[prop].abnormal);
                                }
                            } else {
                                counters[prop].abnormal++;
                                $(counters[prop].box).find("span.abnormal").text(counters[prop].abnormal);
                            }
                        } else if(undo) {
                            if(counters[prop].count > 0) {
                                counters[prop].count--;
                                $(counters[prop].box).find("span.countval").text(counters[prop].count);
                            }
                        } else {
                            counters[prop].count++;
                            $(counters[prop].box).find("span.countval").text(counters[prop].count);
                        }
                    }
                }
                count_total += counters[prop].count;
                count_total += counters[prop].abnormal;
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
