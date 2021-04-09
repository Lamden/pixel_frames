<script context="module">
	import { decodeFrames } from '../../js/utils.js'

	export async function preload({ params, query }) {
		let thingInfo = null
		let data = await Promise.all([
				this.fetch(`./frames/${params.uid}.json`).then(res => res.json()),
				this.fetch(`./history/${params.uid}.json`).then(res => res.json())
		])
		try{
			thingInfo = data[0]
			thingInfo.frames = decodeFrames(thingInfo.thing)
		}catch(e){null}

	    return {
			thingInfo,
			salesHistory: data[1]
		}
	}
</script>

<script>
	import { config } from '../../js/config.js'
	import DisplayFramesOne from "../../components/DisplayFramesOne.svelte";
	import OwnerControls from "../../components/OwnerControls.svelte";
	import { userAccount } from '../../js/stores.js'

    import { formatAccountAddress, updateInfo} from '../../js/utils.js'

	export let thingInfo
	export let salesHistory

	let gifURL = `${config.domainName}/dynamic/${thingInfo.uid}.gif`
	let pageURL = `${config.domainName}/frames/${thingInfo.uid}`

	const updateThingInfo = (updates) => {
    	console.log(updates)
    	updateInfo(thingInfo, updates)
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
	<meta property="og:title" content="Pixel Frames by Lamden" />
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
