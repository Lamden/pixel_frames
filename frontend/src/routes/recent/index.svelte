<script context="module">
	import { config } from '../../js/config.js'
	export async function preload(parms) {
		const res = await this.fetch(`${config.blockExplorer}/things/${config.infoContract}/recent?limit=15`)
		let data = await res.json()
		if (!data) data = []
	    return {recent: data}
	}
</script>

<script>
    import Recent from '../../components/Recent.svelte'

    export let recent;

</script>

<Recent {recent}/>