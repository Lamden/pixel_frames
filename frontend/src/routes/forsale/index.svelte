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
		const res = await this.fetch(`${config.blockExplorer[env]}/things/forsale`, options)
		let data = await res.json()
		if (!data) data = []
	    return {forsale: data}
	}
</script>

<script>
    import ForSale from '../../components/ForSale.svelte'

    export let forsale;

</script>

<ForSale {forsale}/>