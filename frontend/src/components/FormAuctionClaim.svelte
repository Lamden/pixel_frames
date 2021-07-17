<script>
    import { getContext } from 'svelte'

	// Misc
	import {  showModal, currency, userAccount, stampRatio } from '../js/stores.js'
	import { createSnack, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Icons
	import IconTrophy from '../icons/trophy.svelte'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const auctionInfo = $showModal.modalData.auctionInfo
	const thingInfo = auctionInfo.thingInfo

	const uid = auctionInfo.uid
	const thingName = thingInfo.name

	const hasEnded  = $showModal.modalData.end_info.hasEnded
	const winning_bid = $showModal.modalData.end_info.bid
	const bid_winner = $showModal.modalData.end_info.bidder

	$: userIsWinner = $userAccount === bid_winner
	$: endAuctionTxStamps_to_tau = toBigNumber(stampLimits[config.auctionContract].end_auction).dividedBy($stampRatio)

	$: buttonText = getButtonText(endAuctionTxStamps_to_tau)

	function getButtonText(){
		if (!endAuctionTxStamps_to_tau) return "Loading"
    	if (endAuctionTxStamps_to_tau.isGreaterThan($currency)) return `Insufficient ${config.currencySymbol}`
		return `CLAIM NFT`
	}

    const endAuction = () => {
		const transaction = {
			contractName: config.auctionContract,
			methodName: 'end_auction',
			networkType: config.networkType,
			kwargs: {
				uid
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
			title: `NFT Claimed!`,
			body: `You are now the owner of ${thingName}.`,
			type: "info",
			thingInfo
		})
    }
</script>

<style>
	form{
		color: var(--color-white-primary-tint);
		padding: 0;
	}
	.title{
		font-size: 25px;
		font-weight: 900;
		letter-spacing: 1.5px;
		margin-bottom: 1rem;
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
	.preview{
		margin: 1rem auto;
	}

</style>

{#if $showModal.modalData.thingInfo}
	<div class="model-badge-circle flex flex-center-center">
		<div class="model-badge-icon">
			<IconTrophy width="30" color="var(--primary-dark)" margin="3px 0 0"/>
		</div>
	</div>
	<form id="end-auction" class="flex-col" on:submit|preventDefault={checkPrice}>
		{#if userIsWinner }
			<p class="title">Congratulations!</p>
			<p class="subtitle">You have won the auction for the <strong>{thingName}</strong> NFT!</p>
			<div class="preview">
				<Preview
						solidBorder={true}
						solidBorderColor="#00d6a22b"
						frames={thingInfo.frames}
						pixelSize={4}
						thingInfo={thingInfo}
						showWatermark={false} border={false}
				/>
			</div>

			<p><strong>Click the CLAIM</strong> button below to send a transaction to claim your NFT.</p>
		{/if}

		<input
			type="submit"
			class="button_text outlined"
			disabled={endAuctionTxStamps_to_tau.isGreaterThan($currency)}
			value={buttonText}
			form="end-auction"
		/>
	</form>
{/if}