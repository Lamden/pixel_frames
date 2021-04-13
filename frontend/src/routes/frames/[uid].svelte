<script context="module">
	import { decodeFrames } from '../../js/utils.js'
	import { goto } from '@sapper/app';

	export async function preload({ params, query }) {
		let thingInfo = null
		let data = await Promise.all([
				this.fetch(`./frames/${params.uid}.json`).then(res => res.json()),
				this.fetch(`./history/${params.uid}.json`).then(res => res.json())
		])
		try{
			thingInfo = data[0]
			thingInfo.frames = decodeFrames(thingInfo.thing)
		}catch(e){
			goto("./404")
		}

	    return {
			thingInfo,
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
	export let salesHistory

	let gifURL = `${config.domainName}/gif/${thingInfo.uid}.gif`
	let pageURL = `${config.domainName}/frames/${thingInfo.uid}`

	const updateThingInfo = (updates) => {
    	//console.log(updates)
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

<div class="display-one">
	<DisplayFramesOne {thingInfo} {salesHistory} updateInfo={updateThingInfo}/>
</div>
