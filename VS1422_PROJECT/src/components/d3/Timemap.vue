<script setup>

import { ref, watch } from 'vue';
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

const container = ref(null);

function grid(h,w) {
	var canvas = container.value;
	
		var context = canvas.getContext("2d");
		 //水平标尺与canvas的距离
		var HORIZONTAL_AXIS_MARGIN = 50;
		 //竖直标尺与canvas的距离
		var VERTICAL_AXIS_MARGIN = 50;
		 //标尺起点
		var AXIS_ORIGIN = {
			x: HORIZONTAL_AXIS_MARGIN,
			y: canvas.height - VERTICAL_AXIS_MARGIN
		};
		 //坐标的顶部
		var AXIS_TOP = VERTICAL_AXIS_MARGIN;
		 //坐标的长度
		var AXIS_RIGHT = canvas.width - HORIZONTAL_AXIS_MARGIN;
		 //小标记的间隔
		var HORIZONTAL_TICK_SPACING = w/24/2;
		var VERTICAL_TICK_SPACING = 10;
		 //坐标标记的范围
		var AXIS_WIDTH = AXIS_RIGHT - AXIS_ORIGIN.x;
		var AXIS_HEIGHT = AXIS_ORIGIN.y - AXIS_TOP;
		 //纵向标记数值
		var NUM_VERTICAL_TICKS = AXIS_HEIGHT / VERTICAL_TICK_SPACING;
		 //横向标记数值
		var NUM_HORIZONTAL_TICKS = AXIS_WIDTH / HORIZONTAL_TICK_SPACING;
		var TICK_WIDTH = 10;
		 //标牌和坐标轴之间的距离
		var SPACE_BETWEEN_ABELS_AND_AXIS = 20;
 
		function drawAxes() {
			context.save();
			context.lineWidth = 1.0;
			context.fillStyle = "rgba(100, 140, 230, 0.8)";
			context.strokeStyle = "navy";
			drawHorizontalAxis();
			drawVerticalAxis();
			context.lineWidth = 0.5;
			context.strokeStyle = "navy";
			context.strokeStyle = "darkred";
			drawVerticalAxisTicks();
			drawHorizontalAxisTicks();
			context.restore();
		}
		
		//绘制水平的小标
		function drawHorizontalAxisTicks() {
			var deltaY;
			for (var i = 1; i < NUM_HORIZONTAL_TICKS; i++) {
				context.beginPath();
				//判断画的是大坐标还是短坐标
				if (i % 5 == 0) {
					deltaY = TICK_WIDTH;
				} else {
					deltaY = TICK_WIDTH / 2
				}
				context.moveTo(AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING,
					AXIS_ORIGIN.y - deltaY);
				context.lineTo(AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING,
					AXIS_ORIGIN.y + deltaY);
				context.stroke();
			}
		}
		
		//绘制数值的小标
		function drawVerticalAxisTicks() {
			var deltaX;
			for (var i = 1; i < NUM_VERTICAL_TICKS; i++) {
				context.beginPath();
				if (i % 5 === 0) {
					deltaX = TICK_WIDTH;
				} else {
					deltaX = TICK_WIDTH / 2;
				}
				context.moveTo(AXIS_ORIGIN.x - deltaX,
					AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
				context.lineTo(AXIS_ORIGIN.x + deltaX,
					AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
				context.stroke();
			}
		}

		//画竖直线
		function drawVerticalAxis() {
			context.beginPath();
			context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
			context.lineTo(AXIS_ORIGIN.x, AXIS_TOP);
			context.stroke();
		}
		
		//画水平线
		function drawHorizontalAxis() {
			context.beginPath();
			context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
			context.lineTo(AXIS_RIGHT, AXIS_ORIGIN.y);
			context.stroke();
		}
		//绘制标注
		function drawAxisLabels() {
			// context.fillStyle = "blue";
			drawHorizontalAxisLabels();
			drawVerticalAxisLabels();
		}
		
		//绘制竖直轴标注
		function drawVerticalAxisLabels() {
			context.textAlign = "center";
			context.textBaseline = "top";
			for (var i = 0; i <= NUM_HORIZONTAL_TICKS; i++) {
				if (i % 5 === 0) {
					context.fillText(i,
						AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING,
						AXIS_ORIGIN.y + SPACE_BETWEEN_ABELS_AND_AXIS);
				}
			}
		}
		
		//绘制水平轴标注
		function drawHorizontalAxisLabels() {
			context.textAlign = "center";
			context.textBaseline = "middle";
			for (var i = 0; i <= NUM_VERTICAL_TICKS; i++) {
				if (i % 5 === 0) {
					context.fillText(i,
						AXIS_ORIGIN.x - SPACE_BETWEEN_ABELS_AND_AXIS,
						AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
				}
			}
		}

		function drawGrid(color, stepx, stepy) {
			// context.save()
			context.strokeStyle = color;
			// context.fillStyle = '#ffffff';
			context.lineWidth = 0.5;
			// context.fillRect(0, 0, context.canvas.width, context.canvas.height);
			for (var i = stepx + 0.5; i < context.canvas.width; i += stepx) {
				context.beginPath();
				context.moveTo(i, 0);
				context.lineTo(i, context.canvas.height);
				context.stroke();
			}
			for (var i = stepy + 0.5; i < context.canvas.height; i += stepy) {
				context.beginPath();
				context.moveTo(0, i);
				context.lineTo(context.canvas.width, i);
				context.stroke();
			}
			context.restore();
		}

		
		context.font = "11px Arial";
		drawGrid("lightgray", w/24, h/183*7)
		context.shadowColor = "rgba(100, 140, 230, 0.8)";
		context.shadowOffsetX = 1;
		context.shadowOffsetY = 1;
		context.shadowBlur = 2;
		drawAxes();
		drawAxisLabels();



}

function update() {
	let {
		data,
		width,
		height,
		color
	} = props;

	// container.value.style.width = `${width}px`;
	// container.value.style.height = `${height}px`;

	container.value.addEventListener('mousemove', (e) => {
		const rect = container.value.getBoundingClientRect();
		const x = e.clientX - rect.left;
		const y = e.clientY - rect.top;
		const hour = Math.floor(x / (width / 24));
		const day = Math.floor(y / (height / 183));
		console.log(hour, day);
	});

	const px = 50;
	const py = 50;

	const img_height = height - 2*py;
	const img_width = width - 2*px;

	if (img_height <= 0 || img_width <= 0) {
		return;
	}
	

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

	container.value.width = width
	container.value.height = height
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

	context.putImageData(img, px, py);
	grid(img_width, img_height)

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