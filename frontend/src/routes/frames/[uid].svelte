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

	export let thingInfo

</script>

<DisplayFramesOne {thingInfo}/>