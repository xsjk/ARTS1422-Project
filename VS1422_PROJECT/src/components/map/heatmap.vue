 <script>
	import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap'
	import L from 'leaflet'
	//import D3Wrapper from './d3/D3Wrapper.vue';
	import { computed, defineProps } from 'vue';
	import * as d3 from 'd3';
	import { svg } from 'd3';
	export default{
		data(){
			return{
				heatmapLayer, 
				radius_max,
			}	
		},
		methods:{
			generate_layer(Data){
					// 配置
					this.radius_max = 0.015;
					var cfg = {
					  'radius': this.radius_max,
					  'maxOpacity': 0.8,
					  'scaleRadius': true,
					  //'useLocalExtrema': true,
					  latField: 'lat',
					  lngField: 'lng',
					  valueField: 'count'
					}
					// if(heatmapLayer != null){
					// 	map.removeLayer(heatmapLayer);
					// }
					this.heatmapLayer = new HeatmapOverlay(cfg)
					this.heatmapLayer.setData(Data)
					return this.heatmapLayer;
			},
			async update_layer(date, time, center_arr, scale){
				var heatmapTest = await out_degree(date, time, center_arr, Math.pow(2,scale-11));
				var radius = 0;
				var days = (date.length!=0 ? date.length:183); 
				var hours = (time.length!=0 ? time.length:24); 
				radius = 0.03*Math.pow(2,10-scale);	
				console.log(days);
				console.log(hours);
				console.log(radius);
				console.log(heatmapTest);
				console.log(500*days*hours*Math.pow(2,10-scale));
				const Data = {
				  max: 432*days*hours*Math.pow(2,10-scale),
				  data: heatmapTest
				};
				this.heatmapLayer.cfg.radius = radius;
				this.heatmapLayer.setData(Data);	
				return ;
			}
		}
	}
</script>

<template>
	<!-- <D3Wrapper :node="heatmap" /> -->
</template>
