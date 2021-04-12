<script context="module">
	export async function preload() {
		const res = await this.fetch(`./forsale.json?limit=25`)
		let data = await res.json()
		if (!data) data = []
	    return {forsale: data}
	}
</script>

<script>
    import ForSale from '../../components/ForSale.svelte'

    export let forsale;
</script>

<svelte:head>
	<title>Pixel Whale NFTs For Sale!</title>
</svelte:head>

<ForSale {forsale}/>