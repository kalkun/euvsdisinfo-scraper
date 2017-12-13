import React from 'react';
import * as d3 from 'd3';
import SVG from 'react-inlinesvg';
import $ from 'jquery';


function getVal(txt) {
    var match = txt.match(/[0-9]+$/)
    if (match) {
        return +match[0];
    } else {
        return 0;
    }
}


function hideSmallLabels() {
  $("svg g.cell").each(function(index, item) {
      var val = getVal($(item).children("title").text())
      if (val < 10) {
          $(item).children("text").attr("style", "display:none;")
      }
  })
  
}

function langOutlet(props) {
    return <SVG
      src='langThenOutletNumArticles.svg'
      onLoad={() => hideSmallLabels()}
    ></SVG>;
}

/*
}
    TreeMap accepts a dataset and visualize it as a treemap,
    see: https://bl.ocks.org/mbostock/4063582
*/
function fromData(props) {
    console.log("TreeMap called", props);
    const svg = d3.select("svg"),
        // width = +svg.attr("width"),
        // height = +svg.attr("height");
        width = 1200,
        height = 600;

    svg.selectAll("g").remove();

    const fader = function(color) { return d3.interpolateRgb(color, "#fff")(0.2); },
        color = d3.scaleOrdinal(d3.schemeCategory20.map(fader)),
        format = d3.format(",d");

    const treemap = d3.treemap()
        .tile(d3.treemapResquarify)
        .size([width, height])
        .round(true)
        .paddingInner(1);

    // d3.json("flare.json", function(error, data) {
    //   if (error) throw error;

    const data = props
    const byName = props['byName'];

    const root = d3.hierarchy(data, d => d.values)
      .eachBefore(function(d) { d.data.id = (d.parent ? d.parent.data.key + "." : "") + d.data.key; })
      .sum(props.sizeBy === 'likes' ? sumBySize : sumByCount)
      .sort(function(a, b) { return b.height - a.height || b.value - a.value; });
    console.log(root);
    treemap(root);

    const cell = svg.selectAll("g")
    .data(root.leaves())
    .enter().append("g")
      .attr("transform", function(d) { return "translate(" + d.x0 + "," + d.y0 + ")"; });

    cell.append("rect")
      .attr("id", function(d) { return d.data.id; })
      .attr("width", function(d) { return d.x1 - d.x0; })
      .attr("height", function(d) { return d.y1 - d.y0; })
      .attr("fill", function(d) { return color(d.parent.data.id); });

    cell.append("clipPath")
      .attr("id", function(d) { return "clip-" + d.data.id; })
    .append("use")
      .attr("xlink:href", function(d) { return "#" + d.data.id; });

    cell.append("text")
      .attr('dy', "20")
      // .text(d =>  d.value > 100000 ? (byName ? d.data[byName] : d.data.outlet) : '')
      .text(d => {
        if (props.sizeBy === 'likes') {
          return d.value > 100000 ? (byName ? d.data[byName] : d.data.outlet) : '';
        } else if (d.value > 50) {
          return d.data.key;
        }
      })

    cell.append("title")
      .text(d => {
        if (d.data.hasOwnProperty("outlet")) {
          return "Outlet:\t\t" + d.data.outlet + "\nlanguage:\t\t" + d.data.language + "\nlikes:\t\t\t" + d.value + "\nreported by:\t" + d.data['reported by'] + "\ntitle:\t\t\t" + d.data.title
        } else {
          return d.parent.data.key + "\nkey:\t" + d.data.key + "\nvalue:\t" + d.value;
        }})

    d3.selectAll("input")
      .data([sumBySize, sumByCount], function(d) { return d ? d.name : this.value; })
      .on("change", changed);

    const timeout = d3.timeout(function() {
    d3.select("input[value=\"sumByCount\"]")
        .property("checked", true)
        .dispatch("change");
    }, 2000);

    function changed(sum) {
    timeout.stop();

    treemap(root.sum(sum));

    cell.transition()
        .duration(750)
        .attr("transform", function(d) { return "translate(" + d.x0 + "," + d.y0 + ")"; })
      .select("rect")
        .attr("width", function(d) { return d.x1 - d.x0; })
        .attr("height", function(d) { return d.y1 - d.y0; });
    }

    function sumByCount(d) {
      return d.value || 1//s ? 0 : 1;
      // return +d.values;
    }

    function sumBySize(d) {
      return +d.likes;
    }

    return <div>
      
    </div>
}



export {
  langOutlet,
  fromData
}