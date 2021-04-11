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
	import { onMount } from 'svelte'
	//Components
	import Title from "../components/Title.svelte";
	import PixelWall from '../components/PixelWall.svelte';
	import Recent from '../components/Recent.svelte';
	import ForSale from '../components/ForSale.svelte';

	export let mostLiked;
	export let recent;
	export let forsale;

	onMount(() => {
		/*
		fetch(`./frames/3cb59ca68fd7b0e80bae79bc59ce073b4d969888586e0a76be96bc6949cf2a7c.json`)
		.then(res => res.json()).then(res => console.log(res))
		fetch(`./recent_things.json?limit=15`)
		.then(res => res.json()).then(res => console.log(res))
		fetch(`./liked.json?limit=54`)
		.then(res => res.json()).then(res => console.log(res))
		fetch(`./forsale.json`)
		.then(res => res.json()).then(res => console.log(res))
		fetch(`./owned/bc73cd44616b734a89bf44ab81fa580b9cc5b29ef9640b828e8bce919d48fb79.json/`)
		.then(res => res.json()).then(res => console.log(res))
		*/
	})

</script>

<style>
	*{
		text-align: center;
	}
	.release-date{
		margin: 2rem 0 -4rem;
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

	}
</style>

<svelte:head>
	<title>Pixel Whale: On-chain Animations!</title>
</svelte:head>

<p class="release-date">Official Release April 19th @ 22:00 UTC</p>
<div class="hide-mobile">
	<Title fontSize={8}/>
</div>


<div class="mobile-message">
	<strong>This site is not mobile optimized.</strong>>
	Please visit us on a desktop for the full experience including integration with the Lamden Wallet to enable
	<strong>buying, selling and creating custom artwork!</strong>
</div>

<PixelWall {mostLiked}/>
<Recent {recent} preview={true}/>
<ForSale {forsale} preview={true}/>
