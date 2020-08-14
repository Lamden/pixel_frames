<!-- /frontend/src/routes/index.svelte -->
<script context="module">
	import { config } from '../js/config.js'
	export async function preload() {
		let data = await Promise.all([
				this.fetch(`${config.blockExplorer}/things/${config.infoContract}/liked?limit=54`).then(res => res.json()),
				this.fetch(`${config.blockExplorer}/things/${config.infoContract}/recent?limit=5`).then(res => res.json()),
				this.fetch(`${config.blockExplorer}/things/${config.infoContract}/forsale?limit=5`).then(res => res.json())
		])
	    return {
			mostLiked: data[0].data,
			recent: data[1],
			forsale: data[2]
		}
	}
</script>

<script>
	//Components
	import Title from "../components/Title.svelte";
	import PixelWall from '../components/PixelWall.svelte';
	import Recent from '../components/Recent.svelte';
	import ForSale from '../components/ForSale.svelte';

	export let mostLiked;
	export let recent;
	export let forsale;

</script>

<style>
	*{
		text-align: center;
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

<div class="hide-mobile">
	<Title fontSize={8}/>
</div>


<div class="mobile-message">
	<strong>This site is not mobile optimized.</strong>>
	Please visit us on a desktop for the full experience including integration with the Lamden Wallet to enable
	<strong>buying, selling and creating Pixel Frames animations!</strong>
</div>

<PixelWall {mostLiked}/>
<Recent {recent} preview={true}/>
<ForSale {forsale} preview={true}/>