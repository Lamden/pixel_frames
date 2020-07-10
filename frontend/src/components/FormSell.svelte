<script>
    import { getContext } from 'svelte'
	import { frames, showModal } from '../js/stores.js'
	import { createSnack } from '../js/utils.js'
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	let price = $showModal.modalData.thingInfo.price;

    const sell = () => {
    	console.log($showModal)
		const transaction = {
			methodName: 'sell_thing',
			networkType: 'testnet',
			stampLimit: 100000,
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid,
				amount: parseInt(price)
			}
		}
		//sendTransaction(transaction)

        console.log(transaction)
		sendTransaction(transaction)

		createSnack(
			"Submitting Transaction",
			"Please approve the Lamden Wallet transaction popup.",
			"info"
		)

        showModal.set({modalData:{}, show: false})
    }
</script>

<style>
	.flex-row{
		align-items: center;
		justify-content: space-evenly;
		height: 100%;
	}
	.preview-row{
		text-align: center;
	}

	.button_text{
		color: white;
	}
	.outlined:hover{
		color: #ff5bb0;
	}

</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15}/>
		{/if}
		<input type="submit" class="button_text outlined" value="List Item" form="sell" />
	</div>
	<form id="sell" class="flex-col" on:submit|preventDefault={sell}>
		<label for="price">How much does your Pixel Frame cost?</label>
		<input id="price" type="number" min="1" required bind:value={price}/>
	</form>
</div>
