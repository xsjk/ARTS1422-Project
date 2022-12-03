<script setup>
import D3Wrapper from './D3Wrapper.vue';
import { computed } from 'vue';
import * as d3 from 'd3';
import {Calendar} from "../../composables/d3/calendar/calendar"
import {PieChart} from "../../composables/d3/calendar/pie"
import {Legend} from "../../composables/d3/calendar/color-legend"

const props = defineProps({
  data: {
	type: Array,
	required: true,
  },
  calendar_width: {
	type: [Number, String],
	default: null,
  },
  cellSize: {
	type: [Number, String],
	default: null, 
  },
  clock_width:{
	type: [Number, String],
	default: null, 
  },
  clock_height:{
	  type: [Number, String],
	  default: null, 
  }
});

// 在这里搞legend， legend的template写在了下面，搞完记得在这里的style给3个div调下位置
// 现在调用的函数时composables里的color-legend.jsx, d3上找的，它自带的映射不是很好用
// 如果想要看原图，把下面的legend的div注释掉应该就行
const legend = computed(() => {
	const colors = d3.interpolate("#eafffa", "#00004f");
	const weatherMap = {
	    "多云": 0.0,
	    "小到中雨": 0.2,
	    "阵雨": 0.3,
	    "中雨": 0.4,
	    "雷阵雨": 0.5,
	    "中到大雨": 0.6,
	    "大雨": 0.7,
	    "大到暴雨": 0.8,
	    "暴雨": 0.9,
	    "大暴雨": 1.0,
	};
	const test = [0.0,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0];
	return Legend(d3.scaleSequential([0, 1], colors),{
		title: "Unemployment rate (%)",
		tickSize: 0
	});
})


const calendar = computed(() => {
  let {
	data,
	calendar_width,
	cellSize
  } = props;
  
  // 从淡蓝到深蓝,第一个是黄色
  //const colors = ["#FFFF00","#0000FF", "#0000CD", "#191970", "#00008B"];
  const colors = d3.interpolate("#eafffa", "#00004f");
  
  return Calendar(data, {
	x: d => d.date,
	y: d => d.price,
	weekday: "monday",
	width: calendar_width,
	cellSize: cellSize,
	colors: colors
  });
});

const clock = computed(() => {
	let {
		clock_width,
		clock_height
	} = props;
	
	var data = [
		{'hour': 0},{'hour': 1},{'hour': 2},
		{'hour': 3},{'hour': 4},{'hour': 5},
		{'hour': 6},{'hour': 7},{'hour': 8},
		{'hour': 9},{'hour': 10},{'hour': 11},
		{'hour': 12},{'hour': 13},{'hour': 14},
		{'hour': 15},{'hour': 16},{'hour': 17},
		{'hour': 18},{'hour': 19},{'hour': 20},
		{'hour': 21},{'hour': 22},{'hour': 23},
	]
	
	return PieChart(data,{
	name: d => d.hour,
	value: d => 1,
	width: clock_width,
	height: clock_height
	})
});

</script>

<template>
	<div class = "calendar" style = "display: inline;float:left">
		<D3Wrapper :node="calendar"/>
	</div>
	<div class = "legend" style = "display: inline;float:left">
		<D3Wrapper :node="legend"/>
	</div>
	<div class = "clock" style = "display: inline;float:right">
		<D3Wrapper :node="clock"/>
	</div>
</template>

<style>
</style>