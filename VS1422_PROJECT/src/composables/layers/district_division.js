import L from 'leaflet'
import * as d3 from 'd3';
//import D3Wrapper from './d3/D3Wrapper.vue';

var lastSelection;

var selected = undefined; //a reference
var can_move;

export function generate_layer(data, map, s, c) {
	can_move = c
	selected = s;
	// get color depending on population density value
	function getColor(d) {
		return d > 1000 ? '#800026' :
			d > 500  ? '#BD0026' :
			d > 200  ? '#E31A1C' :
			d > 100  ? '#FC4E2A' :
			d > 50   ? '#FD8D3C' :
			d > 20   ? '#FEB24C' :
			d > 10   ? '#FED976' : 'lightblue';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 0.1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.2,
			fillColor: getColor(feature.properties.density)
		};
	}

	// control that shows state info on hover
	const info = L.control.scale({
		position:'bottomright',
		maxWidth:'100',
		imperial:true
	});

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		var texts = props ? `<b>${props.name}</b><br />${props.density} 流量` : 'Hover over a state';
		const contents = texts.bold().fontsize(5);
		this._div.innerHTML = `${contents}`;

	};
	info.addTo(map);

	function highlightFeature(e) {
		const layer = e.target;
		d3.select(`#${layer.feature.properties['name']} > path`)
			.attr('stroke-width',4)
			.attr('stroke','red')

		layer.setStyle({
			weight: 5,
			color: '#663408',
			opacity:0.7,
			dashArray: '',
			//fillOpacity: 0.7
		});
		layer.bringToFront();
		info.update(layer.feature.properties);
	}

	function resetHighlight(e) {
		if(e.target != lastSelection) geojson.resetStyle(e.target);
		d3.select(`#${e.target.feature.properties['name']} > path`)
			.attr('stroke-width',0)
		info.update();
	}

	function onClick(e) {
		selected.value = [
			district_ids[district_names.indexOf(e.target.feature.properties['name'])]
		];
		// if (!can_move.value)
		// 	return;
		if(lastSelection == e.target){
			geojson.resetStyle(lastSelection);
			lastSelection = null;
			return;
		}
		if(lastSelection != null){
			geojson.resetStyle(lastSelection);
		}
		// map.flyTo(e.target.getCenter(),10);
		lastSelection = e.target;
		lastSelection.setStyle({
			weight: 10,
			dashArray: '',
			fillColor: '#663408',
			fillOpacity: 0.7
		});
	}

	function onDoubleClick(e) {
		console.log('double click');
		selected.value = [
			district_ids[district_names.indexOf(e.target.feature.properties['name'])]
		];
		if (!can_move.value)
			return;
		if(lastSelection == e.target){
			geojson.resetStyle(lastSelection);
			lastSelection = null;
			return;
		}
		if(lastSelection != null){
			geojson.resetStyle(lastSelection);
		}
		map.flyTo(e.target.getCenter());
		lastSelection = e.target;
		lastSelection.setStyle({
			weight: 10,
			dashArray: '',
			fillColor: '#663408',
			fillOpacity: 0.7
		});
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: onClick,
			// dblclick: onDoubleClick
		});
	}

	/* global data */
	const geojson = L.geoJson(data, {
		style,
		onEachFeature
	});

	console.log('geojson',geojson);

	return geojson;
}
