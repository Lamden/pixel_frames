<script context="module">
	import { config } from '../../js/config.js'
	import { decodeFrames } from '../../js/utils.js'
	export async function preload({ params, query }) {
		const res = await this.fetch(`${config.blockExplorer}/things/${config.infoContract}/${params.uid}`)
		let data = await res.json()

		if (!data) data = null
		else {
			data.frames = decodeFrames(data.thing)
		}
	    return {thingInfo: data}
	}
</script>

<script>
	import DisplayFramesOne from "../../components/DisplayFramesOne.svelte";
	import OwnerControls from "../../components/OwnerControls.svelte";
	import { userAccount } from '../../js/stores.js'

    import { formatAccountAddress, updateInfo} from '../../js/utils.js'

	export let thingInfo

	let gifURL = `${config.domainName}/dynamic/${thingInfo.uid}.gif`
	let pageURL = `${config.domainName}/frames/${thingInfo.uid}`

	$: owner = $userAccount === thingInfo.owner;

    let watermark = {
        text: formatAccountAddress(thingInfo.owner, 6, 3),
        fillColor: "#ff5bb0",
        font: "30px Roboto",
    }

	const updateThingInfo = (updates) => {
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
	<!--<meta name="twitter:image" content="{gifURL}" />-->
	<meta name="twitter:image:alt" content="{thingInfo.name}" />

	<!--<meta property="og:url" content="{gifURL}" />-->
	<meta property="og:type" content="article" />
	<meta property="og:title" content="Pixel Frames by Lamden" />
	<!--<meta property="og:image" content="{gifURL}" />-->
	<meta property="og:description" content="{thingInfo.description}" />
	<!--<meta property="og:image:url" content="{gifURL}" />-->
	<!--<meta property="og:image:secure_url" content="{gifURL}" />-->
	<!--<meta property="og:image:width" content="150" />-->
	<!--<meta property="og:image:height" content="150" />-->
	<!--<meta property="og:image:type" content="image/gif" />-->
</svelte:head>

<div class="display-one">

	<DisplayFramesOne {thingInfo} watermark={!owner ? watermark : undefined} updateInfo={updateThingInfo}/>
	{#if owner}
		<OwnerControls {thingInfo}/>
	{/if}
</div>
