import L from 'leaflet'
import { computed, defineProps, onScopeDispose } from 'vue';
import * as d3 from 'd3';
import { geoConicConformal, select, svg } from 'd3';
import { equaltimeData } from '../../Global.vue';

const min_lat = 19.50;
const max_lat = 20.10;
const min_lng = 110.100;
const max_lng = 110.700;
const ViewBox = 1000;
const r = 400;
const to_rad =  Math.PI / 180;

var svgElement = d3.create('svg');
var g;
var svgElementBounds = [ [max_lat, min_lng], [min_lat, max_lng] ];
var scale_lat = d3.scaleLinear().domain([max_lat, min_lat]).range([0,ViewBox]);
var scale_lng = d3.scaleLinear().domain([min_lng, max_lng]).range([0,ViewBox]);
var k = ViewBox / (max_lat - min_lat);

// control that shows state info on hover
const selection = L.control.scale({
	position:'bottomleft',
	maxWidth:'100',
	imperial:true
});

export function generate_layer(data, map){
	//data
	svgElement.attr('viewBox', `0 0 ${ViewBox} ${ViewBox}`);

	var layer = L.svgOverlay(
		svgElement.node(), svgElementBounds, {
			opacity: 0.9,
			interactive: true,
		}
	);

	g = svgElement.append('g')
				  .attr('transform', `translate(${scale_lat(map.getCenter().lng)}, ${scale_lng(map.getCenter().lat)})`)

	return layer;
}

const tenMinColor = "red", thirtyMinColor = "#F76809", sixtyMinColor = "#32CD32";

const X = [0,1,2]
const Y = [10,20,30]
const colors = [tenMinColor, thirtyMinColor, sixtyMinColor]
const cell_height = 50;
const cell_width = 50;

export async function update_layer(map, selected, dates, hours, distance) {
	g.attr('transform', `translate(${scale_lng(selected[0])-2},${scale_lat(selected[1])-23})`);
	g.selectAll('path').attr('opacity',0);
	g.selectAll('polygon').attr('opacity',0);
	const colors = {10:tenMinColor,20:thirtyMinColor,30:sixtyMinColor}
	var data = await k_min_isochrone_by_departure_time([distance], [selected[0],selected[1]], dates, hours);
	if (!data) {
		// alert('No data available for the selected time range');
		return;
	}
	var delta_rad = 2 * Math.PI / data[0][0].length;
	var start_rad = Math.PI / 2 + delta_rad / 2;
	g.selectAll('path')
			.data(data[0][0])
			.join("path")
			.attr("d", (d,i)=>{
				return d3.arc()
						.innerRadius(d * k * 0.95)
						.outerRadius(d * k * 1.05)
						.startAngle(start_rad - i * delta_rad)
						.endAngle(start_rad - (i + 1) * delta_rad)()
			})
			.attr('fill', colors[distance])
			.attr('opacity',0.4)
			.attr('stroke-width',1)
			.attr('stroke','black')
			.attr('stroke-opacity',1.0)

	g.selectAll('polygon')
	.data(data[0][1])
	.join('polygon')
	.attr('points',(d,i)=>{return `0,0 ${d*r*Math.cos(10*to_rad)},0 ${d*r*(Math.cos(10*to_rad))},${d*r*Math.sin(10*to_rad)} ${d*r*(Math.cos(10*to_rad)+0.05)},${d*r*Math.sin(10*to_rad)} ${d*r*(Math.cos(10*to_rad)+0.05)},${-d*r*Math.sin(10*to_rad)} ${d*r*(Math.cos(10*to_rad))},${-d*r*Math.sin(10*to_rad)} ${d*r*Math.cos(10*to_rad)},0 0,0`})
	.attr('transform',(d,i)=>{return `rotate(${-i*20})`})
	.attr('fill','black')
	.attr('opacity',0.7)
	.attr('stroke-width',1)
	.attr('stroke','black')
	.attr('stroke-opacity',1.0)


	// g.selectAll('title')
	// 		.data(data[0][1])
	// 		.join('title')
	// 		.text((d)=>{
	// 			return `${d*100}%`
	// 		})
}

export function generate_selection(map,distance){
	const svg = d3.create("svg")
				.attr("id", "selection")
				.attr("width",cell_width)
				.attr("height",3*cell_height);
	const cells = svg.append("g")
				.selectAll("rect")
				.data(X)
				.join("rect")
					.attr('class','Equal_rects')
					.attr("x",0)
					.attr("y",d=> d*cell_height)
					.attr("height", cell_height)
					.attr("width", cell_width)
					.attr("fill", "white")
					.attr("selected",d => d==0 ? true:false)
				.on("mouseover",function(data,d){
					distance.value = Y[d];
					svg.selectAll("rect")
					.attr("selected",false);
					d3.select(this).attr("selected",true);
					})
				.on("click", (e)=>{});
	const texts = svg.append("g")
					.selectAll("Equal_texts")
					.data(X)
					.join("text")
						.attr('class','Equal_texts')
						.attr("x",cell_width/2)
						.attr("y",d=> cell_height/2+d*cell_height+5)
						.text(d=>Y[d]);
	selection.onAdd = function (map) {
		this._div = L.DomUtil.get(svg.node());
		return this._div;
	};
	selection.addTo(map);
}

export function remove_selection(map){
	console.log(selection);
	selection.remove();
	//selection.removeFrom(map);
}
