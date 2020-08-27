<script>
    import { getContext } from 'svelte'
	import { frames, showModal } from '../js/stores.js'
	import { createSnack, closeModel } from '../js/utils.js'
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
	let price = $showModal.modalData.thingInfo['price:amount'];
    const thingName = $showModal.modalData.thingInfo['name']

    const sell = () => {
		const transaction = {
			methodName: 'sell_thing',
			networkType: 'testnet',
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid,
				amount: parseInt(price)
			}
		}

		sendTransaction(transaction, handleSellTx)
        closeModel()
    }

	const handleSellTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
        	updateInfo({
				"price:amount": price,
        	})
			createSnack({
				title: `Listed!`,
				body: `${thingName} now listred for ${price}.`,
				type: "info"
			})
		}
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
		color: #ffffff;
	}
	.outlined:hover{
		color: #ff5bb0;
	}

</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		<input type="submit" class="button_text outlined" value="List Item" form="sell" />
	</div>
	<form id="sell" class="flex-col" on:submit|preventDefault={sell}>
		<label for="price">How much does your Pixel Frame cost?</label>
		<input id="price" type="number" min="1" required bind:value={price}/>
	</form>
</div>
