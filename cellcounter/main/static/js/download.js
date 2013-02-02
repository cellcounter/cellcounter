//$(document).ready(function() {

function add_save_file_button() {
    $("#downloadify").downloadify( {
        filename: function(){
            return "cellcountr.csv";
        },
        data: function(){ 
            return $("table.statistics").toCSV();
        },
        onError: function(){ 
            alert('Unable to save file'); 
        },
        transparent: true,
        swf: '/static/swf/downloadify.swf',
        downloadImage: '/static/images/download.png?rev=1',
        width: 130,
        height: 30,
        //append: false
        dataType: "string"
    });

    //simulate hovering over the button hidden beneath
    $("#downloadify").hover(
    function () {
        $("#downloadify_button").addClass("hover2");
    },
    function () {
        $("#downloadify_button").removeClass("hover2");
    }
    );
}

