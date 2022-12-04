import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap'
import L from 'leaflet'
//import D3Wrapper from './d3/D3Wrapper.vue';

export function generate_layer(data,map) {
		// get color depending on population density value
		function getColor(d) {
			return d > 1000 ? '#800026' :
				d > 500  ? '#BD0026' :
				d > 200  ? '#E31A1C' :
				d > 100  ? '#FC4E2A' :
				d > 50   ? '#FD8D3C' :
				d > 20   ? '#FEB24C' :
				d > 10   ? '#FED976' : '#FFEDA0';
		}
	
		function style(feature) {
			return {
				weight: 2,
				opacity: 1,
				color: 'white',
				dashArray: '3',
				fillOpacity: 0.7,
				fillColor: getColor(feature.properties.density)
			};
		}
		
		// // control that shows state info on hover
		// const info = L.control();
		
		// info.onAdd = function (map) {
		// 	this._div = L.DomUtil.create('div', 'info');
		// 	this.update();
		// 	return this._div;
		// };
		
		// info.update = function (props) {
		// 	const contents = props ? `<b>${props.name}</b><br />${props.density} people / mi<sup>2</sup>` : 'Hover over a state';
		// 	this._div.innerHTML = `<h4>US Population Density</h4>${contents}`;
		// };
		// info.addTo(map);
		
		function highlightFeature(e) {
			const layer = e.target;
	
			layer.setStyle({
				weight: 5,
				color: '#666',
				dashArray: '',
				fillOpacity: 0.7
			});
	
			layer.bringToFront();
	
			//info.update(layer.feature.properties);
		}
		
		function resetHighlight(e) {
			geojson.resetStyle(e.target);
			//info.update();
		}
						
		function zoomToFeature(e) {
			map.fitBounds(e.target.getBounds());
		}
						
		function onEachFeature(feature, layer) {
			layer.on({
				mouseover: highlightFeature,
				mouseout: resetHighlight,
				click: zoomToFeature
			});
		}
	
		/* global data */
		const geojson = L.geoJson(data, {
			style,
			onEachFeature
		});
		
		return geojson;
}