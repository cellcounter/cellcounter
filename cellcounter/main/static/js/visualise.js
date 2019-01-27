function doughnutChart(selector_id) {
    "use strict";
    var _chart = {};

    var _width = 200, _height = 200,
        _data = [],
        _svg, _bodyG, _pieG,
        _radius = 100,
        _inner_radius = 50;

    _chart.render = function(data) {
        if (!_svg) {
            _svg = d3.select(selector_id).append("svg")
                .attr("height", _height)
                .attr("width", _width);
        }
        renderBody(_svg);
    };

    function renderBody(svg) {
        if (!_bodyG) {
            _bodyG = svg.append("g")
                .attr("class", "body");
        }
        renderDoughnut();
    }

    function renderDoughnut() {
        var pie = d3.layout.pie()
            .sort(null)
            .value(function (d) {
                return d.count + d.abnormal;
            });

        var arc = d3.svg.arc()
            .outerRadius(_radius)
            .innerRadius(_inner_radius);

        if (!_pieG) {
            _pieG = _bodyG.append("g")
                .attr("class", "pie")
                .attr("transform", "translate("
                    + _radius
                    + ","
                    + _radius + ")");
        }
        renderSlices(pie, arc);
        renderLabels(pie, arc);
    }

    function renderSlices(pie, arc) {
        var slices;

        if (pie(_data).filter(function(d) {return d.value > 0;}).length > 0 ) {
            slices = _pieG.selectAll("path.arc")
                .data(pie(_data));

            slices.enter()
                .append("path")
                .attr("class", "arc")
                .attr("fill", function (d) {
                    return d.data.visualisation_colour;
                });

            slices.transition()
                .attrTween("d", function (d) {
                    var currentArc = this.__current__;
                    if (!currentArc) {
                        currentArc = {startAngle: 0, endAngle: 0};
                    }
                    var interpolate = d3.interpolate(currentArc, d);
                    this.__current__ = interpolate(1);
                    return function (t) {
                        return arc(interpolate(t));
                    };
                });
        } else {
            /* This handles the case when you have an empty (i.e. Zero'd graph) */
            slices = _pieG.selectAll("path.arc")
                .data(pie(_data));
            slices.remove();
        }
    }

    function renderLabels() {

        var total = 0;
        for (var j=0; j < _data.length; j++) {
            total += (_data[j].count + _data[j].abnormal);
        }
        $("div.total").text(total);
    }

    _chart.data = function(d) {
        if (!arguments.length) {
            return _data;
        }
        _data = d;
        return _chart;
    };

    return _chart;
}