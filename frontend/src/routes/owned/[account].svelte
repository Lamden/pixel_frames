<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params, query }) {
		const res = await this.fetch(`${config.blockExplorer}/things/${config.infoContract}/owned/${params.account}`)
		let data = await res.json()
		if (!data) data = []
	    return {account: params.account, owned: data.data}
	}
</script>

<script>
    import Owned from "../../components/Owned.svelte";

    export let account
	export let owned

</script>

<Owned {owned} {account}/>


