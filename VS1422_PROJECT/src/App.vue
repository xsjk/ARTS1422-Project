<script setup>
	import Calendar from './components/d3/Calendar.vue'
	import TimeMap from './components/d3/Timemap.vue'
	import Title from './components/d3/Title.vue'
	import Title2 from './components/d3/Title2.vue'
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
		:calendar_width="680"
		:cellSize="23"
		:clock_width="270"
		:clock_height="200"
		:legend_width="135"
	/>
	</div>
	<!-- <div class="Title"> 
		<Title
		:width="400"
		:height="200"
		:x="-8"
		:y="0"
		/>
	</div> -->
	<div class="Title2"> 
		<Title2
		:width="1300"
		:height="100"
		/>
	</div>
	<div class="TimeMap">
		<TimeMap
		:data="timemapData"
		:width="230"
		:height="740"
		:color='d3.interpolateRgb.gamma(0.1)("#3561A8", "#ffffff")'
		/>
	</div>
	<div id="map">
		<Maps/>
	</div>
</template>

<style>
	.leaflet-container {
		height: 550px;
		width: 950px;
		max-width: 100%;
		max-height: 100%;
		position: absolute;
		left: 50px;
		top: 90px;
	}
	.Time-Selection{
		position: absolute;
		left: 75px;
		top: 650px;
		width: 1200px;
	}
	/* .Title{
		position: absolute;
		left: 75px;
		top: 15px;
	} */
	.TimeMap{
		position: absolute;
		left: 1025px;
		top: 90px;
	}
	.Title2{
		position: absolute;
		left: 0px;
		top: 0px;
	}
	
</style>

