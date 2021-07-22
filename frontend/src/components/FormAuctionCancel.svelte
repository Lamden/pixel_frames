<script>
    import { getContext } from 'svelte'

	// Misc
	import {  showModal, currency, userAccount, stampRatio } from '../js/stores.js'
	import { createSnack, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Icons
	import IconPixelCancel from '../icons/pixelCancel.svelte'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const auctionInfo = $showModal.modalData.auctionInfo
	const thingInfo = $showModal.modalData.thingInfo

	const uid = auctionInfo.uid
	const thingName = thingInfo.name

	const hasEnded  = $showModal.modalData.end_info.hasEnded
	const end_early  = $showModal.modalData.end_info.end_early
	const winning_bid = $showModal.modalData.end_info.bid
	const bid_winner = $showModal.modalData.end_info.bidder

	$: userIsWinner = $userAccount === bid_winner
	$: endAuctionTxStamps_to_tau = toBigNumber(stampLimits[config.auctionContract].end_auction).dividedBy($stampRatio)

	$: buttonText = getButtonText(endAuctionTxStamps_to_tau, $currency, $userAccount)

	function getButtonText(){
		if (!endAuctionTxStamps_to_tau) return "Loading"
    	if (endAuctionTxStamps_to_tau.isGreaterThan($currency)) return `INSUFFICIENT ${config.currencySymbol}`
		return `CANCEL AUCTION`
	}

    const endAuction = () => {
		const transaction = {
			contractName: config.auctionContract,
			methodName: 'end_auction',
			networkType: config.networkType,
			kwargs: {
				uid,
				end_early
			}
		}

		sendTransaction(transaction, handleEndAuctionTx)
		closeModel()
    }


	const checkPrice = () => {
    	if (endAuctionTxStamps_to_tau.isGreaterThan($currency)){
			createSnack({
                title: `Insufficient ${config.currencySymbol}`,
                body: `
                	You need ${stringToFixed(endAuctionTxStamps_to_tau, 4)} ${config.currencySymbol} to pay the transaction fees.`,
                type: "error"
            })
		}else{
    		endAuction();
		}
	}

	const handleEndAuctionTx = () => {
		createSnack({
			title: `NFT Cancelled!`,
			body: `"${thingName}" has been returned to you.`,
			type: "success",
			delay: 8000,
			thingInfo
		})
    }
</script>

<style>
	form{
		color: var(--color-white-primary-tint);
		padding: 1rem;
		max-width: 650px;
	}
	.title{
		font-size: 25px;
		font-weight: 900;
		letter-spacing: 1.5px;
		margin-bottom: 1rem;
		margin-top: 0;
	}
	.name{
		font-size: 20px;
		font-weight: 600;
		margin: 1rem auto;
		padding: 0.5rem;
		border: 1px dashed var(--gray-6);
		width: 100%;
		text-align: center;
		box-sizing: border-box;
		border-radius: 5px;
	}
	.subtitle{
		margin: 0 0 0.5rem;
    	font-size: 20px;
	}
	.outlined{
		color: var(--color-white-primary-tint);
		margin-bottom: 1rem;
	}
	.outlined:disabled {
		background: var(--primary-dark);
		color: var(--gray-2);
	}
	.model-badge-circle{
		position: absolute;
		width: 75px;
		height: 75px;
		right: -15px;
		top: -15px;
		background: white;
		border-radius: 99px;
		margin-top: 0px;
		border: 2px solid var(--primary-dark);
	}
	.model-badge-icon{
		position: relative;
		width: fit-content;
	}
	input[type="submit"]{
		padding: 1rem;
		margin-bottom: 0;
	}
	.action{
		margin-top: 2rem;
	}

</style>

{#if $showModal.modalData.thingInfo}
	<div class="model-badge-circle flex flex-center-center">
		<div class="model-badge-icon">
			<IconPixelCancel width="40" color="var(--primary-dark)" margin="5px 0 0"/>
		</div>
	</div>
	<form id="end-auction" class="flex-col" on:submit|preventDefault={checkPrice}>

		<p class="title text-color-primary-dark">Cancel Auction</p>
		<p class="name text-color-primary-dark">{thingInfo.name}</p>
		<p class="subtitle">
			Your reserve price of
			<strong>{stringToFixed(auctionInfo.reserve_price, 8)} {config.currencySymbol}</strong>
			was not met. Cancelling the auction will refund the highest bid and return the NFT to you.
		</p>
		<p class="text-color-primary-dark action"><strong>Click the CANCEL</strong> button below to send the transaction.</p>

		<input
			type="submit"
			class="button_text outlined"
			disabled={endAuctionTxStamps_to_tau.isGreaterThan($currency)}
			value={buttonText}
			form="end-auction"
		/>
	</form>
{/if}