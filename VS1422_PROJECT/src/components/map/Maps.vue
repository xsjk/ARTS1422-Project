<script>

import { ref } from 'vue'
export const center = ref([110.355043, 20.004658]);
export const scale = ref(10);
export const selected = ref([]);

</script>

<script setup>
	import * as HeatMapIn from '../../composables/layers/heatmap_in';
	import * as HeatMapOut from '../../composables/layers/heatmap_out';
	import * as DistrictMap from '../../composables/layers/district_division'
	import * as EqualTimeMap from '../../composables/layers/equal_time'
	import * as TopologicMap from '../../composables/layers/topologic'
	import { watch } from 'vue';
	import { hours, dates } from '../d3/Calendar.vue';

	import * as d3 from 'd3';
	import L from 'leaflet';

	import { weatherData, timemapData, equaltimeData, topologicData } from '../../Global.vue';

	const props = defineProps({
	  date: {
		type: Array,
		required: true,
	  },
	  time: {
		type: Array,
		required: true,
	  },
	  center: {
		type: Array,
		required: true,
	  },
	  scale:{
		type: [Number, String],
		default: null, 
	  }
	});


	// 用来获取数据的组合
	const getData = async () => {
		const weatherTest = await d3.csv('weatherData.csv');
		weatherData.value = weatherTest.map(d => d);
		timemapData.value = await traffic_flow_in_degree_graph([46010608]);
		equaltimeData.value = [0.028758452380954324, 0.02031264526842589, 0.03360677895017247, 0.04200094409784688, 0.03459567830588102, 0.0, 0.0, 0.0, 0.0, 0.025049999999993133, 0.03703024779237924, 0.05582818807481003, 0.028591562079811773, 0.02556251189854171, 0.020557370556213986, 0.04941435904157133, 0.06827150819941265, 0.03244533622005591];
		topologicData.value = [
			{"source":"analytics.cluster","target":"animate","value":2},
			{"source":"analytics.cluster","target":"vis.data","value":8},
			{"source":"analytics.cluster","target":"util.math","value":2},
			{"source":"analytics.cluster","target":"analytics.cluster","value":5},
			{"source":"analytics.cluster","target":"util","value":3},
			{"source":"analytics.cluster","target":"vis.operator","value":1},
			{"source":"analytics.graph","target":"animate","value":5},
			{"source":"analytics.graph","target":"vis.data","value":14},
			{"source":"analytics.graph","target":"util","value":5},
			{"source":"analytics.graph","target":"vis.operator","value":6},
			{"source":"analytics.graph","target":"analytics.graph","value":1},
			{"source":"analytics.graph","target":"util.heap","value":2},
			{"source":"analytics.graph","target":"vis","value":1},
			{"source":"analytics.optimization","target":"animate","value":1},
			{"source":"analytics.optimization","target":"util","value":2},
			{"source":"analytics.optimization","target":"vis.data","value":1},
			{"source":"analytics.optimization","target":"scale","value":1},
			{"source":"analytics.optimization","target":"vis.axis","value":1},
			{"source":"analytics.optimization","target":"vis","value":1},
			{"source":"analytics.optimization","target":"vis.operator","value":1},
			{"source":"animate","target":"animate","value":30},
			{"source":"animate","target":"util","value":9},
			{"source":"animate.interpolate","target":"util","value":2},
			{"source":"animate.interpolate","target":"animate.interpolate","value":16},
			{"source":"animate","target":"animate.interpolate","value":1},
			{"source":"data.converters","target":"data.converters","value":7},
			{"source":"data.converters","target":"data","value":17},
			{"source":"data.converters","target":"util","value":1},
			{"source":"data","target":"data","value":7},
			{"source":"data","target":"util","value":1},
			{"source":"data","target":"data.converters","value":2},
			{"source":"display","target":"display","value":3},
			{"source":"display","target":"util","value":1},
			{"source":"flex","target":"display","value":1},
			{"source":"flex","target":"data","value":1},
			{"source":"flex","target":"vis","value":1},
			{"source":"flex","target":"vis.axis","value":2},
			{"source":"flex","target":"vis.data","value":1},
			{"source":"physics","target":"physics","value":22},
			{"source":"query","target":"query","value":61},
			{"source":"query","target":"util","value":6},
			{"source":"query.methods","target":"query.methods","value":39},
			{"source":"query.methods","target":"query","value":32},
			{"source":"scale","target":"scale","value":19},
			{"source":"scale","target":"util","value":14},
			{"source":"util","target":"util","value":23},
			{"source":"util.heap","target":"util.heap","value":2},
			{"source":"util.math","target":"util.math","value":2},
			{"source":"util.palette","target":"util.palette","value":3},
			{"source":"util.palette","target":"util","value":2},
			{"source":"vis.axis","target":"animate","value":3},
			{"source":"vis.axis","target":"vis","value":2},
			{"source":"vis.axis","target":"scale","value":4},
			{"source":"vis.axis","target":"util","value":3},
			{"source":"vis.axis","target":"display","value":5},
			{"source":"vis.axis","target":"vis.axis","value":7},
			{"source":"vis.controls","target":"vis.controls","value":12},
			{"source":"vis.controls","target":"vis","value":3},
			{"source":"vis.controls","target":"vis.operator.layout","value":1},
			{"source":"vis.controls","target":"vis.events","value":4},
			{"source":"vis.controls","target":"util","value":3},
			{"source":"vis.controls","target":"vis.data","value":2},
			{"source":"vis.controls","target":"animate","value":2},
			{"source":"vis.controls","target":"display","value":1},
			{"source":"vis.data","target":"vis.data","value":26},
			{"source":"vis.data","target":"util","value":17},
			{"source":"vis.data","target":"vis.events","value":4},
			{"source":"vis.data","target":"data","value":3},
			{"source":"vis.data","target":"animate","value":2},
			{"source":"vis.data","target":"util.math","value":2},
			{"source":"vis.data","target":"display","value":1},
			{"source":"vis.data","target":"vis.data.render","value":4},
			{"source":"vis.data.render","target":"vis.data","value":5},
			{"source":"vis.data.render","target":"vis.data.render","value":3},
			{"source":"vis.data.render","target":"util","value":3},
			{"source":"vis.data","target":"scale","value":9},
			{"source":"vis.data","target":"util.heap","value":2},
			{"source":"vis.events","target":"vis.data","value":6},
			{"source":"vis.events","target":"vis.events","value":1},
			{"source":"vis.events","target":"animate","value":1},
			{"source":"vis.legend","target":"animate","value":1},
			{"source":"vis.legend","target":"vis.data","value":1},
			{"source":"vis.legend","target":"util.palette","value":5},
			{"source":"vis.legend","target":"scale","value":4},
			{"source":"vis.legend","target":"vis.legend","value":4},
			{"source":"vis.legend","target":"display","value":6},
			{"source":"vis.legend","target":"util","value":6},
			{"source":"vis.operator.distortion","target":"vis.operator.distortion","value":2},
			{"source":"vis.operator.distortion","target":"animate","value":1},
			{"source":"vis.operator.distortion","target":"vis.data","value":2},
			{"source":"vis.operator.distortion","target":"vis.events","value":1},
			{"source":"vis.operator.distortion","target":"vis.axis","value":2},
			{"source":"vis.operator.distortion","target":"vis.operator.layout","value":1},
			{"source":"vis.operator.encoder","target":"animate","value":3},
			{"source":"vis.operator.encoder","target":"scale","value":3},
			{"source":"vis.operator.encoder","target":"vis.operator.encoder","value":4},
			{"source":"vis.operator.encoder","target":"util.palette","value":7},
			{"source":"vis.operator.encoder","target":"vis.data","value":8},
			{"source":"vis.operator.encoder","target":"vis.operator","value":2},
			{"source":"vis.operator.encoder","target":"util","value":3},
			{"source":"vis.operator.filter","target":"animate","value":3},
			{"source":"vis.operator.filter","target":"vis.data","value":10},
			{"source":"vis.operator.filter","target":"vis.operator","value":3},
			{"source":"vis.operator.filter","target":"util","value":1},
			{"source":"vis.operator","target":"animate","value":7},
			{"source":"vis.operator","target":"vis","value":3},
			{"source":"vis.operator","target":"vis.operator","value":11},
			{"source":"vis.operator.label","target":"animate","value":1},
			{"source":"vis.operator.label","target":"vis.data","value":6},
			{"source":"vis.operator.label","target":"display","value":3},
			{"source":"vis.operator.label","target":"vis.operator","value":1},
			{"source":"vis.operator.label","target":"util","value":5},
			{"source":"vis.operator.label","target":"vis.operator.label","value":2},
			{"source":"vis.operator.layout","target":"scale","value":6},
			{"source":"vis.operator.layout","target":"vis.data","value":34},
			{"source":"vis.operator.layout","target":"vis.axis","value":4},
			{"source":"vis.operator.layout","target":"util","value":20},
			{"source":"vis.operator.layout","target":"vis.operator.layout","value":14},
			{"source":"vis.operator.layout","target":"animate","value":6},
			{"source":"vis.operator.layout","target":"vis.operator","value":2},
			{"source":"vis.operator.layout","target":"vis.data.render","value":1},
			{"source":"vis.operator.layout","target":"physics","value":3},
			{"source":"vis.operator.layout","target":"vis","value":1},
			{"source":"vis.operator","target":"util","value":5},
			{"source":"vis.operator","target":"vis.data","value":1},
			{"source":"vis","target":"animate","value":3},
			{"source":"vis","target":"vis.operator","value":2},
			{"source":"vis","target":"vis.events","value":2},
			{"source":"vis","target":"vis.data","value":2},
			{"source":"vis","target":"vis.axis","value":2},
			{"source":"vis","target":"util","value":1},
			{"source":"vis","target":"vis.controls","value":1}];

	};
	getData()

	var testData = {
	  max: 0,
	  data: []
	};



	/// layers
	

	const mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
	const mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
	const streets = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	const dark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	});
	const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'});
	const satellite = L.tileLayer(mbUrl, {id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	const baseLayers = {
		'Basemap': osm,
		'Streets': streets,
		'Dark': dark,
		'Satellite': satellite
	};
	
	let heatmapinLayer = HeatMapIn.generate_layer(testData);
		heatmapinLayer.cfg.radius = 0.001;
	let heatmapoutLayer = HeatMapOut.generate_layer(testData);
		heatmapoutLayer.cfg.radius = 0.001;
	heatmapinLayer.on("add",function(){
		HeatMapIn.update_layer(dates.value, hours.value, center.value, scale.value);
	})
	const map = L.map('map', {
		center: [center.value[1], center.value[0]],
		zoom: scale.value,
		renderer: L.svg(),
		attributionControl:false,
		layers: [streets]
	})

	let districtLayer = DistrictMap.generate_layer(data, map);
	let equaltimeLayer = EqualTimeMap.generate_layer(equaltimeData.value, map);
	let topologicLayer = TopologicMap.generate_layer(topologicData.value, map);


	
	// 给所有图层添加add时的自动更新
	heatmapoutLayer.on("add",function(){
		console.log("HeatMapOut Loaded");
		HeatMapOut.update_layer(dates.value, hours.value, center.value, scale.value);
	})
	equaltimeLayer.on("add",function(){
		console.log("equalTime Loaded");
		if (selected.value == undefined || selected.value.length == 0){
			selected.value = center.value;
		}
		//EqualTimeMap.update_layer(dates.value, hours.value, selected.value, map);
		EqualTimeMap.generate_selection(map);
	})
	equaltimeLayer.on("remove",function(){
		console.log("equalTime Removed");
		EqualTimeMap.remove_selection(map);
	})
	topologicLayer.on("add",function(){
		console.log("toplogic Loaded");
		console.log(topologicData.value);
		TopologicMap.update_layer(topologicData.value,map);
	})

	
	var marker = L.marker(center.value);
	marker.addTo(map);
	map.on('click', async(e) => {
		//console.log(e);
		var popup = L.popup()
			.setContent(marker)
			.setLatLng(e.latlng)
			.setContent(`${e.latlng.toString()}`)
			// .openOn(map);
		marker.setLatLng(e.latlng);
		marker.bindPopup(popup).openPopup();
		//marker.bindPopup(Popup);
		selected.value = [e.latlng.lng, e.latlng.lat];
		center.value = [e.latlng.lng, e.latlng.lat];
	});


	map.on('zoomend', async(e) => {
		scale.value = e.target.getZoom();
	});

	map.on('mouseup', async(e) => {
		//var center = e.target.getCenter();
		//center.value = [e.target.getCenter().lng, e.target.getCenter().lat];
	});


	/// control
	L.control.scale({ maxWidth: 200, metric: true, imperial: false }).addTo(map)
	let mixed = {
		'HeatMapInLayer': heatmapinLayer,
		'HeatMapOutLayer': heatmapoutLayer,
		'equaltimeLayer': equaltimeLayer,
		'topologicalLayer': topologicLayer,
	}
	const controller = L.control.layers(baseLayers, mixed).addTo(map);
	districtLayer.addTo(map);
	// watch
	watch(
		[hours, dates, center, scale],
		async () => {                                                                                                      
			if(!map.hasLayer(heatmapoutLayer)){
			  //console.log("HeatMapOut不需要更新")
			  return;
			} 
			//console.log("HeatMapOut需要更新")
			HeatMapOut.update_layer(dates.value, hours.value, center.value, scale.value);
		},
		{ deep: true }
	);
	
	watch(
		[hours, dates, center, scale],
		async () => {                                                                                                      
			if(!map.hasLayer(heatmapinLayer)){
			  //console.log("HeatMapIn不需要更新")
			  return;
			} 
			//console.log("HeatMapIn需要更新")
			HeatMapIn.update_layer(dates.value, hours.value, center.value, scale.value);
		},
		{ deep: true }
	);

	watch(
		[hours, dates, selected],
		async () => {
			if(!map.hasLayer(equaltimeLayer)){
			  //console.log("EqualTimeMap不需要更新")
			  return;
			} 
			//console.log("EqualTimeMap需要更新")
			//EqualTimeMap.update_layer(map,selected.value,dates.value,hours.value);
		},
		{ deep: true }
	)



</script>


<template>
	<!-- <div id="map"></div> -->
</template>

<style>
</style>