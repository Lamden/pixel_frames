<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal, currency, userAccount, approvalAmount, stampRatio } from '../js/stores.js'
	import { createSnack, checkForApproval, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo

	const uid = $showModal.modalData.thingInfo.uid
	const price = toBigNumber($showModal.modalData.thingInfo['price_amount'])
	const approvalTxStamps_to_tau = price.isGreaterThan(toBigNumber($approvalAmount[config.masterContract])) ? toBigNumber(stampLimits.currency.approve).dividedBy($stampRatio) : toBigNumber(0)
	const buyTxStamps_to_tau = toBigNumber(stampLimits[config.masterContract].buy_thing).dividedBy($stampRatio)
	const total_tx_fees = approvalTxStamps_to_tau.plus(buyTxStamps_to_tau)
	const total_tau_to_buy = price.plus(total_tx_fees)
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
    	if (total_tau_to_buy.isGreaterThan($currency)){
			createSnack({
                title: `Insufficient ${config.currencySymbol}`,
                body: `
                	You need ${stringToFixed(total_tau_to_buy, 4)} ${config.currencySymbol} to buy this.
                	 ${stringToFixed(price, 4)} ${config.currencySymbol} plus ${stringToFixed(total_tau_to_buy, 4)} ${config.currencySymbol} for tx fees.`,
                type: "error"
            })
		}else{
    		approveAndSend();
		}
	}

	const approveAndSend = async () => {
		checkForApproval(config.masterContract).then((value) => {
			console.log(value)
			if (value.isLessThan(price)){
				approveBuy();
			}else{
				buy();
			}
		})
	}

	const handleApproveTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
        	buy()
        }
    }

	const handleBuyTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
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
			<input
				type="submit"
				class="button_text outlined"
				disabled={total_tau_to_buy.isGreaterThan($currency)}
				value={total_tau_to_buy.isGreaterThan($currency) ?
					`Insufficient ${config.currencySymbol}` :
					`Buy For ${stringToFixed(total_tau_to_buy, 4)} ${config.currencySymbol}`
				} form="buy" />
		</div>
		<form id="buy" class="flex-col" on:submit|preventDefault={checkPrice}>
			<label for="name">Name</label>
			<input id="name" type="text" readonly value={$showModal.modalData.thingInfo.name}/>
			<label for="desc">Description</label>
			<textarea id="desc" type="textarea" rows="8" readonly value={$showModal.modalData.thingInfo.description}/>
			<div class="tx-costs">
				<p>Transaction Cost</p>
				<strong>{`${stringToFixed(total_tx_fees, 4)} ${config.currencySymbol}`}</strong>
				<p>Total Cost</p>
				<strong>{`${stringToFixed(total_tau_to_buy, 4)} ${config.currencySymbol}`}</strong>
			</div>
		</form>
	</div>
{/if}