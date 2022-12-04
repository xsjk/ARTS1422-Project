<script>

import { ref } from 'vue'
export const center = ref([110.355043, 20.004658]);
export const scale = ref(10);
export const selected = ref([]);

</script>

<script setup>
	import * as HeatMap from '../../composables/layers/heatmap';
	import * as DistrictMap from '../../composables/layers/district_division'
	import * as EqualTimeMap from '../../composables/layers/equal_time'
	import { watch } from 'vue';
	import { hours, dates } from '../d3/Calendar.vue';

	import * as d3 from 'd3';
	import L from 'leaflet';

	import { weatherData, timemapData, equaltimeData } from '../../Global.vue';

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
	const getData = async () => {
	  const weatherTest = await d3.csv('weatherData.csv');
	  weatherData.value = weatherTest.map(d => d);
	  timemapData.value = [[0.1,0.2],[0.3,0.4]]
	  equaltimeData.value = [0.028758452380954324, 0.02031264526842589, 0.03360677895017247, 0.04200094409784688, 0.03459567830588102, 0.0, 0.0, 0.0, 0.0, 0.025049999999993133, 0.03703024779237924, 0.05582818807481003, 0.028591562079811773, 0.02556251189854171, 0.020557370556213986, 0.04941435904157133, 0.06827150819941265, 0.03244533622005591];
	};
	getData()

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
	const satellite = L.tileLayer(mbUrl, {id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	const baseLayers = {
		'Basemap': osm,
		'Streets': streets,
		'Dark': dark,
		'Satellite': satellite
	};
	
	let heatmapLayer = HeatMap.generate_layer(testData);
		heatmapLayer.cfg.radius = 0.001;
		
	const map = L.map('map', {
		center: [center.value[1], center.value[0]],
		zoom: scale.value,
		renderer: L.svg(),
		layers: [streets, heatmapLayer]
	})

	let districtLayer = DistrictMap.generate_layer(data, map);
	let equaltimeLayer = EqualTimeMap.generate_layer(equaltimeData.value, map);


	map.on('click', async(e) => {
		console.log(e);
		L.popup()
			.setLatLng(e.latlng)
			.setContent(`${e.latlng.toString()}`)
			.openOn(map);
		selected.value = [e.latlng.lng, e.latlng.lat];
	});


	map.on('zoomend', async(e) => {
		console.log(e);
		scale.value = e.target.getZoom();
	});

	map.on('mouseup', async(e) => {
		var center = e.target.getCenter();
		center.value = [center.lng, center.lat];
	});


	/// control
	L.control.scale({ maxWidth: 200, metric: true, imperial: false }).addTo(map)
	let mixed = {
		'districtLayer': districtLayer,
		'heatmapLayer': heatmapLayer,
		'equaltimeLayer': equaltimeLayer,
	}
	L.control.layers(baseLayers, mixed).addTo(map);
	


	// watch

	watch(
		[hours, dates, center, scale],
		async () => {
			console.log("HeatMap需要更新")
			HeatMap.update_layer(dates.value, hours.value, center.value, scale.value);

		},
		{ deep: true }
	);

	watch(
		[hours, dates, selected],
		async () => {
			console.log("EqualTimeMap需要更新")
			equaltimeData.value = await k_min_isochrone([10, 15], selected.value, dates.value, hours.value)
			EqualTimeMap.update_layer(equaltimeData.value, map);
		},
		{ deep: true }
	)



</script>


<template>
	<!-- <div id="map"></div> -->
</template>

<style>
</style>