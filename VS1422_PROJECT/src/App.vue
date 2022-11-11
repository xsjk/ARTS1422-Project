<script setup>
import Heatmap from './components/heatmap.vue'
import { ref } from 'vue';
import * as d3 from 'd3';
var testData = {
  max: 8,
  data: [{ lat: 24.6408, lng: 46.7728, count: 3 },
	{ lat: 50.75, lng: -1.55, count: 1 },
	{ lat: 51.55, lng: -1.55, count: 9 },
	{ lat: 52.65, lng: -1.45, count: 8 },
	{ lat: 53.45, lng: -1.35, count: 7 },
	{ lat: 54.35, lng: -1.25, count: 6 },
	{ lat: 5.25, lng: -1.15, count: 5 }
  ]
}

</script>

<template>
	<div id = "map"></div>
	<div class="v-main">
	  <div class="d-flex justify-center pb-16">
	    <div class="pt-8">
	      <Heatmap
			:Data = "testData"
		  />
	      <div class="text-center text-h5">Heatmap</div>
		</div>
	  </div>
	</div>
</template>

<style>

</style>
