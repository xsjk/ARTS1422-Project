<script setup>
	import D3Wrapper from './D3Wrapper.vue';
	import { computed } from 'vue';
	import * as d3 from 'd3';
	import { color } from 'd3';
	
	const props = defineProps({
		width:{
			type: [Number, String],
			default: null, 
		},
		height:{
			type: [Number, String],
			default: null, 
		},
		x:{
			type: [Number, String],
			default: null, 
		},
		y:{
			type: [Number, String],
			default: null, 
		}
	});
	
	const title = computed(() => {
		let {
			width,
			height,
			x,
			y
		} = props;
		
		
		const svg = d3.create("svg")
					.attr("class", "back")
					.attr("width", width)
					.attr("height", height)
					.attr("transform", `translate(${x},${y})`)
					
		let top = 25;
		
		let TextE = svg.append("g")
		.append("text")
		.attr("class", "title")
		.text("Visual Analysis")
		.attr("x", width/2)
		.attr("y", top)
		// .attr("fill", )
		// .style("text-anchor", "start")
		// .style("font-size", "")
		// .style("font-weight", "")
		// .style("font-family", "")
		
		let padding = 25;
		
		TextE.append("tspan")
		.attr("class", "interval")
		.text("of the")
		.attr("x", width/2)
		.attr("y", top+1*padding)
		TextE.append("tspan")
		.attr("class", "title")
		.text("Spatial and Temporal")
		.attr("x", width/2)
		.attr("y", top+2*padding)
		TextE.append("tspan")
		.attr("class", "title")
		.text("Evolution")
		.attr("x", width/2)
		.attr("y", top+3*padding)
		TextE.append("tspan")
		.attr("class", "interval")
		.text("of")
		.attr("x", width/2)
		.attr("y", top+4*padding)
		TextE.append("tspan")
		.attr("class", "title")
		.text("Traffic Flow")
		.attr("x", width/2)
		.attr("y", top+5*padding)
		TextE.append("tspan")
		.attr("class", "interval")
		.text("in")
		.attr("x", width/2)
		.attr("y", top+6*padding)
		TextE.append("tspan")
		.attr("class", "title")
		.text("Haikou")
		.attr("x", width/2)
		.attr("y", top+7*padding)
		
		
		
		
		
		return svg.node();
	})
	
</script>

<template>
	<div>
		<D3Wrapper :node="title"/>
	</div>
</template>

<style>
	.title{
		position: relative;
		text-anchor: middle;
		fill: black;
		font-size: 0.8cm;
		font-family: 'Courier New', Courier, monospace;
		stroke: antiquewhite;
		stroke-width: 0.3;
	}
	.interval{
		position: relative;
		text-anchor: middle;
		fill: black;
		font-size: 0.55cm;
		font-family: 'Courier New', Courier, monospace;
		stroke: antiquewhite;
		stroke-width: 0.3;
	}
	.back{
		background-color: aqua;
	}
</style>