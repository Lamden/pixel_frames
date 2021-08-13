

<script>
	import Preview from './Preview.svelte';
	import { formatThings  } from "../js/utils";

	export let mostLiked;
	let sending = false;

    let formatted = formatThings (mostLiked);

</script>

<style>
	.pixelwall {
		width: 100%;
		padding: 0;
		flex-wrap: wrap;
		box-sizing: border-box;
		justify-content: center;
	}
	@media (min-width: 400px) {
		.pixelwall {
			padding: 2rem 0;
		}
	}
</style>

<div class="flex-row pixelwall">
    {#each formatted as thingInfo (thingInfo.uid)}
		<a rel=prefetch href="{'frames/' + thingInfo.uid}">
			<Preview solidBorder={true} solidBorderColor="#00d6a22b" frames={thingInfo.frames} pixelSize={4} {thingInfo} showWatermark={false} border={false}/>
		</a>
    {/each}
</div>