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
		}
	});
	
	const title = computed(() => {
		let {
			width,
			height
		} = props;
		
		
		const svg = d3.create("svg")
					.attr("width", width)
					.attr("height", height)
					
		let top = 25;
		
		let TextE = svg.append("g")
		.append("text")
		.attr("class", "title")
		.text("Spatial and Temporal Evolution of Traffic Flow in Haikou City")
		.attr("transform", `translate(${width/2},${height/2})`)
		
		
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
		fill: cyan;
		font-size: 1cm;
		font-family: 'Segoe UI Light';
		stroke: antiquewhite;
		stroke-width: 0.1;
		/* font-weight: bold; */
	}
</style>