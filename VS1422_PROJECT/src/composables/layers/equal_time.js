
import L from 'leaflet'
import { computed, defineProps, onScopeDispose } from 'vue';
import * as d3 from 'd3';
import { svg } from 'd3';

var svgElement = d3.create('svg');
var g;
var svgElementBounds = [ [20.1, 110.100], [19.5, 110.700] ];


export function generate_layer(data,map){
	console.log(map.getCenter());
	var layer = L.svgOverlay(
		svgElement.node(), svgElementBounds, {
			opacity: 0.9,
			interactive: true,
		}
	);
	layer.setBounds(map.getBounds());
	// console.log(map.getBounds());
	// console.log(map.getPixelBounds());
	var lat_to_y = d3.scaleLinear().domain([map.getBounds()._southWest.lat, map.getBounds()._northEast.lat]).range([map.getPixelBounds().max.y, map.getPixelBounds().min.y]);
	var lng_to_x = d3.scaleLinear().domain([map.getBounds()._southWest.lng, map.getBounds()._northEast.lng]).range([map.getPixelBounds().min.x, map.getPixelBounds().max.x]);
	// console.log(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y);
	// console.log(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x);
	
	g = svgElement.append('g')
					.attr('transform',`translate(${(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x) * Math.pow(2,(map.getZoom() - 10))}, ${(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y) * Math.pow(2,(map.getZoom() - 10))})`);



	var k = (map.getPixelBounds().max.x -map.getPixelBounds().min.x) / (map.getBounds()._northEast.lng - map.getBounds()._southWest.lng);
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

export function update_layer(data, map) {
	console.log(map);
	// console.log(map.getBounds());
	// console.log(map.getPixelBounds());
	console.log(map.getCenter());
	var lat_to_y = d3.scaleLinear().domain([map.getBounds()._southWest.lat, map.getBounds()._northEast.lat]).range([map.getPixelBounds().max.y, map.getPixelBounds().min.y]);
	var lng_to_x = d3.scaleLinear().domain([map.getBounds()._southWest.lng, map.getBounds()._northEast.lng]).range([map.getPixelBounds().min.x, map.getPixelBounds().max.x]);
	console.log(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x);
	console.log(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y);
	g.attr('transform',`translate(${(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x) * Math.pow(2,(map.getZoom() - 10))}, ${(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y)* Math.pow(2,(map.getZoom() - 10))})`);
	var k = (map.getPixelBounds().max.x -map.getPixelBounds().min.x) / (map.getBounds()._northEast.lng - map.getBounds()._southWest.lng);
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
}
