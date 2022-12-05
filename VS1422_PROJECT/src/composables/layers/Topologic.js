import * as d3 from 'd3';
import { color } from 'd3'; 
import L from 'leaflet';


const svg = d3.create('svg')
            .attr('viewBox', '0 0 925 550');
const bg_rect  = svg.append("rect")
                    .attr("fill", "white")
                    .attr("width", "100%")
                    .attr("height", "100%")
                    .attr("opacity", 0.8);
            
const g1 = svg.append("g")
            .attr("font-size", 10)
            .attr("font-family", "sans-serif")
            .attr("transform", "translate(467, 275)")
const g2 = svg.append("g").attr("fill-opacity", 0.75).attr("transform", "translate(467, 275)");


var last_view
var svgElementBounds = [ [20.1, 110.100], [19.5, 110.700] ];
var layer = L.svgOverlay(
    svg.node(), svgElementBounds, {
        opacity: 0.9,
        interactive: true,
    }
);


var innerRadius = 200;
var outerRadius = 220;

export function generate_layer(data, map) {
    last_view = {
        center: map.getCenter(),
        zoom: map.getZoom(),
    }

    return layer;
}


export function update_layer(data, map) {
    console.log("update_layer");
    map.setView([19.855845697571294, 110.39339405963088], 10);
    layer.setBounds(L.latLngBounds(
        L.latLng(19.500253226982274, 109.75753784179689),
        L.latLng(20.210656234489853, 111.02783203125001)
    ));
    console.log("map", map);
    console.log("layer", layer);
    console.log("svg", svg);

    const districts = new Set();

    const names = Array.from(new Set(data.flatMap(d => [d.source, d.target]))).sort(d3.ascending)

    const index = new Map(names.map((name, i) => [name, i]));
    const matrix = Array.from(index, () => new Array(names.length).fill(0));
    console.log("matrix", matrix);
    for (const {source, target, value} of data) {
        districts.add(source, target);
        matrix[index.get(source)][index.get(target)] += value;
    }

    console.log("districts", districts);

    const chord = d3.chordDirected()
                    .padAngle(10 / innerRadius)
                    .sortSubgroups(d3.descending)
                    .sortChords(d3.descending)

    const arc   = d3.arc()
                    .innerRadius(innerRadius)
                    .outerRadius(outerRadius)

    const ribbon = d3.ribbonArrow()
    .radius(innerRadius - 1)
    .padAngle(1 / innerRadius)

    const color = d3.scaleOrdinal(names, d3.quantize(d3.interpolateRainbow, names.length))


    const chords = chord(matrix);

    console.log(chords)

    const group = g1.selectAll("g")
                    .data(chords.groups)
                    .join("g");

    console.log("group",group);


    group.append("path")
        .attr("fill", d => color(names[d.index]))
        .attr("d", arc);

    group.append("text")
        .each(d => (d.angle = (d.startAngle + d.endAngle) / 2))
        .attr("dy", "0.35em")
        .attr("transform", d => `
            rotate(${(d.angle * 180 / Math.PI - 90)})
            translate(${outerRadius + 5})
            ${d.angle > Math.PI ? "rotate(180)" : ""}
        `)
        .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
        .text(d => names[d.index]);

    group.attr("id", d => `${names[d.index]}`);
    group.append("title")
        .text(d => `${names[d.index]}
    ${d3.sum(chords, c => (c.source.index === d.index) * c.source.value)} outgoing →
    ${d3.sum(chords, c => (c.target.index === d.index) * c.source.value)} incoming ←`);

    g2
        .selectAll("path")
        .data(chords)
        .join("path")
        .style("mix-blend-mode", "multiply")
        .attr("fill", d => color(names[d.target.index]))
        .attr("d", ribbon)
        .append("title")
        .text(d => `${names[d.source.index]} → ${names[d.target.index]} ${d.source.value}`);


}
