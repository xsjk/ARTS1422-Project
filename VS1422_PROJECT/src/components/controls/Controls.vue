<template>
</template>

<script>
	import L from 'leaflet';
	import { can_move } from '../map/Maps.vue'
	L.Control.Order = L.Control.extend({
		options: {
			position: 'topright' //初始位置
		},
		initialize: function (options) {
			L.Util.extend(this.options, options);
		},
		onAdd: function (map) {
			//创建一个class为info legend的div
			this._container = L.DomUtil.create('select', 'order_selection');
			//创建一个图片要素	
			this._container.appendChild(new Option("in","in"));
			this._container.appendChild(new Option("out","out"));
			if (!L.Browser.touch) {
				L.DomEvent.disableClickPropagation(div);
				L.DomEvent.on(this._container, 'mousewheel', L.DomEvent.stopPropagation);
			} else {
				L.DomEvent.on(this._container, 'click', L.DomEvent.stopPropagation);
			}
			return this._container;
		},
		onRemove: function (map) {
			// Nothing to do here
			L.DomEvent.off();
		}
	});

	export default {
		methods:{
			L_control_order: function (opts) {
				return new L.Control.Order(opts);
			},	
		}
	}
	
	
</script>

<style>
</style>