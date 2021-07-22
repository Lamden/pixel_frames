<!-- /frontend/src/routes/index.svelte -->
<script context="module">
	export async function preload() {
		let data = await Promise.all([
			this.fetch(`./mostliked.json?limit=54`).then(res => res.json()),
			this.fetch(`./recent_things.json?limit=10`).then(res => res.json()),
			this.fetch(`./forsale.json?limit=10`).then(res => res.json())
		])
		return {
			mostLiked: data[0],
			recent: data[1],
			forsale: data[2]
		}
	}
</script>

<script>
	import {onMount} from 'svelte'

	// Components
	import Title from "../components/Title.svelte";
	import PixelWall from '../components/PixelWall.svelte';
	import Recent from '../components/Recent.svelte';
	import ForSale from '../components/ForSale.svelte';
	import ArtistEvent from "../components/ArtistEvent.svelte";


	export let mostLiked;
	export let recent;
	export let forsale;


</script>

<style>
	*{
		text-align: center;
	}
	.release-date{
		margin: 2rem 0 0;
		font-size: 3rem;
    	font-weight: 200;
		color: var(--primary-dark);
    	text-shadow: 2px 2px #c3c3c3;
	}
	.hide-mobile{
		margin: 3rem auto;
	}
	@media (min-width: 450px) {
		.mobile-message{
			display: none;
		}
		.release-date{
			margin: 2rem 0 -4rem;
		}
	}
</style>

<svelte:head>
	<title>Pixel Whale: On-chain NFT Animations!</title>
</svelte:head>

<div class="hide-mobile">
	<Title fontSize={8} showFullLogo={true}/>
</div>

<div class="mobile-message">
	<strong>This site is not mobile optimized.</strong>>
	Please visit us on a desktop for the full experience including integration with the Lamden Wallet to enable
	<strong>buying, selling and creating custom NFT pixel animations!</strong>
</div>
<ArtistEvent />
<PixelWall {mostLiked}/>
<Recent {recent} preview={true}/>
<ForSale {forsale} preview={true}/>
