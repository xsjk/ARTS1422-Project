import * as d3 from 'd3';
import { color } from 'd3'; 
import L from 'leaflet';



var svg = d3.create('svg');
svg.attr('viewBox', '0 0 925 550');
var g;
var svgElementBounds = [ [20.1, 110.100], [19.5, 110.700] ];
var layer = L.svgOverlay(
    svg.node(), svgElementBounds, {
        opacity: 0.9,
        interactive: true,
    }
);

export function generate_layer(data,map) {
    console.log(map.getPixelBounds());
    layer.setBounds(map.getBounds());

    console.log(layer);

    // var lat_to_y = d3.scaleLinear().domain([map.getBounds()._southWest.lat, map.getBounds()._northEast.lat]).range([map.getPixelBounds().max.y, map.getPixelBounds().min.y]);
    // var lng_to_x = d3.scaleLinear().domain([map.getBounds()._southWest.lng, map.getBounds()._northEast.lng]).range([map.getPixelBounds().min.x, map.getPixelBounds().max.x]);
	

    // g = svg.append('g')
	// 				.attr('transform',`translate(${(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x) * Math.pow(2,(map.getZoom() - 10))}, ${(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y) * Math.pow(2,(map.getZoom() - 10))})`);


    
	// var k = (map.getPixelBounds().max.x -map.getPixelBounds().min.x) / (map.getBounds()._northEast.lng - map.getBounds()._southWest.lng);
	// var start_rad = Math.PI / 2;
	// var delta_rad = 2 * Math.PI / data.length;
	// g.selectAll('path')
	// 		.data(data)
	// 		.join("path")
	// 		.attr("d", (d,i)=>{
	// 			return d3.arc()
	// 					.innerRadius(0)
	// 					.outerRadius(d * k)
	// 					.startAngle(start_rad - i * delta_rad)
	// 					.endAngle(start_rad - (i + 1) * delta_rad)()
	// 		})
	// 		.attr('fill', "green")
	// 		.attr('opacity',0.4)
	// 		.attr('stroke-width',1)
	// 		.attr('stroke','black')
	// 		.attr('stroke-opacity',1.0)
	// return layer;	



    innerRadius = 100;


    const names = Array.from(new Set(data.flatMap(d => [d.source, d.target]))).sort(d3.ascending)

    const index = new Map(names.map((name, i) => [name, i]));
    const matrix = Array.from(index, () => new Array(names.length).fill(0));
    for (const {source, target, value} of data) matrix[index.get(source)][index.get(target)] += value;

    const chord = d3.chordDirected()
    .padAngle(10 / innerRadius)
    .sortSubgroups(d3.descending)
    .sortChords(d3.descending)

    const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius)

    const ribbon = d3.ribbonArrow()
    .radius(innerRadius - 1)
    .padAngle(1 / innerRadius)

    const color = d3.scaleOrdinal(names, d3.quantize(d3.interpolateRainbow, names.length))

    
    const svg = d3.create("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height]);

    const chords = chord(matrix);

    const group = svg.append("g")
        .attr("font-size", 10)
        .attr("font-family", "sans-serif")
        .selectAll("g")
        .data(chords.groups)
        .join("g");

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

    group.append("title")
        .text(d => `${names[d.index]}
    ${d3.sum(chords, c => (c.source.index === d.index) * c.source.value)} outgoing →
    ${d3.sum(chords, c => (c.target.index === d.index) * c.source.value)} incoming ←`);

    svg.append("g")
        .attr("fill-opacity", 0.75)
        .selectAll("path")
        .data(chords)
        .join("path")
        .style("mix-blend-mode", "multiply")
        .attr("fill", d => color(names[d.target.index]))
        .attr("d", ribbon)
        .append("title")
        .text(d => `${names[d.source.index]} → ${names[d.target.index]} ${d.source.value}`);


    return svg.node();
}



export function update_layer(data, map) {
    // console.log(map);
	// // console.log(map.getBounds());
	// // console.log(map.getPixelBounds());
	// console.log(map.getCenter());
	// var lat_to_y = d3.scaleLinear().domain([map.getBounds()._southWest.lat, map.getBounds()._northEast.lat]).range([map.getPixelBounds().max.y, map.getPixelBounds().min.y]);
	// var lng_to_x = d3.scaleLinear().domain([map.getBounds()._southWest.lng, map.getBounds()._northEast.lng]).range([map.getPixelBounds().min.x, map.getPixelBounds().max.x]);
	// console.log(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x);
	// console.log(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y);
	// g.attr('transform',`translate(${(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x) * Math.pow(2,(map.getZoom() - 10))}, ${(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y)* Math.pow(2,(map.getZoom() - 10))})`);
	// var k = (map.getPixelBounds().max.x -map.getPixelBounds().min.x) / (map.getBounds()._northEast.lng - map.getBounds()._southWest.lng);
	// var start_rad = Math.PI / 2;
	// var delta_rad = 2 * Math.PI / data.length;
	// g.selectAll('path')
	// 		.data(data)
	// 		.join("path")
	// 		.attr("d", (d,i)=>{
	// 			return d3.arc()
	// 					.innerRadius(0)
	// 					.outerRadius(d * k)
	// 					.startAngle(start_rad - i * delta_rad)
	// 					.endAngle(start_rad - (i + 1) * delta_rad)()
	// 		})
	// 		.attr('fill', "green")
	// 		.attr('opacity',0.4)
	// 		.attr('stroke-width',1)
	// 		.attr('stroke','black')
	// 		.attr('stroke-opacity',1.0)

}
