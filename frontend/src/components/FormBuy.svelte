<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal, currency, userAccount, approvalAmount } from '../js/stores.js'
	import { createSnack, checkForApproval, closeModel } from '../js/utils.js'
	import { config } from '../js/config.js'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo

	const uid = $showModal.modalData.thingInfo.uid
	const price = parseFloat($showModal.modalData.thingInfo['price_amount'])
	const thingName = $showModal.modalData.thingInfo['name']

    const buy = () => {
		const transaction = {
			methodName: 'buy_thing',
			networkType: config.networkType,
			kwargs: {
				uid
			}
		}

		sendTransaction(transaction, handleBuyTx)
		closeModel()
    }

	const approveBuy = () => {
		const transaction = {
			contractName: 'currency',
			methodName: 'approve',
			networkType: config.networkType,
			kwargs: {
				amount: {"__fixed__": "100000000"},
				to: config.masterContract
			}
		}

		sendTransaction(transaction, handleApproveTx)
		closeModel()
	}

	const checkPrice = () => {
    	if ($currency <=  price){
			createSnack({
                title: `Insufficient Funds ${config.currencySymbol}`,
                body: `You do not have enough ${config.currencySymbol} to complete this transfer.`,
                type: "error"
            })
		}else{
    		approveAndSend();
		}
	}

	const approveAndSend = async () => {
		checkForApproval().then((value) => {
			if ()
			console.log(value)/*
			if (value.isLessThan(price)){
				approveBuy();
			}else{
				buy();
			}*/
		})
	}

	const handleApproveTx = (txResults) => {
        if (txResults.data.txBlockResult.status === 0) {
        	buy()
        }
    }

	const handleBuyTx = (txResults) => {
        if (txResults.data.txBlockResult.status === 0) {
        	updateInfo({
				owner: $userAccount,
				"price_amount": "0",
        	})
			createSnack({
				title: `Purchased!`,
				body: `You are now the proud over of ${thingName}.`,
				type: "info"
			})
		}
    }

</script>

<style>
	.outlined{
		color: var(--color-white-primary-tint);
	}
	.outlined:disabled {
		background: var(--primary-dark);
		color: var(--gray-2);
	}
	.preview-row{
		align-items: center;
		height: 100%;
		justify-content: space-evenly;
	}
	textarea{
		resize: none;
	}
	input[type="text"], textarea{
		margin-bottom: 1rem;
	}
	.insufficient{

	}
</style>
{#if $showModal.modalData.thingInfo}
<div class="flex-row">
	<div class="flex-col preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		{#if $currency > $showModal.modalData.thingInfo['price_amount']}
			<input type="submit" class="button_text outlined" value={`Buy For ${$showModal.modalData.thingInfo['price_amount']} ${config.currencySymbol}`} form="buy" />
		{:else}
			<p class="button_text outlined insufficient">Insufficient {config.currencySymbol}</p>
		{/if}
	</div>
	<form id="buy" class="flex-col" on:submit|preventDefault={checkPrice}>
		<label for="name">Name</label>
		<input id="name" type="text" readonly value={$showModal.modalData.thingInfo.name}/>
		<label for="desc">Description</label>
		<textarea id="desc" type="textarea" rows="8" readonly value={$showModal.modalData.thingInfo.description}/>
	</form>
</div>
{/if}