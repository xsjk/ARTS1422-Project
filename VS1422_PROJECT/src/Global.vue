<script>

	import { ref } from 'vue'
	// global reference variables
	export const weatherData = ref([]);
	export const timemapData = ref([[],[]]);
	export const equaltimeData = ref([]);
	export const topologicData = ref([]);

	export const mousehold = ref(false);
	export const keyhold = ref(false);

	export const selected_days = ref([]);
	export const selected_hours = ref([]);
	export const selected_districts = ref([]);

	export const temp_days = ref([]);
	export const temp_hours = ref([]);
</script>



<style>
</style>