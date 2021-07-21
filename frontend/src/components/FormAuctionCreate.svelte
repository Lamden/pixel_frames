<script>
    import { getContext, onMount } from 'svelte'

	// Misc
	import {  showModal, currency, stampRatio } from '../js/stores.js'
	import {
		createSnack,
		closeModel,
		toBigNumber,
		stringToFixed,
		toDateTime,
		checkForAuctionApproval
	} from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js'

	// Components
	import DatePicker from "@beyonk/svelte-datepicker/src/components/DatePicker.svelte";
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')
	let inputElm

	const thingInfo = $showModal.modalData.thingInfo

	const uid = thingInfo.uid
	const thingName = thingInfo.name

	let endDate = new Date()
	let dateRange

	$: hasApproval = false
	$: endDate = new Date()
	$: reserve_price = toBigNumber("0")
	$: thingApprovalTxStamps_to_tau = toBigNumber(stampLimits[config.masterContract].approve).dividedBy($stampRatio)
	$: createAuctionTxStamps_to_tau = toBigNumber(stampLimits[config.auctionContract].auction_thing).dividedBy($stampRatio)
	$: total_tx_fees = hasApproval ? createAuctionTxStamps_to_tau : thingApprovalTxStamps_to_tau.plus(createAuctionTxStamps_to_tau)
	$: buttonText = getButtonText(total_tx_fees, dateRange)

	onMount(() => {
		checkForAuctionApproval(uid).then((value) => hasApproval = value)
	})

	function getButtonText(amount, dateRange){
		if (!dateRange) return 'Choose Auction Dates'

		const { from, to } = dateRange
    	if (new Date(to) < new Date() ) return `End Date has past`

		return `Create Auction`
	}

	function setDateRange(e){
		dateRange = e.detail
		console.log(dateRange)
	}

	function fixMonth(datetime){
		datetime.__time__[1] = datetime.__time__[1] + 1
		console.log({datetime})
		return datetime
	}

    const auction_thing = () => {
		const transaction = {
			contractName: config.auctionContract,
			methodName: 'auction_thing',
			networkType: config.networkType,
			kwargs: {
				uid,
				reserve_price: {__fixed__: reserve_price.toString()},
				start_date: fixMonth(toDateTime(dateRange.from)),
				end_date: fixMonth(toDateTime(dateRange.to))
			}
		}

		sendTransaction(transaction, handleBidTx)
		closeModel()
    }

	const approveThing = () => {
		const transaction = {
			contractName: config.masterContract,
			methodName: 'approve',
			networkType: config.networkType,
			kwargs: {
				uid: thingInfo.uid,
				to: config.auctionContract
			}
		}

		sendTransaction(transaction, handleApproveTx)
		closeModel()
	}

	const checkPrice = () => {
    	if (total_tx_fees.isGreaterThan($currency)){
			createSnack({
                title: `Insufficient ${config.currencySymbol}`,
                body: `You need ${stringToFixed(total_tx_fees, 4)} ${config.currencySymbol} to list this NFT to pay the transaction fees.`,
                type: "error"
            })
		}else{
    		approveAndSend();
		}
	}

	const approveAndSend = async () => {
		checkForAuctionApproval(uid).then((value) => {
			console.log({value})
			if (!value){
				approveThing();
			}else{
				auction_thing();
			}
		})
	}

	const handleApproveTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
        	auction_thing()
        }
    }

	const handleBidTx = () => {
		createSnack({
			title: `Auction Created!`,
			body: `Good Luck!`,
			type: "info",
			thingInfo
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
			reserve_price = value
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
	:global(.contents-wrapper){
		top: 50px!important;
		left: 50px!important;
	}
	:global(.time-container){
		box-sizing: border-box;
	}
	:global(.datepicker){
		--highlight-color: var(--primary)!important;
		--passive-highlight-color: var(--primary-highlight)!important;
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

			<label for="bid_amount">Reserve Amount</label>
			<input id="bid_amount" type="number" step="0.1" autofocus required bind:this={inputElm} on:input={handleInput} value={0}/>

			<label for="bid_amount">Auction End Date</label>
			<DatePicker range={true} time={true} on:range-selected={setDateRange}/>
			<input
				type="submit"
				class="button_text outlined"
				disabled={buttonText !== "Create Auction"}
				value={buttonText} form="bid" />
		</form>
	</div>
{/if}