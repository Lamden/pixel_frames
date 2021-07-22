
<script>
	// Components
	import Auctions from '../../components/Auctions.svelte'

	// Misc
    import { auctions } from '../../js/stores'

</script>

<svelte:head>
	<title>Pixel Whale NFT Auctions!</title>
</svelte:head>

<Auctions auctions={$auctions} />