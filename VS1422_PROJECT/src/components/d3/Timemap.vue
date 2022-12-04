<script setup>

import { defineProps, ref, watch } from 'vue';
import * as d3 from 'd3';

const bilinearInterpolator = func => (x, y) => {
  // "func" is a function that takes 2 integer arguments and returns some value
  const x1 = Math.floor(x);
  const x2 = Math.ceil(x);
  const y1 = Math.floor(y);
  const y2 = Math.ceil(y);

  if ((x1 === x2) && (y1 === y2)) return func(x1, y1);
  if (x1 === x2) return (func(x1, y1) * (y2 - y) + func(x1, y2) * (y - y1)) / (y2 - y1);
  if (y1 === y2) return (func(x1, y1) * (x2 - x) + func(x2, y1) * (x - x1)) / (x2 - x1);
  // else: x1 != x2 and y1 != y2
  return (
    func(x1, y1) * (x2 - x) * (y2 - y) +
    func(x2, y1) * (x - x1) * (y2 - y) +
    func(x1, y2) * (x2 - x) * (y - y1) +
    func(x2, y2) * (x - x1) * (y - y1)
  )
  / ((x2 - x1) * (y2 - y1));
}

function interpolate_tiles(tile, n=40) {
  return d3.range(0, tile.length-1, 1/n).map(y => (
      d3.range(0, tile[0].length-1, 1/n).map(x => {
      const interpolate = bilinearInterpolator((i, j) => tile[j][i])
      return interpolate(x, y);
      })
  ));
}

const props = defineProps({
	data: {
		type: Array,
		default: null,
	},
	width:{
		type: [Number, String],
		default: null, 
	},
	height:{
		type: [Number, String],
		default: null, 
	},
	color:{
		type: Function,
		default: d3.interpolateViridis, 
	}
});

const container = ref(null);

function update() {
	let {
		data,
		width,
		height,
		color
	} = props;

	container.value.style.width = `${width}px`;
	container.value.style.height = `${height}px`;

	container.value.addEventListener('mousemove', (e) => {
		const rect = container.value.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;
		const hour = Math.floor(x / (width / 24));
		const day = Math.floor(y / (height / 183));
		console.log(hour, day);
	});
	
	const tiles = interpolate_tiles(data, 40);
	if (tiles.length === 0) {
		console.log("empty tiles");
		return;
	}
	// draw the canvas
	const shape = {x: tiles[0].length, y: tiles.length};
	container.value.width = shape.x;
	container.value.height = shape.y;
	const context = container.value.getContext("2d");
	const img = context.createImageData(shape.x, shape.y);
	const flat = [].concat.apply([], tiles);
	const [min, max] = d3.extent(flat);
	const normalize = d => ((d-min)/(max-min));
	const colorScale = d => color(normalize(d));
	tiles.forEach((row, i) => {
		row.forEach((d, j) => {
		let color = isNaN(d) ? {r: 0, g: 0, b: 0} : d3.color(colorScale(d));
		img.data[(i*tiles[0].length+j)*4  ] = color.r;
		img.data[(i*tiles[0].length+j)*4+1] = color.g;
		img.data[(i*tiles[0].length+j)*4+2] = color.b;
		img.data[(i*tiles[0].length+j)*4+3] = 255;
		});
	});
	context.putImageData(img, 0, 0);
}

watch(
	() => props.data,
	() => {
		update();
	},
);


</script>


<template>
	<div>
		<canvas ref="container" />
	</div>
</template>