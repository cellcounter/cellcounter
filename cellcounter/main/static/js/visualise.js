var display_data = {};
//$(document).ready(function() {
function init_visualisation() {
    "use strict";

    // Size of doughnut.
    //var size = 200;

    // Set up a function used to calculate the angles of the doughnut.
    pie = d3.layout.pie()
        // This ensures the segments remain ordered.
        .sort(null) 
        .value(function(d) { return d.count; });

    // Set up a function used to calculate the width of the doughnut.
    arc = d3.svg.arc()
        .outerRadius(size / 2)
        .innerRadius(size / 4);

    // Set up the SVG element for the doughnut on the page.
    $('#doughnut').empty();
    doughnut = d3.select('#doughnut').append('svg')
        .attr('width', size)
        .attr('height', size)
      .append('g')
        // This ensures the doughnut is centred in the SVG element.
        .attr('transform', 'translate(' + size / 2 + ',' + size / 2 + ')');

    display_data = [];

    for(var x in cell_types) {
        display_data.push(cell_types[x]);
    }

    // Bind the data to the doughnut and create a grouping element ('g') for
    // each item of data.
    doughnut.selectAll('g')
        .data(pie(display_data))
      .enter().append('g');

    // Add the paths to grouping elements and set the colour.
    doughnut.selectAll('g').append('path')
        .style("fill", function(d) { return d.data.colour });

    // Add the text to grouping elements.
    doughnut.selectAll('g').append('text')
        .attr('dy', '.35em')
        .style('text-anchor', 'middle');
 
}

function update_visualisation() {

    display_data = [];

    for(var x in cell_types) {
        display_data.push(cell_types[x]);
    }

    // Update the doughnut's data.
    doughnut.selectAll('g')
        .data(pie(display_data));

    // Redraw the paths.
    doughnut.selectAll('g').select('path')
        .attr('d', arc);

    // Display the text and put it in the right location.
    doughnut.selectAll('g').select('text')
        .attr('transform', function(d) { return 'translate(' + arc.centroid(d) + ')'; })
        .text(function(d) { return d.value > 0 ? d.data.key : ''; });

}

