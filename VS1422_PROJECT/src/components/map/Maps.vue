<script>
import { ref } from 'vue'
export const center = ref([110.355043, 20.004658]);
export const scale = ref(12);
export const selected = ref([]);
export const distance = ref(10);
export const global_map = ref(null);
export const can_move = ref(true);
</script>

<script setup>
	import * as HeatMapIn from '../../composables/layers/heatmap_in';
	import * as HeatMapOut from '../../composables/layers/heatmap_out';
	import * as DistrictMap from '../../composables/layers/district_division'
	import * as EqualTimeMap from '../../composables/layers/equal_time'
	import * as TopologicMap from '../../composables/layers/topologic'
	import { watch } from 'vue';
	import Controls from '../controls/Controls.vue'
	import { mousehold, selected_hours, selected_days, selected_districts, mouseovered_district } from '../../Global.vue';
	import {order} from '../d3/Timemap.vue'

	import * as d3 from 'd3';
	import L from 'leaflet';

	import { weatherData, timemapData, equaltimeData, topologicData } from '../../Global.vue';

	const props = defineProps({
	  date: {
		type: Array,
		required: true,
	  },
	  time: {
		type: Array,
		required: true,
	  },
	  center: {
		type: Array,
		required: true,
	  },
	  scale:{
		type: [Number, String],
		default: null,
	  }
	});


	// 用来获取数据的组合
	timemapData.value = await traffic_flow_in_degree_graph(district_ids)

	var testData = {
	  max: 0,
	  data: []
	};



	/// layers
	const mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
	const mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
	const streets = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	const dark = L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	});
	const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'});
	const timemap_img = L.tileLayer('../../../src/assets/timemap.png');
	const satellite = L.tileLayer(mbUrl, {id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	const baseLayers = {
		// 'Basemap': osm,
		// 'Streets': streets,
		'Dark': dark,
		'Satellite': satellite,
	};

	let heatmapinLayer = HeatMapIn.generate_layer(testData);
		heatmapinLayer.cfg.radius = 0.001;
	let heatmapoutLayer = HeatMapOut.generate_layer(testData);
		heatmapoutLayer.cfg.radius = 0.001;

	const map = L.map('map', {
		center: [center.value[1], center.value[0]],
		zoom: scale.value,
		renderer: L.svg(),
		attributionControl:false,
		layers: [dark],
		doubleClickZoom: true,
		dragging: true,
		closePopupOnClick: true,
	})
	global_map.value = map;
	let districtLayer = DistrictMap.generate_layer(data, map, selected_districts, can_move);
	let equaltimeLayer = EqualTimeMap.generate_layer(equaltimeData.value, map);
	topologicData.value = await draw_topological_graph_by_departure_time([], []);
	let topologicLayer = TopologicMap.generate_layer(topologicData.value, map, can_move, mouseovered_district);



	// 给所有图层添加add时的自动更新
	// HeatMap
	heatmapinLayer.on("add",function(){
		HeatMapIn.update_layer(selected_days.value, selected_hours.value, center.value, scale.value);
	})
	heatmapoutLayer.on("add",function(){
		console.log("HeatMapOut Loaded");
		HeatMapOut.update_layer(selected_days.value, selected_hours.value, center.value, scale.value);
	})
	// 等时线图
	equaltimeLayer.on("add",function(){
		if (selected.value == undefined || selected.value.length == 0){
			selected.value = center.value;
		}
		distance.value = 10;
		EqualTimeMap.update_layer(map,selected.value,selected_days.value,selected_hours.value,distance.value);
		EqualTimeMap.generate_selection(map,distance);
	}).on("remove",function(){
		console.log("equalTime Removed");
		EqualTimeMap.remove_selection(map);
	})
	// 拓扑图
	topologicLayer.on("add", async function(){
		topologicData.value = await draw_topological_graph_by_departure_time(selected_days.value, selected_hours.value);
		TopologicMap.update_layer(topologicData.value, map);
	}).on("remove",function(){
		console.log("topologic Removed");
		TopologicMap.remove_layer(map);
	})

	var marker = L.marker(center.value);
	marker.addTo(map);
	map.on('click', async(e) => {
		// mousehold.value = false;
		// if(!can_move.value) return;
		if(!map.hasLayer(equaltimeLayer)) return;
		//console.log(e);
		var popup = L.popup()
			.setContent(marker)
			.setLatLng(e.latlng)
			.setContent(`${e.latlng.toString()}`)
			// .openOn(map);
		marker.setLatLng(e.latlng);
		//marker.bindPopup(popup).openPopup();
		//marker.bindPopup(Popup);
		selected.value = [e.latlng.lng, e.latlng.lat];
		center.value = [e.latlng.lng, e.latlng.lat];
	});

	map.on('zoomend', async(e) => {
		scale.value = e.target.getZoom();
	});

	map.on('mouseup', async(e) => {
		console.log("map mouseup")
		mousehold.value = false;
		center.value = [e.target.getCenter().lng, e.target.getCenter().lat];
	});

	const scale_control = L.control.scale({ maxWidth: 200, metric: true, imperial: false });
	scale_control.addTo(map)
	
	///////
	let mixed = {
		'HeatMapInLayer': heatmapinLayer,
		'HeatMapOutLayer': heatmapoutLayer,
		'equaltimeLayer': equaltimeLayer,
		'topologicalLayer': topologicLayer,
	}
	const controller = L.control.layers(baseLayers, mixed).addTo(map);
	districtLayer.addTo(map);
	
	
	// watch
	watch(
		[selected_hours, selected_days, center, scale],
		async () => {
			if(map.hasLayer(heatmapoutLayer)){
				HeatMapOut.update_layer(selected_days.value, selected_hours.value, center.value, scale.value);
			}

			if(map.hasLayer(heatmapinLayer)){
				HeatMapIn.update_layer(selected_days.value, selected_hours.value, center.value, scale.value);
			}
		},
		{ deep: true }
	);

	watch(
		[selected_hours, selected_days, selected, distance],
		async () => {
			if(!map.hasLayer(equaltimeLayer)){
			  console.log("EqualTimeMap不需要更新")
			  return;
			}
			console.log("EqualTimeMap需要更新")
			EqualTimeMap.update_layer(map,selected.value,selected_days.value,selected_hours.value,distance.value);
		},
		{ deep: true }
	);

	watch(
		[selected_hours, selected_days],
		async () => {
			if (map.hasLayer(topologicLayer)) {
				console.log("TopologicMap需要更新")
				console.log(selected_days.value, selected_hours.value)
				topologicData.value = await draw_topological_graph_by_departure_time(selected_days.value, selected_hours.value);
				TopologicMap.update_layer(topologicData.value, map);
			}
		},
		{ deep: true }
	);


	watch(
		[selected_districts,order],
		async () => {
			console.log("TimeMap需要更新")
			console.log(selected_districts.value)
			console.log("order"+order.value)
			if(order.value == 0) {
				console.log(timemapData, selected_districts)
				timemapData.value = await traffic_flow_in_degree_graph(selected_districts.value);	
				// console.log(timemapData.value);
				// console.log("输出in order的tilemap");
			}
			else{
				timemapData.value = await traffic_flow_out_degree_graph(selected_districts.value);
				// console.log(timemapData.value);
				// console.log("输出out order的tilemap");
			}
		},
		{ deep: true }
	)

	
	watch(
		mouseovered_district,
		async () => {
			if (mouseovered_district.value == null) {
				districtLayer.eachLayer(function (layer) {
					console.log(layer.feature.properties.name);
					districtLayer.resetStyle(layer);
				});
				return;
			} else {
				districtLayer.eachLayer(function (layer) {
					if (layer.feature.properties.name == mouseovered_district.value) {
						layer.setStyle({
							weight: 5,
							color: '#666',
							dashArray: '',
							fillOpacity: 0.7
						});
					} else {
						districtLayer.resetStyle(layer);
					}
				});
			}
			// DistrictMap.highlightFeature(mouseovered_district.value);

		},
		{ deep: true }
	)



</script>


<template>
</template>

<style>
	.Equal_rects{
		rx:10;
		ry:10;
	}
	.Equal_rects[selected=false]{
		stroke: white;
		stroke-width: 0.3px;
		fill-opacity: 0.3;
		stroke-opacity: 0.3;
	}
	.Equal_rects[selected=true]{
		stroke: black;
		stroke-width: 1px;
		fill-opacity: 0.7;
		stroke-opacity: 0.7;
	}
	.Equal_texts{
		text-anchor: middle;
		font-size: 20px;
		font-weight: bold;
		fill: black;
	}
</style>