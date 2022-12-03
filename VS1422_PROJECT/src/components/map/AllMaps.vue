<script setup>
	import Heatmap from './heatmap.vue'
	import Districtmap from './district_division.vue'
	import { nextTick, ref, watch } from 'vue';
	import { getUUID } from '../../composables/utils/uuid.js';
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
	const test = ref(null);
	const uuid = getUUID();
	function UpdateMaps() {
		Heatmap.methods.update_layer(props.date, props.time, props.center, props.scale);
		console.log(11111111111);
		test.value = 0;
	}
	nextTick(() => {
	  UpdateMaps();
	});
	watch(
	  () => props.scale,
	  () => {
		UpdateMaps();
	  },
	);	
</script>

<template>
	<div ref="test"></div>
</template>

<style>
</style>