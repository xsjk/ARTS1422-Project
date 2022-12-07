<script>
	import { ref } from 'vue';
	export const mouse_cur_time = ref({
		day:null,
		hour:null,
	})
	export const mouse_drag_start = ref({
		day:null,
		hour:null,
	});
</script>

<script setup>

import * as d3 from 'd3';
import D3Wrapper from './D3Wrapper.vue';
import { watch, computed } from 'vue';
import { mousehold, selected_days, selected_hours, temp_days, temp_hours } from '../../Global.vue';


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
		default: null,
	}
});

const canvas_container = ref(null);
const svg_container = ref(null);


function get_cur_time_by_event (e) {
	const rect = svg_container.value.getBoundingClientRect();
	const x = e.clientX - rect.left;
	const y = e.clientY - rect.top;
	const hour = Math.floor(x / (props.width / 24));
	const day = Math.floor(y / (props.height / 183));
	return {hour: hour, day: day};
}

function update_cur_time(e) {
	if (e) {
		const {hour, day} = get_cur_time_by_event(e);
		mouse_cur_time.value.hour = hour;
		mouse_cur_time.value.day = day;
	} else {
		mouse_cur_time.value.hour = null;
		mouse_cur_time.value.day = null;
	}
}




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
	
	// // draw a grid
	// const grid = svg.selectAll("g.grid").data(d3.range(0, 24, 1));
	// grid.exit().remove();
	// grid.enter().append("g").attr("class", "grid").merge(grid)
	// 	.attr("transform", d => `translate(${d * (width / 24)}, 0)`)
	// 	.call(g => g.append("line")
	// 		.attr("x1", 0)
	// 		.attr("y1", 0)
	// 		.attr("x2", 0)
	// 		.attr("y2", height)
	// 		.attr("stroke", "black")
	// 		.attr("stroke-width", 0.1)
	// 	);

	// // draw a grid
	// const grid2 = svg.selectAll("g.grid2").data(d3.range(0, 183, 1));
	// grid2.exit().remove();
	// grid2.enter().append("g").attr("class", "grid2").merge(grid2)
	// 	.attr("transform", d => `translate(0, ${d * (height / 183)})`)
	// 	.call(g => g.append("line")
	// 		.attr("x1", 0)
	// 		.attr("y1", 0)
	// 		.attr("x2", width)
	// 		.attr("y2", 0)
	// 		.attr("stroke", "black")
	// 		.attr("stroke-width", 0.1)
	// 	);
	
	// draw rectangles 24*183
	const rects = svg.selectAll("rect").data(d3.range(0, 24*183, 1));
	rects.exit().remove();
	rects.enter().append("rect")
		.attr("class", "timemap_rect")
		.attr("x", d => (d % 24) * (width / 24))
		.attr("y", d => (Math.floor(d / 24)+0.5) * (height / 183))
		.attr("selected", "false")
		.merge(rects);




		
	svg.on("mousemove", e => {
		update_cur_time(e);
	}).on('mouseup', e => {
		mousehold.value = false;
		const mouse_drag_end = get_cur_time_by_event(e);
		// console.log("hour range:", mouse_drag_start.value.hour, mouse_drag_end.hour);
		// console.log("day range:", mouse_drag_start.value.day, mouse_drag_end.day);

	}).on('mouseout', e => {
		update_cur_time();
	}).on('mousedown', e => {

		const {hour, day} = get_cur_time_by_event(e);
		console.log("click", hour, day);
		
		mouse_drag_start.value.hour = hour;
		mouse_drag_start.value.day = day;
		temp_days.value = [day];
		temp_hours.value = [hour];
	});

}


watch(
	() => props.data,
	() => {
		update();
	},
);

watch(
	[temp_days, temp_hours],
	() => {
		d3.select('.timemap_svg').selectAll("rect").filter(d => {
			const hour = d % 24;
			const day = Math.floor(d / 24);
			return temp_hours.value.includes(hour) && temp_days.value.includes(day);
		}).attr("selected", "true");
		d3.select('.timemap_svg').selectAll("rect").filter(d => {
			const hour = d % 24;
			const day = Math.floor(d / 24);
			return !temp_hours.value.includes(hour) || !temp_days.value.includes(day);
		}).attr("selected", "false");
	},
)


watch(
	[mouse_cur_time],
	() => {
		if (mousehold.value) {
			console.log("dragging");
			if (mouse_cur_time.value.hour == null || mouse_cur_time.value.day == null) {
				return;
			}
			if (mouse_drag_start.value.hour == null || mouse_drag_start.value.day == null) {
				
				return;
			}
            const hour_range = {
                min: Math.min(mouse_cur_time.value.hour, mouse_drag_start.value.hour),
                max: Math.max(mouse_cur_time.value.hour, mouse_drag_start.value.hour)
            };
            const day_range = {
                min: Math.min(mouse_cur_time.value.day, mouse_drag_start.value.day),
                max: Math.max(mouse_cur_time.value.day, mouse_drag_start.value.day)
            };

            console.log("hour_range", hour_range);
            console.log("day_range", day_range);

			temp_days.value = d3.range(day_range.min, day_range.max+1);
			temp_hours.value = d3.range(hour_range.min, hour_range.max+1);


		} else {
			// highlight current time in clock
			const hour = mouse_cur_time.value.hour;
			// console.log("highlight", hour);
			d3.selectAll(".hour_arc")
                .attr("mouseovered", d => d.data % 24 == hour)
				
				// .attr("stroke", d => d.data % 24 == hour ? "yellow" : "white")
				// .attr("stroke-width", d => d.data % 24 == hour ? 3 : 0.5)

			// highlight current day in calendar
			const day = mouse_cur_time.value.day;
			// console.log("highlight", day);
			d3.selectAll(".day_cell")
				.attr("mouseovered", d => d == day )
		}

	},
	{ deep: true }

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
	rect.timemap_rect[selected=false] {
		width: 9.583333333333334px;
		height: 4.054054054054054px;
		fill: none;
		stroke-width: 0;
	}
	rect.timemap_rect[selected=true] {
		width: 9.583333333333334px;
		height: 4.054054054054054px;
		opacity: 0.3;
		stroke-width: 0;
	}
	
</style>


