/*global $:false, jQuery:false */
//counters = new Array();
//$box = new Array();
var counters = {};
var abnormal = false;
var undo = false;
var keyboard_active = false;
var img_displayed = false;

$(document).ready(function() {
    "use strict";
    var key, name, img;
    $("#myCounts").tablesorter();

    $('.count').each(function () {
            //access to element via $(this)
            key = $(this).find('div#key').text();
            name = $(this).find('font2').text();
            img = $(this).find('a#img').text();
            counters[name] = {};
            counters[name].key = key.toUpperCase();
            counters[name].count = 0;
            counters[name].abnormal = 0;
            counters[name].box = $(this);
            counters[name].img = img;

            //$count[key] = 0;
            //$count[key + "_abnormal"] = 0;
            //$box[key] = $(this);
            //$box[key + "_abnormal"] = $(this);
    });

    $('#openkeyboard').click(function () {
        $('#fuzz').fadeIn('slow', function () {
            $('#counterbox').slideDown('slow', function () {
            $("#fuzz").css("height", $(document).height());
            keyboard_active = true;
            });
        });
    });

    $('#fuzz').click(function () {
        var output, total, percent, per;
        
        if (keyboard_active) {
            keyboard_active = false;
            output = {};
            total = 0;

            for (var prop in counters) {
                if (counters.hasOwnProperty(prop)) { 
                    // or if (Object.prototype.hasOwnProperty.call(obj,prop)) for safety...
                    output[prop] = {};
                    output[prop].normal = counters[prop].count;
                    output[prop].abnormal = counters[prop].abnormal;

                    total += counters[prop].count;
                    total += counters[prop].count;
                }
            }

            // Put counts into the ModelForms
            for (var cell in output) {
                if (output.hasOwnProperty(cell)) {
                    $("#"+cell+"").children()[1].value=output[cell].normal;
                    $("#"+cell+"").children()[2].value=output[cell].abnormal;
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
                    if (counters[prop].key === key) {
                        if(abnormal === true) {
                            if(undo) {
                                if(counters[prop].abnormal > 0) {
                                    counters[prop].abnormal--;
                                }
                            } else {
                                counters[prop].abnormal++;
                                $(counters[prop].box).find("span#abnormal").text(counters[prop].abnormal);
                            }
                        } else if(undo) {
                            if(counters[prop].count > 0) {
                                counters[prop].count--;
                            }
                        } else {
                            counters[prop].count++;
                            $(counters[prop].box).find("span#countval").text(counters[prop].count);
                        }
                    }
                }
                count_total += counters[prop].abnormal;
                count_total += counters[prop].count;
            }
            $("#total").text(count_total);
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
