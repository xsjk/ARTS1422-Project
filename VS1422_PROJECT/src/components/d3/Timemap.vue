<script>
	import { ref } from 'vue';
	export const timemap_cur_day = ref(0);
	export const timemap_cur_hour = ref(0);
</script>

<script setup>

import { watch } from 'vue';
import * as d3 from 'd3';
import { mousehold } from '../../Global.vue';
import D3Wrapper from './D3Wrapper.vue';
import { computed } from 'vue';




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

function interpolate_tiles(tile, n, m) {
  return d3.range(0, tile.length-1, 1/n).map(y => (
      d3.range(0, tile[0].length-1, 1/m).map(x => {
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
		default: d3.interpolate("#4581D8", "#ffffff"),
	}
});

const canvas_container = ref(null);
const svg_container = ref(null);

function update() {
	let {
		data,
		width,
		height,
		color
	} = props;



	// update the canvas

	canvas_container.value.addEventListener('mousemove', (e) => {
		const rect = canvas_container.value.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;
		const hour = Math.floor(x / (width / 24) + 0.5);
		const day = Math.floor(y / (height / 182) + 0.5);
		console.log(hour, day);
	});

	const px = 0;
	const py = 0;

	const img_height = height - 2*py;
	const img_width = width - 2*px;

	if (img_height <= 0 || img_width <= 0) {
		return;
	}

	// add a column
	data = data.map(row => row.concat(row[0]));


	const tiles = interpolate_tiles(data, img_height / 183, img_width / 24);
	if (tiles.length === 0) {
		console.log("empty tiles");
		return;
	}
	console.log(tiles);
	// draw the canvas
	const shape = {x: tiles[0].length, y: tiles.length};

	console.log(shape);
	console.log(height, width);
	console.log(img_height, img_width);


	canvas_container.value.width = width
	canvas_container.value.height = height
	const context = canvas_container.value.getContext("2d");
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

	context.putImageData(img, px, py);



	// update the svg
	const svg = d3.select(svg_container.value);
	
	// draw a grid
	const grid = svg.append("g")
		.attr("class", "grid")
		.attr("transform", `translate(0, ${height})`);

	const y = d3.scaleTime()
		.domain([new Date(2017, 5, 1), new Date(2017, 10, 31)])
		.range([0, height]);

	const x = d3.scaleTime()
		.domain([0, 24])
		.range([0, width]);

	console.log("x", x);
	console.log("y", y);

	const xAxis = d3.axisBottom(x)
		.tickFormat(d3.timeFormat("%b"))
		.tickSize(-height);

	const yAxis = d3.axisLeft(y)
		.tickFormat(d3.timeFormat("%d"))
		.tickSize(-width);

		
	svg.on("mousemove", e => {
		if (mousehold.value) {
			
			console.log("dragging");
		} else {
			const rect = svg_container.value.getBoundingClientRect();
			const x = e.clientX - rect.left;
			const y = e.clientY - rect.top;
			const hour = Math.floor(x / (width / 24) + 0.5);
			const day = Math.floor(y / (height / 183) + 0.5);
			timemap_cur_day.value = day;
			timemap_cur_hour.value = hour;
			// console.log(curDatetime.value);
		}
	});
		



}

// const gridlayer = computed(() => {
// 	const {
// 		width,
// 		height,
// 	} = props;

// 	const grid = s.append("g")
// 		.attr("class", "grid")
// 		.attr("transform", `translate(0, ${height})`);

// 	console.log("gridlayer", grid);


// 	const x = d3.scaleTime()
// 		.domain([new Date(2017, 5, 1), new Date(2017, 10, 31)])
// 		.range([0, width]);

// 	const y = d3.scaleTime()
// 		.domain([0, 24])
// 		.range([0, height]);

// 	const xAxis = d3.axisBottom(x)
// 		.tickFormat(d3.timeFormat("%b"))
// 		.tickSizeOuter(0);

// 	const yAxis = d3.axisLeft(y)
// 		.tickFormat(d3.timeFormat("%H"))
// 		.tickSizeOuter(0);

// 	grid.append("g")
// 		.attr("class", "x axis")
// 		.call(xAxis);

// 	grid.append("g")
// 		.attr("class", "y axis")
// 		.call(yAxis);

// 	return grid.node();
// });


watch(
	() => props.data,
	() => {
		update();
	},
);


</script>


<template>
	<div class="timemap_img">
		<canvas ref="canvas_container" />
	</div>
	<div class="timemap_axis">
		<svg class="timemap_svg" ref="svg_container" />
	</div>
</template>



<style>
	.timemap_img {
		width: 230px;
		height: 740px;
		position: absolute;
		z-index: 1;
	}
	.timemap_axis {
		width: 230px;
		height: 740px;
		position: absolute;
		z-index: 2;
	}
	.timemap_svg {
		width: 230px;
		height: 740px;
	}
</style>


