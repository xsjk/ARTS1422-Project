import * as d3 from 'd3'
import { selection } from 'd3';
import { setBlockTracking } from 'vue'
import { update_layer } from '../../maps/heatmap.js'
let value = [];
let hours = [];
let center = [];
let scale = 0;
export function SelectedDate(){
	return value;
}
export function SelectedTime(){
	return hours;
}
export function SelectedCenter(){
	return value;
}
export function SelectedScale(){
	return hours;
}
export function SetPosition(_center,_scale){
	center = _center;
	scale = _scale;
}
// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/calendar-view
export function Calendar(data, {
  x = ([x]) => x, // given d in data, returns the (temporal) x-value
  y = ([, y]) => y, // given d in data, returns the (quantitative) y-value
  title, // given d in data, returns the title text
  width = 928, // width of the chart, in pixels
  cellSize = 17, // width and height of an individual day, in pixels
  weekday = "monday", // either: weekday, sunday, or monday
  formatDay = i => "SMTWTFS"[i], // given a day number in [0, 6], the day-of-week label
  formatMonth = "%b", // format specifier string for months (above the chart)
  yFormat, // format specifier string for values (in the title)
  colors = d3.interpolatePiYG
} = {}) {
  // Compute values.
  const X = d3.map(data, x);
  const Y = d3.map(data, y);
  const I = d3.range(X.length);
  const countDay = weekday === "sunday" ? i => i : i => (i + 6) % 7;
  const timeWeek = weekday === "sunday" ? d3.utcSunday : d3.utcMonday;
  const weekDays = weekday === "weekday" ? 5 : 7;
  const height = cellSize * (weekDays + 2);

  // Compute a color scale. This assumes a diverging color scheme where the pivot
  // is zero, and we want symmetric difference around zero.
  const max = d3.quantile(Y, 0.9975, Math.abs);
  const color = d3.scaleSequential([-max, +max], colors).unknown("none");

  // Construct formats.
  formatMonth = d3.utcFormat(formatMonth);

  // Compute titles.
  if (title === undefined) {
	const formatDate = d3.utcFormat("%B %-d, %Y");
	const formatValue = color.tickFormat(100, yFormat);
	title = i => `${formatDate(X[i])}\n${formatValue(Y[i])}`;
  } else if (title !== null) {
	const T = d3.map(data, title);
	title = i => T[i];
  }

  // Group the index by year, in reverse input order. (Assuming that the input is
  // chronological, this will show years in reverse chronological order.)
  const years = d3.groups(I, i => X[i].getUTCFullYear()).reverse();
  //console.log(years);
  function pathMonth(t) {
	const d = Math.max(0, Math.min(weekDays, countDay(t.getUTCDay())));
	const w = timeWeek.count(d3.utcMonth(X[0]), t);
	return `${d === 0 ? `M${w * cellSize},0`
		: d === weekDays ? `M${(w + 1) * cellSize},0`
		: `M${(w + 1) * cellSize},0V${d * cellSize}H${w * cellSize}`}V${weekDays * cellSize}`;
  }

  const svg = d3.create("svg")
	  .attr("width", width)
	  .attr("height", height * years.length)
	  .attr("viewBox", [0, 0, width, height * years.length])
	  .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
	  .attr("font-family", "sans-serif")
	  .attr("font-size", 10);

  const year = svg.selectAll("g")
	.data(years)
	.join("g")
	  .attr("transform", (d, i) => `translate(40.5,${height * i + cellSize * 1.5})`);

  year.append("text")
	  .attr("x", -5)
	  .attr("y", -5)
	  .attr("font-weight", "bold")
	  .attr("text-anchor", "end")
	  .text(([key]) => key);

  year.append("g")
	  .attr("text-anchor", "end")
	.selectAll("text")
	.data(weekday === "weekday" ? d3.range(1, 6) : d3.range(7))
	.join("text")
	  .attr("x", -5)
	  .attr("y", i => (countDay(i) + 0.5) * cellSize)
	  .attr("dy", "0.31em")
	  .text(formatDay);

  let xScale = i => (timeWeek.count(d3.utcYear(X[i]), X[i]) - timeWeek.count(d3.utcYear(X[0]), X[0])) * cellSize + 0.5;
  let yScale = i => countDay(X[i].getUTCDay()) * cellSize + 0.5
  
  const cell = year.append("g")
	.selectAll("rect")
	.data(weekday === "weekday"
		? ([, I]) => I.filter(i => ![0, 6].includes(X[i].getUTCDay()))
		: ([, I]) => I)
	.join("rect")
	  .attr("width", cellSize - 1)
	  .attr("height", cellSize - 1)
	  .attr("x", i => xScale(i))
	  .attr("y", i => yScale(i)) 
	  .attr("fill", i => color(Y[i]))
	  .attr('opacity', 1)
	  .attr('stroke', 'white')
	  .attr('stroke-width', 0.1)
	.attr('noclicked',true)
	.on('click', function(I,i){
		var noclicked = this.getAttribute('noclicked') == 'true';
		if(noclicked == true){
			d3.select(this)
			.attr('opacity', 0.5)
			.attr('stroke', 'black')
			.attr('stroke-width', 1)
			.attr('noclicked', false)
		}
		else{
			//console.log(clicked)
			d3.select(this)
			.attr('opacity', 1)
			.attr('stroke', 'white')
			.attr('stroke-width', 0.1)
			.attr('noclicked', true)
		}
	})
	

  if (title) cell.append("title")
	  .text(title);

  const month = year.append("g")
	.selectAll("g")
	.data(([, I]) => d3.utcMonths(d3.utcMonth(X[I[0]]), X[I[I.length - 1]]))
	.join("g");

  month.filter((d, i) => i).append("path")
	  .attr("fill", "none")
	  .attr("stroke", "#fff")
	  .attr("stroke-width", 3)
	  .attr("d", pathMonth);

  month.append("text")
	  .attr("x", d => timeWeek.count(d3.utcYear(d), timeWeek.ceil(d)) * cellSize - 360)
	  //.attr("x", d => timeWeek.count(d3.utcYear(d), d3.utcMonth(X[0[0]])) * cellSize - 5)
	  .attr("y", -5)
	  .text(formatMonth);
  
  // brush内容
  const brush = d3.brush()
	  .extent([[30,10], [width-60,height-10]])
	  .on("start", OnStart)
	  .on("brush", OnBrush)
	  .on("end", OnEnd);
  svg.brush = false;
  const selectPlace = svg.append("g")
		.attr('class', 'brush')
		.call(brush);
  d3.select("body").on("keydown",function(current){
		//keydown事件的监听器
		if(current.key == "a" && !svg.brush){
			//如果所按下的键与此svg元素上绑定的数据相同，则call brush
			console.log("按键对了");
		}else{
			//否则不动
			//console.log("按键不对");
			return;}
	})
	.on("keyup", function(current){
		if(current.key == "a"){
			console.log("按键解除");
			svg.brush = false;
		}
	});
  
  // brush 相关函数
  function OnStart({selection}){
	// hide this
	// this.setAttribute('style','display: None');
	if (selection) {
		const [x, y] = selection[0];
		let x_ = x-40.5, y_ = y-cellSize * 1.5;
		console.log(x,y);
		let f = cell.filter(i => xScale(i) < x_ && xScale(i) + cellSize > x_ && yScale(i) < y_ && yScale(i) + cellSize > y_);
		f._groups[0].forEach(rect => {
			if (rect.getAttribute('noclicked') == 'true'){
				rect.setAttribute('opacity', 0.5);
				rect.setAttribute('stroke', 'black');
				rect.setAttribute('stroke-width', 1);
				rect.setAttribute('noclicked', false);
				value.push(rect.__data__);
				//console.log(value);
			} else {
				rect.setAttribute('opacity', 1);
				rect.setAttribute('stroke', 'white');
				rect.setAttribute('stroke-width', 0.1);
				rect.setAttribute('noclicked', true);
				value = value.filter(d => d != rect.__data__);
				update_layer(value,hours,center,scale);
				//console.log(value);
			}
		});
	}
  }
  function OnBrush({selection}) {
	let temp = [];
	if (selection) {
		const [[x0, y0], [x1, y1]] = selection;
		let x_0 = x0-40.5, x_1 = x1-40.5;
		let y_0 = y0 - cellSize * 1.5, y_1 = y1 - cellSize * 1.5;
		d3.selectAll('rect')
		  .attr('opacity', 1)
		  .attr('stroke', 'white')
		  .attr('stroke-width', 0.1)
		  .attr('noclicked', true);
		value = cell
			.filter(i => x_0 <= xScale(i)+cellSize && xScale(i) < x_1
			 && y_0 <= yScale(i)+cellSize && yScale(i) < y_1)
			.attr('opacity', 0.5)
			.attr('stroke', 'black')
			.attr('stroke-width', 1)
			.attr('noclicked',false)
			.data(); 
		//value.push.apply(value,temp);
	} 
	svg.property("value", value).dispatch("input");
  };
  async function OnEnd({selection}){
	update_layer(value,hours,center,scale);
  };
  
  return Object.assign(svg.node(), {scales: {color}});
}

// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/pie-chart
export function PieChart(data, {
  name = ([x]) => x,  // given d in data, returns the (ordinal) label
  value = ([, y]) => y, // given d in data, returns the (quantitative) value
  title, // given d in data, returns the title text
  width = 640, // outer width, in pixels
  height = 400, // outer height, in pixels
  innerRadius = 0, // inner radius of pie, in pixels (non-zero for donut)
  outerRadius = Math.min(width, height) / 2, // outer radius of pie, in pixels
  labelRadius = (innerRadius * 0.2 + outerRadius * 0.8), // center radius of labels
  format = ",", // a format specifier for values (in the label)
  names, // array of names (the domain of the color scale)
  colors, // array of colors for names
  stroke = innerRadius > 0 ? "none" : "white", // stroke separating widths
  strokeWidth = 1, // width of stroke separating wedges
  strokeLinejoin = "round", // line join of stroke separating wedges
  padAngle = stroke === "none" ? 1 / outerRadius : 0, // angular separation between wedges
} = {}) {
  // Compute values.
  const N = d3.map(data, name);
  const V = d3.map(data, value);
  const I = d3.range(N.length).filter(i => !isNaN(V[i]));

  // Unique the names.
  if (names === undefined) names = N;
  names = new d3.InternSet(names);

  // Chose a default color scheme based on cardinality.
  //if (colors === undefined) colors = d3.schemeSpectral[names.size];
  //if (colors === undefined) colors = interpolateWithSteps(names.size).map(d3.interpolateRainbow);
  if (colors === undefined) colors = d3.quantize(t => d3.interpolateRainbow(t * 1), names.size);

  // Construct scales.
  const color = d3.scaleOrdinal(names, colors);

  // Compute titles.
  if (title === undefined) {
    const formatValue = d3.format(format);
    //title = i => `${N[i]}\n${formatValue(V[i])}`;
	title = i => `${N[i]}`;
  } else {
    const O = d3.map(data, d => d);
    const T = title;
    title = i => T(O[i], i, data);
  }

  // Construct arcs.
  const arcs = d3.pie().padAngle(padAngle).sort(null).value(i => V[i])(I);
  const arc = d3.arc().innerRadius(innerRadius).outerRadius(outerRadius);
  const arcLabel = d3.arc().innerRadius(labelRadius).outerRadius(labelRadius);
  
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [-width / 2, -height / 2, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

  svg.append("g")
      .attr("stroke", stroke)
      .attr("stroke-width", strokeWidth)
      .attr("stroke-linejoin", strokeLinejoin)
    .selectAll("path")
    .data(arcs)
    .join("path")
      .attr("fill", d => color(N[d.data]))
      .attr("d", arc)
	.attr('noclicked',true)
		.on('click', function(I,i){
			var noclicked = this.getAttribute('noclicked') == 'true';
			if(noclicked == true){
				hours.push(i.data+1);
				d3.select(this)
				.attr('opacity', 1)
				.attr('stroke', 'black')
				.attr('stroke-width', 1)
				.attr('noclicked', false)
				update_layer(value,hours,center,scale);
			}
			else{
				hours = hours.filter(d => d!=i.data+1)
				d3.select(this)
				.attr('opacity', 0.5)
				.attr('stroke', 'white')
				.attr('stroke-width', 0.5)
				.attr('noclicked', true)
				update_layer(value,hours,center,scale);
			}
		})
	.append("title")
	  .text(d => title(d.data));

  svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("text-anchor", "middle")
    .selectAll("text")
    .data(arcs)
    .join("text")
      .attr("transform", d => `translate(${arcLabel.centroid(d)})`)
    .selectAll("tspan")
    .data(d => {
      const lines = `${title(d.data)}`.split(/\n/);
      return (d.endAngle - d.startAngle) > 0.25 ? lines : lines.slice(0, 1);
    })
    .join("tspan")
      .attr("x", 0)
      .attr("y", (_, i) => `${i * 1.1}em`)
      .attr("font-weight", (_, i) => i ? null : "bold")
      .text(d => d);

  return Object.assign(svg.node(), {scales: {color}});
}