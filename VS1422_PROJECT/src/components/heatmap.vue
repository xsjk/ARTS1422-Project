 <script>
	import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap'
	import L from 'leaflet'
	//import D3Wrapper from './d3/D3Wrapper.vue';
	import { computed, defineProps } from 'vue';
	import * as d3 from 'd3';
	import { svg } from 'd3';
	export default{
		methods:{
			generate_layer(Data){
					// 配置
					var cfg = {
					  'radius': 0.008,
					  'maxOpacity': 0.8,
					  'scaleRadius': true,
					  'useLocalExtrema': true,
					  latField: 'lat',
					  lngField: 'lng',
					  valueField: 'count'
					}
					// if(heatmapLayer != null){
					// 	map.removeLayer(heatmapLayer);
					// }
					var heatmapLayer = null
					heatmapLayer = new HeatmapOverlay(cfg)
					heatmapLayer.setData(Data)
					return heatmapLayer;
					
				}
			}
		}
</script>

<template>
	<!-- <D3Wrapper :node="heatmap" /> -->
</template>

<!-- /* <style>
	.leaflet-container {
		height: 400px;
		width: 600px;
		max-width: 100%;
		max-height: 100%;
	}
</style> */ -->