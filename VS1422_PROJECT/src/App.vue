<script setup>
	//import Heatmap from './components/map/heatmap.vue'
	import Calendar from './components/d3/Calendar.vue'
	import TimeMap from './components/d3/Timemap.vue'
	import Title from './components/d3/Title.vue'
	import Maps from './components/map/Maps.vue'
	import * as d3 from 'd3';
	import { weatherData, timemapData, equaltimeData } from './Global.vue';
		
	// 用来获取数据的组合
	console.log(timemapData);
	const getData = async () => {
	  const weatherTest = await d3.csv('weatherData.csv');
	  weatherData.value = weatherTest.map(d => d);
	  timemapData.value = [[0.1,0.2],[0.3,0.4]];
	  equaltimeData.value = [0.028758452380954324, 0.02031264526842589, 0.03360677895017247, 0.04200094409784688, 0.03459567830588102, 0.0, 0.0, 0.0, 0.0, 0.025049999999993133, 0.03703024779237924, 0.05582818807481003, 0.028591562079811773, 0.02556251189854171, 0.020557370556213986, 0.04941435904157133, 0.06827150819941265, 0.03244533622005591];
	};
	getData()
	
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
		:calendar_width="600"
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
		background-color: azure;
		width: 1200px;
	}
	.Title{
		position: absolute;
		left: 0px;
		top:0px;
/* 		background-color: aqua; */
	}
	.TimeMap{
		position: absolute;
		left: 0px;
		top: 200px;
/* 		background-color: rgb(15, 20, 19); */
	}
	
</style>

