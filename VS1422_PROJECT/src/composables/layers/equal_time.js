import L from 'leaflet'
import { computed, defineProps, onScopeDispose } from 'vue';
import * as d3 from 'd3';
import { select, svg } from 'd3';
import { equaltimeData } from '../../Global.vue';

const min_lat = 19.50;
const max_lat = 20.10;
const min_lng = 110.100;
const max_lng = 110.700;
const ViewBox = 1000;


var svgElement = d3.create('svg');
var g;
var svgElementBounds = [ [max_lat, min_lng], [min_lat, max_lng] ];
var scale_lat = d3.scaleLinear().domain([max_lat, min_lat]).range([0,ViewBox]);
var scale_lng = d3.scaleLinear().domain([min_lng, max_lng]).range([0,ViewBox]);
var k = ViewBox / (max_lat - min_lat);


export function generate_layer(data, map){
	svgElement.attr('viewBox', `0 0 ${ViewBox} ${ViewBox}`)

	var layer = L.svgOverlay(
		svgElement.node(), svgElementBounds, {
			opacity: 0.9,
			interactive: true,
		}
	);

	g = svgElement.append('g')
				  .attr('transform', `translate(${scale_lat(map.getCenter().lng)}, ${scale_lng(map.getCenter().lat)})`)
	
	var start_rad = Math.PI / 2;
	var delta_rad = 2 * Math.PI / data.length;
	g.selectAll('path')
			.data(data)
			.join("path")
			.attr("d", (d,i)=>{
				return d3.arc()
						.innerRadius(0)
						.outerRadius(d * k)
						.startAngle(start_rad - i * delta_rad)
						.endAngle(start_rad - (i + 1) * delta_rad)()
			})
			.attr('fill', "green")
			.attr('opacity',0.4)
			.attr('stroke-width',1)
			.attr('stroke','black')
			.attr('stroke-opacity',1.0)
	return layer;	
}

export async function update_layer(map, selected, dates, hours) {

	g.attr('transform', `translate(${scale_lng(selected[0])-2},${scale_lat(selected[1])-23})`);
	g.selectAll('path').attr('opacity',0);

	
	var data = await k_min_isochrone([10], [selected[0],selected[1]], dates, hours)

	var start_rad = Math.PI / 2;
	var delta_rad = 2 * Math.PI / data[0].length;
	g.selectAll('path')
			.data(data[0])
			.join("path")
			.attr("d", (d,i)=>{
				return d3.arc()
						.innerRadius(0)
						.outerRadius(d * k)
						.startAngle(start_rad - i * delta_rad)
						.endAngle(start_rad - (i + 1) * delta_rad)()
			})
			.attr('fill', "green")
			.attr('opacity',0.4)
			.attr('stroke-width',1)
			.attr('stroke','black')
			.attr('stroke-opacity',1.0)
}
