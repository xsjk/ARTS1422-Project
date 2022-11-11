 <script setup>
  import HeatmapOverlay from 'heatmap.js/plugins/leaflet-heatmap'
  import L from 'leaflet'
  import D3Wrapper from './d3/D3Wrapper.vue';
  import { computed, defineProps } from 'vue';
  import * as d3 from 'd3';
  import { svg } from 'd3';
  
  const props = defineProps({
    Data: {
      type: Object,
      required: true,
    },
    width: {
      type: [Number, String],
      default: null,
    },
    height: {
      type: [Number, String],
      default: null,
    },
  });
	// if (width === null) {
	//   width = columns * (rectWidth + 2 * rectMargin + textWidth);
	// }

	// if (height === null) {
	//   height = rows * (rectHeight + 2 * rectMargin);
	// }
	
	
	const heatmap = computed(() => {
		let {
		  Data,
		  width,
		  height,
		} = props;
		var heatmapLayer = null;

		// 配置
		var cfg = {
		  'radius': 20,
		  'maxOpacity': 1,
		  'scaleRadius': true,
		  'useLocalExtrema': true,
		  latField: 'lat',
		  lngField: 'lng',
		  valueField: 'count'
		}
		heatmapLayer = new HeatmapOverlay(cfg)
		// 图层
		let baseLayer = L.tileLayer(
		  'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: 'Haut-Gis-Org © OpenStreetMap'
		  }
		)
		
		const svg = d3.create('map');
		
		const map = L.map('map', {
		  center: [50.75, -1.55],
		  zoom: 10
		})
		baseLayer.addTo(map)
		heatmapLayer.addTo(map)
		heatmapLayer.setData(Data)

		L.control.scale({ maxWidth: 200, metric: true, imperial: false }).addTo(map)

		let baseLayers = {
		  'heatmapLayer': heatmapLayer,
		  'OpenStreetMap': baseLayer
		}

		L.control.layers(baseLayers).addTo(map)
		console.log(1234);
		return svg.node();
	})
</script>

<template>
	<D3Wrapper :node="heatmap" />
</template>

<style>
	.leaflet-container {
		height: 400px;
		width: 600px;
		max-width: 100%;
		max-height: 100%;
	}
</style>