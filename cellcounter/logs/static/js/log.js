/*global $:false, jQuery:false */

var hosts = {};
var unique_hosts;
var pages = {};
var dates = {};

var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}


$(document).ready(function() {
    "use strict";
    
    get_hosts();
    get_pages();
    get_referrers();
    get_dates();
    
});

function get_hosts() {
    $.getJSON("/logs/hosts/", function(data) {

        hosts = data["hosts"];
        unique_hosts = data["unique"]
        
        update_hosts();

        //init_visualisation("#doughnut");

        //update_visualisation();
    });
}

function update_hosts() {
    var hosts_sorted = [];
    var i = 0;

    for(var x in hosts) {
        hosts_sorted[i] = {host: x, count: hosts[x].length};
        i++;
    }

    hosts_sorted.sort(function(a, b){
        return b.count-a.count;
    });

    var hosts_text = "<table>"
    var j = 0;
    for(var i in hosts_sorted) {
        var x = hosts_sorted[i];
        j++;
        hosts_text += "<tr><td>"+j+".</td><td>"+x["host"]+"</td><td>"+x["count"]+"</td></tr>";
        if(j>=10) break;
    }
    hosts_text += "</table>"
    $('div#hostsdata').empty().append(hosts_text);

    $('div#uniquehostsdata').empty().append(unique_hosts);
}

function get_pages() {
    $.getJSON("/logs/pages/", function(data) {

        pages = data["pages"];
        
        update_pages();
    });
}

function update_pages() {

    var pages_sorted = [];
    var i = 0;

    for(var x in pages) {
        pages_sorted[i] = {page: x, count: pages[x].length};
        i++;
    }

    pages_sorted.sort(function(a, b){
        return b.count-a.count;
    });

    var pages_text = "<table>";
    var j = 0;
    for(var i in pages_sorted) {
        var x = pages_sorted[i];
        j++;
        pages_text += "<tr><td>"+j+".</td><td>"+x["page"]+"</td><td>"+x["count"]+"</td></tr>";
        if(j>=10) break;
    }
    pages_text += "</table>"
    $('div#pagesdata').empty().append(pages_text);
}

function get_referrers() {
    $.getJSON("/logs/referrers/", function(data) {

        referrers = data["referrers"];
        
        update_referrers();
    });
}

function update_referrers() {

    var referrers_sorted = [];
    var i = 0;

    for(var x in referrers) {
        referrers_sorted[i] = {referrer: x, count: referrers[x].length};
        i++;
    }

    referrers_sorted.sort(function(a, b){
        return b.count-a.count;
    });

    var referrers_text = "<table>";
    var j = 0;
    for(var i in referrers_sorted) {
        var x = referrers_sorted[i];
        j++;
        referrers_text += "<tr><td>"+j+".</td><td>"+escapeHtml(x["referrer"])+"</td><td>"+x["count"]+"</td></tr>";
        if(j>=10) break;
    }
    referrers_text += "</table>"
    $('div#referralsdata').empty().append(referrers_text);

}

function get_dates() {
    $.getJSON("/logs/dates/", function(data) {

        dates = data["dates"];
        
        update_dates();
    });
}

function daysInMonth(month,year) {
    return new Date(year, month, 0).getDate();
}

function update_dates() {

    var dates_sorted = [];

    //graph this month's hits
    var d = new Date();
    month = d.getMonth() + 1;
    year = d.getFullYear();

    days = dates[year][month];

    var count = [];
    var day_labels = [];
    for(var i=0; i<daysInMonth(year, month); i++){
        if(days[i+1]!=undefined)
            count[i] = days[i+1].length;
        else
            count[i] = 0
        day_labels[i] = i+1;
    }

    var w = 700;
    var h = 200;
    var barPadding = 2;

    //Create SVG element
    var svg = d3.select("div#visitorsgraph")
        .append("svg")
        .attr("width", w)
        .attr("height", h+20);

    var xScale = d3.scale.ordinal()
        .domain(day_labels)
        .rangeRoundBands([30, w], .1);

    var yScale = d3.scale.linear()
        .domain([0, d3.max(count)])
        .range([h, 10]);

svg.selectAll("line")
  .data(yScale.ticks(5))
  .enter().append("line")
  .attr("x1", 30)
  .attr("x2", w)
  .attr("y1", yScale)
  .attr("y2", yScale)
  .style("stroke", "#ccc");

svg.selectAll(".rule")
    .data(yScale.ticks(5))
    .enter().append("text")
    .attr("class", "rule")
    .attr("x", 0)
    .attr("y", yScale)
    .attr("dx", 0)
    .attr("dy", 5)
    .attr("text-anchor", "start")
    .text(String);


    svg.selectAll("rect")
        .data(count)
        .enter()
        .append("rect")
        .attr("x", function(d, i) {
            return xScale(i+1); //i * (w / count.length);
        })
        .attr("y", yScale) //function(d) {
        //    return yScale(d);  //Height minus data value
        //})
        //.attr("width", w / count.length - barPadding)
        .attr("width", xScale.rangeBand())
        .attr("height", function(d) {
            return h - yScale(d);  //Just the data value
        })
        .attr("fill", function(d) {
            return "rgb(0, 0, " + (Math.floor(yScale(d)) * 10) + ")";
        });

    svg.selectAll("text")
        .data(count)
        .enter()
        .append("text")
        .text(function(d) {
            return d;
        })
        .attr("x", function(d, i) {
            return xScale(i+1)+xScale.rangeBand()/2 // * (w / count.length) + (w / count.length - barPadding) / 2;
        })
        .attr("y", function(d) {
            return yScale(d) + 14;              // +15
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
        .attr("fill", "white")
        .attr("text-anchor", "middle");


/*var chart = d3.select("body").append("svg")
     .attr("class", "chart")
     .attr("width", 440)
     .attr("height", 140)
     .append("g")
     .attr("transform", "translate(10,15)");*/

//svg.append("line")
//    .attr("x1", 0)
//    .attr("x2", 120)
//    .style("stroke", "#000");



var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(1);

     svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis);


    var monthNames = [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December" ];

    $('span#visitors_span').text("Hits this month (" + monthNames[month-1] + " " + year + "):");

    return;

    
    var i = 0;
    for(var x in dates) {
        dates_sorted[i] = {date: x, count: dates[x].length};
        i++;
    }

    dates_sorted.sort(function(a, b){
        return b.count-a.count;
    });

    var dates_text = "<table>";
    var j = 0;
    for(var i in dates_sorted) {
        var x = dates_sorted[i];
        j++;
        dates_text += "<tr><td>"+j+".</td><td>"+escapeHtml(x["date"])+"</td><td>"+x["count"]+"</td></tr>";
    }
    dates_text += "</table>"
    $('div#visitorsgraph').empty().append(dates_text);
}

