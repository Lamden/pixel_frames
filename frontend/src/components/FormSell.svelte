<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal } from '../js/stores.js'
	import { createSnack, closeModel } from '../js/utils.js'
	import { config } from '../js/config.js';

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
	let price = $showModal.modalData.thingInfo['price_amount'];
    const thingName = $showModal.modalData.thingInfo['name']

    const sell = () => {
		const transaction = {
			methodName: 'sell_thing',
			networkType: config.networkType,
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid,
				amount: parseInt(price)
			}
		}

		sendTransaction(transaction, handleSellTx)
        closeModel()
    }

	const handleSellTx = (txResults) => {
    	console.log(txResults)
        if (txResults.data.txBlockResult.status === 0) {
        	updateInfo({
				"price_amount": price,
        	})
			createSnack({
				title: `Listed!`,
				body: `${thingName} now listed for ${price}.`,
				type: "info"
			})
		}
    }
</script>

<style>
	.preview-row{
		text-align: center;
	}

	.button_text{
		color: #ffffff;
	}
	.outlined:hover{
		color: var(--primary);
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
