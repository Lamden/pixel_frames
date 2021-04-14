

<script>
	import { onMount, beforeUpdate } from 'svelte'
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

	import DisplayFrames from './DisplayFrames.svelte';
	import { formatThings, updateInfo, dedupArray } from "../js/utils";
	import { config } from '../js/config.js'
	import { userAccount } from '../js/stores.js'

	export let forsale;

	export let preview = false;

    let count = forsale.count;
    let sending = false;

	let scrollHeight;
	let innerHeight;

	$: formatted = !forsale.data ? [] : formatThings(forsale.data)
	$: elements = []
	$: lastElementTop = elements.length > 0 ? elements[elements.length -1].offsetTop: null
	$: lastElementOffsetHeight = elements.length > 0 ? elements[elements.length -1].offsetHeight: null
	$: visibleHeight = scrollHeight + innerHeight
	$: checker = checkGetMore(elements)

	const checkGetMore = () => {
    	if (lastElementTop === null || lastElementOffsetHeight === null) return
		if (visibleHeight > lastElementTop - (lastElementOffsetHeight * 4)) getMore()
	}

    const getMore = async () => {
		if (count === formatted.length) return
    	if (sending) return;
		sending = true;
		const res = await fetch(`./forsale.json?limit=25&offset=${formatted.length}`)
		let things = await res.json()
		
		if (!things.data) return

		sending = false;

		formatted = dedupArray([...formatted, ...formatThings(things.data)])

		if (things.count) count = things.count
	}

	const updateThing = (e) => {
    	const { updates, index } = e.detail
    	updateInfo(formatted[index], updates)
		formatted = [...formatted].filter(thing => thing['price_amount'] > 0)
	}

</script>

<style>
	h2{
		border-top: 1px solid lightgray;
		padding-top: 1rem;
		margin-top: 2rem;
	}
	button, a{
		max-width: fit-content;
		padding: 10px 20px;
    	margin: 0 auto;
	}
	.owned{
        border: 2px dashed var(--primary);
    }
</style>

<h2 class="text-color-primary-dark">NFTs For Sale!</h2>
<div class="flex-row display-card">
    {#each formatted as thingInfo, index}
		<div class:owned={$userAccount ? thingInfo.owner === $userAccount : false}
			 in:scale="{{duration: 200, delay: 0, opacity: 0, start: 0.75, easing: quintOut}}"
			bind:this={elements[index]}>
			<DisplayFrames pixelSize={7} {thingInfo} {index} title={false} on:update={updateThing}/>
		</div>
    {/each}

</div>
{#if preview}
	<a class="button" rel=prefetch href="{'forsale'}">SEE MORE</a>
{:else}
	<!--<button disabled={sending} class="button" on:click={getMore}> GET MORE </button>-->
{/if}

<svelte:window bind:scrollY={scrollHeight} bind:innerHeight={innerHeight} on:scroll={checkGetMore}/>