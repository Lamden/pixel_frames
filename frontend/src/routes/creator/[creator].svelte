<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params, query }) {
		const res = await this.fetch(`./creator/${params.creator}.json`)
		let data = await res.json()
		if (!data) data = []
	    return {created: data, creator: params.creator}
	}
</script>

<script>
    import Creator from "../../components/Creator.svelte";

	import { formatAccountAddress } from '../../js/utils'

    export let created
	export let creator
</script>

<svelte:head>
	<title>{`Pixel Frames created by ${formatAccountAddress(creator)}`}</title>
</svelte:head>

<Creator {created} {creator}/>