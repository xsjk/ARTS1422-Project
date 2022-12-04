import L from 'leaflet'
import { computed, defineProps, onScopeDispose } from 'vue';
import * as d3 from 'd3';
import { equaltimeData } from '../../Global.vue';

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

export function generate_layer(data,map){
	console.log(map.getCenter());
	
	layer.setBounds(map.getBounds());
	// console.log(map.getBounds());
	// console.log(map.getPixelBounds());
	var lat_to_y = d3.scaleLinear().domain([map.getBounds()._southWest.lat, map.getBounds()._northEast.lat]).range([map.getPixelBounds().max.y, map.getPixelBounds().min.y]);
	var lng_to_x = d3.scaleLinear().domain([map.getBounds()._southWest.lng, map.getBounds()._northEast.lng]).range([map.getPixelBounds().min.x, map.getPixelBounds().max.x]);
	// console.log(lat_to_y(map.getCenter().lat) - map.getPixelBounds().min.y);
	// console.log(lng_to_x(map.getCenter().lng) - map.getPixelBounds().min.x);
	
	g = svg.append('g')
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

export async function update_layer(dates, hours, selected, map) {
	console.log('selected', selected);
	layer.setBounds(map.getBounds());
	// console.log('k_min_isochrone('+[10]+','+map.getCenter()+','+dates+','+hours+')');
	equaltimeData.value = (await k_min_isochrone([10], selected, dates, hours))
	// console.log(equaltimeData.value);
	equaltimeData.value = equaltimeData.value[0]
	//data = equaltimeData.value;
	//console.log(map);
	// console.log(map.getBounds());
	// console.log(map.getPixelBounds());
	//console.log(map.getCenter());
	const p = map.latLngToLayerPoint(L.latLng(selected[1], selected[0]));
	console.log('p', p);
	g.attr('transform',`translate(${p.x}, ${p.y})`);
	var k = (map.getPixelBounds().max.x -map.getPixelBounds().min.x) / (map.getBounds()._northEast.lng - map.getBounds()._southWest.lng);
	var start_rad = Math.PI / 2;
	var delta_rad = 2 * Math.PI / equaltimeData.value.length;
	g.selectAll('path')
			.data(equaltimeData.value)
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
