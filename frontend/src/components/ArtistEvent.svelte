<script context="module">

</script>

<script>
	import {onMount} from 'svelte'

	// Components
	import PixelWall from './PixelWall.svelte'
	import Auctions from './Auctions.svelte'

	// Misc
	import { getTimeAgo, getTimeTo } from "../js/utils";

	let eventInfo = null
	let auctions = undefined

	$:  eventHasEnded = true;
	$:  shouldShowEvent = false;
	$:  eventHasStarted = false;
	$:  announceStarted = false;

	onMount(async () => {
		let res = await fetch(`./getArtistEvent.json?event=artist`).then(res => res.json())
		try{
			let endDate = new Date(res.endDate)
			eventHasEnded = endDate < new Date()
			shouldShowEvent = new Date() <= endDate.setDate(endDate.getDate() + 3)

			if (shouldShowEvent){
				announceStarted = new Date() > new Date(res.announceDate)
				eventHasStarted = new Date() > new Date(res.startDate)
				eventInfo = res
				console.log({eventInfo})
				if (eventInfo.eventType === "auction") auctions = eventInfo.auctions
			}
		}catch (e){
			console.log(e)
		}
	})

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
	h1 > strong{
		color: var(--primary-highlight);
		font-weight: 600;
		font-size: 1.5em;
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
	p.subtitle{
		display: block;
		margin: 1rem auto;
		font-weight: 200;
		color: var(--primary-dark);
	}
	.sold{
		color: var(--primary);
		font-size: 2em;
		font-weight: bold;
		margin-bottom: 0rem;
	}
	.time{
		font-size: 25px;
		font-weight: 500;
	}
</style>

{#if eventInfo && announceStarted}
	<div class="container">
		<img src="{`/img/events/${eventInfo.image}`}" alt="event announcement" />
		<h3 class="text-color-primary-dark"><strong>{eventInfo.name}</strong> by <a href="{`./creator/${eventInfo.artistVk}`}">{eventInfo.artistName}</a></h3>
		<div class="gallery">
			<PixelWall mostLiked={soldList(eventInfo.artThingList)} />
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

		{#if eventInfo.eventType === "auction" && auctions}
			<Auctions {auctions} title={false}/>
		{/if}
	</div>
{/if}