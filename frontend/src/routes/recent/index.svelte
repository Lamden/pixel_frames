<script context="module">
	export async function preload(parms) {
		let things = await this.fetch(`./recent_things.json?limit=25`).then(res => res.json())

	    return {
			recent: things
		}}
</script>

<script>
    import Recent from '../../components/Recent.svelte'

    export let recent;

</script>

<svelte:head>
	<title>Pixel Whale Recent NFT Creations!</title>
</svelte:head>

<Recent {recent}/>