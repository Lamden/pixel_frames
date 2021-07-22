<script>
    import { getContext } from 'svelte'

	// Misc
	import {  showModal, currency, userAccount, stampRatio } from '../js/stores.js'
	import {createSnack, closeModel, toBigNumber, stringToFixed, formatAccountAddress} from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Icons
	import IconTrophy from '../icons/trophy.svelte'

	// Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const auctionInfo = $showModal.modalData.auctionInfo
	const thingInfo = $showModal.modalData.thingInfo

	const uid = auctionInfo.uid
	const thingName = thingInfo.name

	const hasEnded  = $showModal.modalData.end_info.hasEnded
	const winning_bid = $showModal.modalData.end_info.bid
	const bid_winner = $showModal.modalData.end_info.bidder
	const claim = $showModal.modalData.end_info.claim
	const reserveMet = $showModal.modalData.end_info.reserveMet

	$: userIsWinner = $userAccount === bid_winner
	$: endAuctionTxStamps_to_tau = toBigNumber(stampLimits[config.auctionContract].end_auction).dividedBy($stampRatio)

	$: buttonText = getButtonText(endAuctionTxStamps_to_tau, $currency, $userAccount)

	function getButtonText(){
		if (!endAuctionTxStamps_to_tau) return "Loading"
    	if (endAuctionTxStamps_to_tau.isGreaterThan($currency)) return `INSUFFICIENT ${config.currencySymbol}`
		return claim ? `CLAIM NFT` : 'RESOLVE AUCTION'
	}

    const endAuction = () => {
		const transaction = {
			contractName: config.auctionContract,
			methodName: 'end_auction',
			networkType: config.networkType,
			kwargs: {
				uid,
				end_early: false
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
    	if (claim){
			createSnack({
				title: `NFT Claimed!`,
				body: `You are now the owner of ${thingName}.`,
				type: "info",
				thingInfo
			})
		}else{
    		if (reserveMet){
				createSnack({
					title: `Auction Resolved`,
					body: `You have sent ${thingName} to ${formatAccountAddress(bid_winner, 8, 4)}.`,
					type: "info",
					thingInfo
				})
			}else{
				createSnack({
					title: `Auction Resolved`,
					body: `You have sent ${thingName} to ${formatAccountAddress(auctionInfo.old_owner, 8, 4)}.`,
					type: "info",
					thingInfo
				})
			}
		}

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
			<IconTrophy width="30" color="var(--primary-dark)" margin="3px 0 0"/>
		</div>
	</div>
	<form id="end-auction" class="flex-col" on:submit|preventDefault={checkPrice}>
		{#if userIsWinner }
			<p class="title text-color-primary-dark">Congratulations!</p>
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
			{:else}
			<p class="title text-color-primary-dark">Resolve Auction</p>
			{#if reserveMet}
				<p class="subtitle">
					Resolving this auction will send the <strong>"{thingName}"</strong> NFT to the winner <strong>{formatAccountAddress(bid_winner, 8, 4)}</strong> ,
					pay the auction creator as well as any royalties to the NFT artist.
				</p>
				<p class="subtitle">
					The winner of the auction has the option to claim the NFT themselves, which will also resolve the
					auction in the same way.  This process lets you do it for them, if you choose.
				</p>
			{:else}
				<p class="subtitle">
					The reserve price for this auction was not met.
				</p>

				<p class="subtitle">
					Resolving this auction will send the <strong>"{thingName}"</strong> NFT back to the user that listed it.
					It will also refund the highest bid back to that user.
				</p>
			{/if}
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

			<p class="text-color-primary-dark action"><strong>Click the RESOLVE</strong> button below to send a transaction to resolve this auction.</p>
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