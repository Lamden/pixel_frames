<script>
	// Components
	import Auction from './Auction.svelte';

	export let auctions;
	export let title = true;
	export let preview = false;
	export let showMore = true;

	$: auctionList = preview ? [...auctions.slice(0, 10)] : auctions

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
</style>

{#if title}
	<h2 class="text-color-primary-dark">NFTs Auctions!</h2>
{/if}

<div class="flex-row flex-wrap flex-justify-spaceevenly">
	{#each auctionList as auctionInfo, index (auctionInfo.thingInfo.uid)}
		{#if auctionInfo.thingInfo}
			<Auction {auctionInfo} thingInfo={auctionInfo.thingInfo} id={auctionInfo.thingInfo.uid}/>
		{/if}
	{/each}
</div>


{#if showMore}
	<a class="button" rel=prefetch href="{'auctions'}">SEE MORE</a>
{:else}
	<!--<button disabled={sending} class="button" on:click={getMore}> GET MORE </button>-->
{/if}