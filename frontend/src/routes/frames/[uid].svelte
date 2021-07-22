<script context="module">
	import { decodeFrames } from '../../js/utils.js'

	export async function preload({ params, query }) {
		let data = await Promise.all([
				this.fetch(`./frames/${params.uid}.json`).then(res => res.json()),
				this.fetch(`./history/${params.uid}.json`).then(res => res.json())
		])

		let { thingInfo, auctionInfo } = data[0]

		try{
			thingInfo.frames = decodeFrames(thingInfo.thing)
		}catch(e){
			thingInfo = {
				name: "Not Found",
				owner: "",
				uid: params.uid,
				description: "",
				notFound: true
			}
		}

	    return {
			thingInfo,
			auctionInfo,
			salesHistory: data[1]
		}
	}
</script>

<script>
	// Components
	import DisplayFramesOne from "../../components/DisplayFramesOne.svelte";

	// MISC
    import { updateInfo} from '../../js/utils.js'
	import { config } from '../../js/config.js'

	export let thingInfo
	export let auctionInfo
	export let salesHistory

	console.log({thingInfo, auctionInfo})

	let gifURL = `${config.domainName}/gif/${thingInfo.uid}.gif`

	const updateThingInfo = (updates) => {
    	thingInfo = updateInfo(thingInfo, updates)
    }

</script>

<style>
	.display-one{
        max-width: 75em;
        margin: 0 auto;
    }

</style>


	<svelte:head>
		<title>{thingInfo.name}</title>

		<meta name="twitter:card" content="summary" />
		<meta name="twitter:title" content="{thingInfo.name}" />
		<meta name="twitter:description" content="{thingInfo.description}" />
		<meta name="twitter:site" content="@framespixel" />
		<meta name="twitter:creator" content="{thingInfo.owner}" />
		<meta name="twitter:image" content="{gifURL}" />
		<meta name="twitter:image:alt" content="{thingInfo.name}" />

		<meta property="og:url" content="{gifURL}" />
		<meta property="og:type" content="article" />
		<meta property="og:title" content="Pixel Whale by Lamden" />
		<meta property="og:image" content="{gifURL}" />
		<meta property="og:description" content="{thingInfo.description}" />
		<meta property="og:image:url" content="{gifURL}" />
		<meta property="og:image:secure_url" content="{gifURL}" />
		<meta property="og:image:width" content="150" />
		<meta property="og:image:height" content="150" />
		<meta property="og:image:type" content="image/gif" />
	</svelte:head>

{#if typeof thingInfo.notFound === 'undefined'}
	<div class="display-one">
		<DisplayFramesOne {thingInfo} {auctionInfo} {salesHistory} updateInfo={updateThingInfo}/>
	</div>
{:else}
	<p>{`${thingInfo.uid} doesn't exist.`}</p>
{/if}