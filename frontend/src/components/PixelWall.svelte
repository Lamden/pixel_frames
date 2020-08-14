

<script>
	import Preview from './Preview.svelte';
	import { formatThings  } from "../js/utils";
	import { config } from '../js/config.js'

	export let mostLiked;
	let sending = false;

    let formatted = formatThings (mostLiked);

</script>

<style>
	.pixelwall {
		width: 100%;
		padding: 2rem 0;
		flex-wrap: wrap;
		box-sizing: border-box;
		justify-content: center;
	}
</style>

<div class="flex-row pixelwall">
    {#each formatted as thingInfo}
		<a rel=prefetch href="{'frames/' + thingInfo.uid}">
			<Preview frames={thingInfo.frames} pixelSize={5} {thingInfo} showWatermark={false} border={false}/>
		</a>
    {/each}
</div>