<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal, currency, userAccount, approvalAmount, stampRatio } from '../js/stores.js'
	import { createSnack, checkForApproval, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')
	let inputElm

	const auctionInfo = $showModal.modalData.auctionInfo
	const thingInfo = $showModal.modalData.thingInfo || auctionInfo.thingInfo

	const uid = auctionInfo.uid
	const thingName = thingInfo.name

	$: bidAmount = $showModal.modalData.winning_bid ? $showModal.modalData.winning_bid.plus(1) : toBigNumber(1)
	$: approvalTxStamps_to_tau = bidAmount.isGreaterThan(toBigNumber($approvalAmount[config.masterContract])) ? toBigNumber(stampLimits.currency.approve).dividedBy($stampRatio) : toBigNumber(0)
	$: bidTxStamps_to_tau = toBigNumber(stampLimits[config.auctionContract].bid).dividedBy($stampRatio)
	$: total_tx_fees = approvalTxStamps_to_tau.plus(bidTxStamps_to_tau)
	$: total_tau_to_bid = bidAmount.plus(total_tx_fees)

	$: buttonText = getButtonText(bidAmount)

	function getButtonText(amount){
    	if (amount.isGreaterThan($currency)) return `Insufficient ${config.currencySymbol}`
		if (amount.isLessThanOrEqualTo($showModal.modalData.winning_bid)) return "Bid is too low"

		return `Bid ${stringToFixed(amount, 4)} ${config.currencySymbol}`
	}

    const bid = () => {
		const transaction = {
			contractName: config.auctionContract,
			methodName: 'bid',
			networkType: config.networkType,
			kwargs: {
				uid,
				bid_amount: {__fixed__: bidAmount.toString()}
			}
		}

		sendTransaction(transaction, handleBidTx)
		closeModel()
    }

	const approveBid = () => {
		const transaction = {
			contractName: 'currency',
			methodName: 'approve',
			networkType: config.networkType,
			kwargs: {
				amount: {"__fixed__": "100000000"},
				to: config.auctionContract
			}
		}

		sendTransaction(transaction, handleApproveTx)
		closeModel()
	}

	const checkPrice = () => {
    	if (total_tau_to_bid.isGreaterThan($currency)){
			createSnack({
                title: `Insufficient ${config.currencySymbol}`,
                body: `
                	You need ${stringToFixed(total_tau_to_bid, 4)} ${config.currencySymbol} to bid for this.
                	 ${stringToFixed(bidAmount, 4)} ${config.currencySymbol} plus ${stringToFixed(total_tau_to_bid, 4)} ${config.currencySymbol} for tx fees.`,
                type: "error"
            })
		}else{
    		approveAndSend();
		}
	}

	const approveAndSend = async () => {
		checkForApproval(config.auctionContract).then((value) => {
			console.log(value)
			if (value.isLessThan(bidAmount)){
				approveBid();
			}else{
				bid();
			}
		})
	}

	const handleApproveTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
        	bid()
        }
    }

	const handleBidTx = () => {
		createSnack({
			title: `Bid Accepted!`,
			body: `You are now the highest bidder on ${thingName}.`,
			type: "info"
		})
    }

	const handleInput = (e) => {
		let validateValue = e.target.value.replace(/[^0-9.]/g, '').replace(/(\..*?)\..*/g, '$1')
		if (validateValue !== e.target.value) {
			inputElm.value = validateValue
		}else{
			let value = toBigNumber(e.target.value)
			if (value.isNaN()) value = toBigNumber("0")
			value = toBigNumber(stringToFixed(value, 8))
			inputElm.value = stringToFixed(value, 8)
			bidAmount = value
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
	input[type="submit"]{
		margin-top: auto;
		width: 100%;
	}
	form{
		height: 379px;
		justify-content: flex-start;
	}

</style>

{#if $showModal.modalData.thingInfo}
	<div class="flex-row">
		<div class="flex-col preview-row">
			{#if $showModal.modalData.thingInfo}
				<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
			{/if}
		</div>
		<form id="bid" class="flex-col" on:submit|preventDefault={checkPrice}>
			<label for="name">Name</label>
			<input id="name" type="text" readonly value={$showModal.modalData.thingInfo.name}/>

			<label for="desc">Description</label>
			<textarea id="desc" type="textarea" rows="5" readonly value={$showModal.modalData.thingInfo.description}/>

			<label for="bid_amount">How much to bid?</label>
			<input id="bid_amount" type="number" step="0.1" autofocus required bind:this={inputElm} on:input={handleInput} value={bidAmount.toString()} />
			<input
				type="submit"
				class="button_text outlined"
				disabled={bidAmount.isGreaterThan($currency) || bidAmount.isLessThanOrEqualTo($showModal.modalData.winning_bid)}
				value={buttonText} form="bid" />
		</form>
	</div>
{/if}