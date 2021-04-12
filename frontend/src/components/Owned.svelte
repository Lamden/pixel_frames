<script>
    import { onMount, beforeUpdate } from 'svelte'
    import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    import DisplayFrames from './DisplayFrames.svelte';

    import { formatThings, updateInfo, dedupArray, formatAccountAddress, isLamdenKey } from "../js/utils.js";
    import { userAccount } from '../js/stores'
	import { config } from '../js/config'

    export let owned;
    export let account;

    let count = owned.count
    let sending = false;
    let scrollHeight;
	let innerHeight;

    $: formatted = !owned.data ? [] : formatThings(owned.data)
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
		const res = await fetch(`./owned/${account}.json?limit=25&offset=${formatted.length}`)
		let things = await res.json()
		if (!things.data) things.data = []
		sending = false;
		formatted = dedupArray([...formatted, ...formatThings(things.data)])
		if (things.count) count = things.count
	}

    const updateThing = (e) => {
    	const { updates, index } = e.detail
    	updateInfo(formatted[index], updates)
		formatted = [...formatted]
	}

</script>

<style>
	h2{
		border-top: 1px solid lightgray;
		padding-top: 1rem;
		margin-top: 2rem;
	}
    p{
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
	a{
		color: var(--primary);
	}
</style>

<h2 class="text-color-primary-dark">
	All NFTs owned by
	{#if isLamdenKey(account)}
		<a href="{`${config.blockExplorer}/addresses/${account}`}" >{formatAccountAddress(account, 8, 5)}</a>
	{:else}
		{account.length > 15 && !account.startsWith("con_") ? formatAccountAddress(account, 8, 5) : account}
	{/if}
</h2>

{#if formatted.length == 0}
	<p>
		{`${account === $userAccount ? "You don't" : "This user doesn't"} own anything yet!`}
	</p>
{/if}

<div class="flex-row display-card">
    {#each formatted as thingInfo, index}
		{#if thingInfo.blacklist && thingInfo.owner !== $userAccount}

		{:else}
			<div in:scale="{{duration: 200, delay: 0, opacity: 0, start: 0.75, easing: quintOut}}"
				bind:this={elements[index]}>
				<DisplayFrames pixelSize={7} {thingInfo} {index} on:update={updateThing}/>
        	</div>
		{/if}
    {/each}
</div>

<svelte:window bind:scrollY={scrollHeight} bind:innerHeight={innerHeight} on:scroll={checkGetMore}/>