<script>
    import { getContext } from 'svelte'
	import { frames, showModal } from '../js/stores.js'
	import { createSnack } from '../js/utils.js'
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

    const buy = () => {
		const transaction = {
			methodName: 'buy_thing',
			networkType: 'testnet',
			stampLimit: 100000,
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid
			}
		}

		sendTransaction(transaction)

		createSnack(
			`Buying ${$showModal.modalData.thingInfo.name}!`,
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
	textarea{
		resize: none;
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
		<input type="submit" class="button_text outlined" value={`Buy For ${$showModal.modalData.thingInfo['price:amount']} dTAU`} form="buy" />
	</div>
	<form id="buy" class="flex-col" on:submit|preventDefault={buy}>
		<label for="name">Name</label>
		<input id="name" type="text" readonly value={$showModal.modalData.thingInfo.name}/>
		<label for="desc">Description</label>
		<textarea id="desc" type="textarea" rows="8" readonly value={$showModal.modalData.thingInfo.description}/>
	</form>
</div>
