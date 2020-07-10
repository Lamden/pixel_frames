<script context="module">
	import { config } from '../../js/config.js'
	export async function preload(parms) {
		let env = process.env.NODE_ENV
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
		const res = await this.fetch(`${config.blockExplorer[env]}/things/recent`, options)
		let data = await res.json()
		if (!data) data = []
	    return {recent: data}
	}
</script>

<script>
	import { afterUpdate } from 'svelte'
    import Recent from '../../components/Recent.svelte'

    export let recent;

</script>

<Recent {recent}/>