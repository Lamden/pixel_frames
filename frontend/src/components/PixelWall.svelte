

<script>
	import { onMount } from 'svelte'
	import Preview from './Preview.svelte';
	import { formatThings  } from "../js/utils";
	import { config } from '../js/config.js'

	export let mostLiked;
	let sending = false;

	$: outerWidth = 0

    let formatted = formatThings (mostLiked);

	onMount(() => console.log({mostLiked}))

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
    {#each formatted as thingInfo}
		<a rel=prefetch href="{'frames/' + thingInfo.uid}">
			<Preview solidBorder={true} solidBorderColor="#00d6a22b" frames={thingInfo.frames} pixelSize={outerWidth > 400 ? 4 : 3} {thingInfo} showWatermark={false} border={false}/>
		</a>
    {/each}
</div>
<svelte:window bind:outerWidth />