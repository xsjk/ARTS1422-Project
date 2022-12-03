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
				radius_max:0.001,
			}	
		},
		methods:{
			generate_layer(Data){
					// 配置
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
			async update_layer(scale, date, time, center_arr){
				var heatmapTest = await out_degree(date, time, center_arr, Math.pow(2,scale-11));
				var radius = 0;
				if(scale <= 13){
					radius = this.radius_max - 0.001*Math.pow(2,scale-11);	
				}else{
					radius = 0.001 - 0.0005;
				}
				console.log(scale);
				console.log(radius);
				const Data = {
				  max: heatmapTest.max,
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
