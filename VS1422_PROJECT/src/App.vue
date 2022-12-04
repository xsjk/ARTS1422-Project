<script setup>
<<<<<<< HEAD
	//import Heatmap from './components/map/heatmap.vue'
	import Districtmap from './components/map/district_division.vue'
	import Calendar from './components/d3/Calendar.vue'
	import MapUpdate from './components/map/AllMaps.vue'
	import {generate_layer, update_layer} from './composables/maps/heatmap.js'
	import {SelectedDate,SelectedTime,SetPosition} from './composables/d3/calendar/calendar.jsx'
=======

	import Calendar from './components/d3/Calendar.vue'
	import TimeMap from './components/d3/Timemap.vue'
>>>>>>> f34f06f323abd5c29364f9a28a2a5122b6edbffc
	import Title from './components/d3/Title.vue'
	import Maps from './components/map/Maps.vue'

	import * as d3 from 'd3';
	import { weatherData, timemapData, equaltimeData } from './Global.vue';
	
	
<<<<<<< HEAD
	const cityScheme = discreteScheme(42, 42).reverse();
	const newdata = ref([]);
	const weatherData = ref([]);
		
	// 用来获取数据的组合
=======
	console.log(timemapData);

	// // 用来获取数据的组合
>>>>>>> f34f06f323abd5c29364f9a28a2a5122b6edbffc
	const getData = async () => {
	  const weatherTest = await d3.csv('weatherData.csv');
	  weatherData.value = weatherTest.map(d => d);
	  timemapData.value = [[0.1,0.2],[0.3,0.4]];
	  equaltimeData.value = [0.028758452380954324, 0.02031264526842589, 0.03360677895017247, 0.04200094409784688, 0.03459567830588102, 0.0, 0.0, 0.0, 0.0, 0.025049999999993133, 0.03703024779237924, 0.05582818807481003, 0.028591562079811773, 0.02556251189854171, 0.020557370556213986, 0.04941435904157133, 0.06827150819941265, 0.03244533622005591];
	};
	getData()
<<<<<<< HEAD
	const map = L.map('map', {
		center: [20.004658, 110.355043],
		zoom: 10,
		renderer: L.svg()
	})
	
	SetPosition([20.004658, 110.355043],10);
	var testData = {
	  max: 0,
	  data: []
	};
	
	// 加入基础地图
	let baseLayer = L.tileLayer(
	  'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: 'Haut-Gis-Org © OpenStreetMap'
	})
	
	// 加入其他层级
	let heatmapLayer = generate_layer(testData);
	heatmapLayer.cfg.radius = 0.001;
	let districtLayer = Districtmap.methods.generate_layer(data,map);
	
	L.control.scale({ maxWidth: 200, metric: true, imperial: false }).addTo(map)
	let mixed = {
		'heatmapLayer': heatmapLayer,
		'districtLayer': districtLayer
		//'OpenStreetMap': baseLayer,
	}
	L.control.layers(null, mixed).addTo(map);
	baseLayer.addTo(map);
	
	map.on('zoomend mouseup', async(e) => {
		let scale = e.target.getZoom();
		let center = e.target.getCenter();
		let center_arr = [center.lng,center.lat];
		let date = SelectedDate();
		let time = SelectedTime();
		SetPosition(center_arr,scale);
		update_layer(date,time,center_arr,scale);
	});
=======



>>>>>>> f34f06f323abd5c29364f9a28a2a5122b6edbffc
</script>
	

<template>
	<div class="Time-Selection">
	<Calendar
		:data="
			weatherData.map((d) => ({
				date:new Date(d['date']),
				price:d['weather'],
			}))
		"
		:calendar_width="650"
		:cellSize="20"
		:clock_width="270"
		:clock_height="200"
	/>
	</div>
	<div class="Title"> 
		<Title
		:width="400"
		:height="200"
		:x="-8"
		:y="0"
		/>
	</div>
	<div class="TimeMap">
		<TimeMap
		:data="timemapData"
		:width="400"
		:height="575"
		/>
	</div>
	<div id="map">
		<Maps
			
		/>
	</div>
</template>

<style>
	.leaflet-container {
		height: 550px;
		width: 925px;
		max-width: 100%;
		max-height: 100%;
		position: absolute;
		left: 400px;
		top: 0px;
	}
	.Time-Selection{
		position: absolute;
		left: 400px;
		top: 560px;
		background-color: chocolate;
	}
	.Title{
		position: absolute;
		left: 0px;
		top:0px;
		background-color: aqua;
	}
	.TimeMap{
		position: absolute;
		left: 0px;
		top: 200px;
		background-color: rgb(15, 20, 19);
	}
	
</style>

