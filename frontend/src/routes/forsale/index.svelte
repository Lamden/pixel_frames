<script context="module">
	import { config } from '../../js/config.js'
	export async function preload(parms) {
		const res = await this.fetch(`${config.blockExplorer}/things/${config.infoContract}/forsale?limit=15`)
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