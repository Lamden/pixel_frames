<script context="module">

</script>

<script>
	// Components
	import PixelWall from './PixelWall.svelte'
	import Auctions from './Auctions.svelte'

	// Misc
	import {getTimeAgo, getTimeTo} from "../js/utils";
	import { auctions } from "../js/stores";

	//auctions.subscribe(curr => console.log(curr))

	export let eventInfo

	$: endDate = new Date(eventInfo.endDate)
	$: eventInfoType = eventInfo.eventType
	$: eventAuctions = eventInfoType === "auction" ? getAuctions(eventInfo.artList, $auctions) : null
	$: eventHasEnded = endDate < new Date()
	$: eventHasStarted = new Date() > new Date(eventInfo.startDate)

	function getAuctions(eventInfoAuctions, storeAuctions){
		return storeAuctions.filter(f => {
			let found = eventInfoAuctions.find(auction => auction === f.uid)
			return found ? true : false
		})
	}

	const sortLastUpdated = (auctionList) => {
		return auctionList.sort((a, b) => a.last_tx_uid < b.last_tx_uid ? 1 : -1)
	}

	const removeSold = (artList) => {
		return artList.filter(f => f.owner === eventInfo.artistVk)
	}
	const soldList = (artList) => {
		return artList.filter(f => f.owner !== eventInfo.artistVk)
	}
</script>

<style>
	.container{
		width: 100%;
		border-top: 5px dotted var(--primary);
		border-bottom: 5px dotted var(--primary);
		padding: 3rem 0;
		margin: 4rem 0;
	}
	.gallery{
		margin: 3rem 0;
	}
	h1 > strong{
		color: var(--primary-highlight);
		font-weight: 600;
		font-size: 1.5em;
	}
	h3.artist-info{
		margin: 0 0 2rem;
	}
	img{
		display: block;
		width: 100%;
		margin: 1rem auto 1rem;
	}
	p{
		text-align: center;
		display: block;
		margin: 1rem auto;
		font-size: 1.2em;
		color: var(--primary-dark);
	}
	.time{
		font-size: 25px;
		font-weight: 500;
	}
</style>

<div class="container">
	<img src="{`/img/events/${eventInfo.image}`}" alt="event announcement" />
	<div class="gallery">
		<PixelWall mostLiked={eventInfo.artThingList} />
	</div>

	{#if !eventHasStarted}
		<h3 class="text-color-primary time">
			{`Event Starts ${new Date(eventInfo.startDate).toLocaleString()} (${getTimeTo(new Date(eventInfo.startDate))})`}
		</h3>
	{:else}
		{#if !eventHasEnded}
			<h3 class="text-color-primary time">
				{`Event Ends ${new Date(eventInfo.endDate).toLocaleString()} (${getTimeTo(new Date(eventInfo.endDate))})`}
			</h3>
		{:else}
			<h3 class="text-color-primary time">
				{`Event Ended ${new Date(eventInfo.endDate).toLocaleString()} ( ${getTimeAgo(new Date(eventInfo.endDate), true)})`}
			</h3>
		{/if}
	{/if}
	<h3 class="text-color-primary-dark artist-info"><strong>{eventInfo.name}</strong> by <a href="{`./creator/${eventInfo.artistVk}`}">{eventInfo.artistName}</a></h3>

	{#if eventAuctions}
		<Auctions auctions={sortLastUpdated(eventAuctions)} title={false} showMore={false} />
	{/if}
</div>
