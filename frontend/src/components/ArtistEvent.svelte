<script context="module">

</script>

<script>
	import {onMount} from 'svelte'

	import PixelWall from './PixelWall.svelte'
    let eventInfo = null

	let eventStarted = false;

	onMount(async () => {
		let res = await fetch(`./getArtistEvent.json?event=artist`).then(res => res.json())
		try{
			if (new Date() <= new Date(res.endDate)){
				eventStarted = new Date() > new Date(res.startDate)
				eventInfo = res
			}
		}catch (e){}
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
		margin-bottom: 3rem;
	}
	h1 > strong{
		color: var(--primary-highlight);
		font-weight: 600;
		font-size: 1.5em;
	}
	h2{
		border-top: 0pc;
		padding-top: 1rem;
		margin-top: 2rem;
	}
	h3{
		color: var(--primary);

	}
	img{
		display: block;
		width: 100%;
		max-width: 750px;
		margin: 2rem auto 1rem;
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
</style>

{#if eventInfo}
	<div class="container">
		<h2>
			{eventStarted ? "An Artist Event is going on!"  :"Upcoming Artist Event!"}
		</h2>
		<h3><strong>{eventInfo.name}</strong> by <a href="{`./creator/${eventInfo.artistVk}`}">{eventInfo.artistName}</a></h3>
		<img src="{`/img/events/${eventInfo.image}`}" alt="event announcement" />
		<p>ALL WHALES WELCOME!</p>
		{#if eventStarted}
			<p>ON SALE NOW! Select NFT for price!</p>
		{:else}
			<p>Buy these collectables starting on {new Date(eventInfo.startDate).toLocaleString()} (your local time)</p>
		{/if}
		<p class="subtitle">Prices reduced by 500 TAU every hour until the collection is SOLD!</p>
		<div>
			<PixelWall mostLiked={removeSold(eventInfo.artList)} />
		</div>
		{#if eventStarted}
			<p class="sold">SOLD!</p>
			<div class="gallery">
				<PixelWall mostLiked={soldList(eventInfo.artList)} />
			</div>
		{/if}
	</div>
{/if}