<script setup>
import D3Wrapper from './D3Wrapper.vue';
import { computed, defineProps } from 'vue';
import * as d3 from 'd3';
import {Calendar} from "../../composables/d3/calendar/calendar"

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  rows: {
    type: [Number, String],
    default: 2,
  },
  columns: {
    type: [Number, String],
    default: null,
  },
  scheme: {
    type: Array,
    default: d3.schemeCategory10,
  },
  rectWidth: {
    type: [Number, String],
    default: 20,
  },
  rectHeight: {
    type: [Number, String],
    default: 20,
  },
  rectMargin: {
    type: [Number, String],
    default: 0,
  },
  width: {
    type: [Number, String],
    default: null,
  },
  height: {
    type: [Number, String],
    default: null,
  },
});

const legend = computed(() => {
  let {
    data,
    rows,
    columns,
    scheme,
    rectWidth,
    rectHeight,
    rectMargin,
    width,
    height,
  } = props;

  if (columns === null) {
    columns = Math.floor(new Set(data.map((d) => d.category)).size / rows);
  }

  if (width === null) {
    width = columns * (rectWidth + 2 * rectMargin);
  }

  if (height === null) {
    height = rows * (rectHeight + 2 * rectMargin);
  }
  
  const svg = d3
    .create('svg')
    .attr('viewBox', [0, 0, width, height])
    .attr('width', width)
    .attr('height', height);
  const color = d3.scaleOrdinal(
    data.map((d) => d.category),
    scheme,
  );
  svg
    .selectAll('rect')
    .data(color.domain().slice())
    .join('rect')
    .attr(
      'x',
      (d, i) => (i % columns) * (rectWidth + 2 * rectMargin),
    )
    .attr(
      'y',
      (d, i) => Math.floor(i / columns) * (rectHeight + 2 * rectMargin),
    )
    .attr('width', 20)
	.attr('luaobb',123)
    .attr('height', 20)
    .attr('fill', (d) => color(d))
	.attr('opacity', 0.5)
	.attr('stroke', 'white')
	.attr('stroke-width', 0.5)
	.attr('noclicked',true)
	.on('click', function(I,i){
		var noclicked = this.getAttribute('noclicked') == 'true';
		//console.log("1"+noclicked);
		if(noclicked == true){
			//console.log('2'+noclicked)
			d3.select(this)
			.attr('opacity', 1)
			.attr('stroke', 'black')
			.attr('stroke-width', 1)
			.attr('noclicked', false)
		}
		else{
			//console.log(clicked)
			d3.select(this)
			.attr('opacity', 0.5)
			.attr('stroke', 'white')
			.attr('stroke-width', 0.5)
			.attr('noclicked', true)
		}
	})

  return Calendar(data, {
	x: d => d.date,
	y: d => d.price,
	weekday: "weekday",
	width
  });
});
</script>
<template>
  <D3Wrapper :node="legend" />
</template>