<script context="module">
	export async function preload() {
		const res = await this.fetch(`./auctionsAll.json?limit=25`)
		let data = await res.json()
		if (!data) data = []
	    return {auctions: data}
	}
</script>

<script>
    import Auctions from '../../components/Auctions.svelte'

    export let auctions;
</script>

<svelte:head>
	<title>Pixel Whale NFT Auctions!</title>
</svelte:head>

<Auctions {auctions} />