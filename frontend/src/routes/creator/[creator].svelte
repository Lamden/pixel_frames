<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params, query }) {
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				contractName: 'con_pf_test',
				variableName: 'S'
			})
		}
		const res = await this.fetch(`${config.blockExplorer}/things/created/${params.creator}`, options)
		let data = await res.json()
		if (!data) data = []
	    return {created: data, creator: params.creator}
	}
</script>

<script>
    import Creator from "../../components/Creator.svelte";

    export let created
	export let creator
</script>

<Creator {created} {creator}/>