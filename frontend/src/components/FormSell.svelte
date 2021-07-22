<script>
    import { getContext, onMount } from 'svelte'

	// Misc
	import { frames, showModal, stampRatio, currency } from '../js/stores.js'
	import { createSnack, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js';

	// Components
	import Preview from './Preview.svelte'

	let inputElm

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
	const currentSellPrice = $showModal.modalData.thingInfo['price_amount']
    const thingName = $showModal.modalData.thingInfo['name']
	const royalty_percent = $showModal.modalData.thingInfo['royalty_percent']
	const thingInfo = $showModal.modalData.thingInfo

	const sellTxStamps_to_tau = toBigNumber(stampLimits[config.masterContract].sell_thing).dividedBy($stampRatio)


	$: price = toBigNumber("0")
	$: royaltyAmount = toBigNumber(price).multipliedBy(royalty_percent / 100)
	$: netAmount = toBigNumber(price).minus(royaltyAmount)
	$: isOwner = thingInfo.owner === thingInfo.creator

	onMount(() => {
		inputElm.value = toBigNumber(stringToFixed(currentSellPrice, 8))
		price = toBigNumber(inputElm.value)
	})

    const sell = () => {
		const transaction = {
			methodName: 'sell_thing',
			networkType: config.networkType,
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid,
				amount: {"__fixed__": price}
			}
		}

		sendTransaction(transaction, handleSellTx)
        closeModel()
    }

	const handleSellTx = (txResults) => {
    	console.log(txResults)
        if (txResults.txBlockResult.status === 0) {
        	updateInfo({
				"price_amount": price,
        	})
			createSnack({
				title: `Listed!`,
				body: `${thingName} now listed for ${price} ${config.currencySymbol}.`,
				type: "info"
			})
		}
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
			price = value
		}
	}
</script>

<style>
	label{
		font-weight: 600;
	}
	input[type="number"]{
		margin-bottom: 1rem;
	}
	.preview-row{
		text-align: center;
	}
	.outlined{
		color: var(--color-white-primary-tint);
	}
	.outlined:disabled {
		background: var(--primary-dark);
		color: var(--gray-2);
	}
	.royalty-calcs > p{
		color: var(--color-white-primary-tint);
		margin: 1rem 0 0 ;
		font-weight: 600;
	}
	.royalty-calcs > strong {
		color: var(--primary-dark);
		font-weight: 600;
	}

</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		<input
			type="submit"
			form="sell"
			class="button_text outlined"
			disabled={sellTxStamps_to_tau.isGreaterThan($currency) && (price.isLessThanOrEqualTo(0) || price.isEqualTo(currentSellPrice))}
			value={sellTxStamps_to_tau.isGreaterThan($currency) ? `Insufficient ${config.currencySymbol}`: "List NFT!"}
		/>
	</div>
	<div class="flex-col">
		<form id="sell" class="flex-col" on:submit|preventDefault={sell}>
			<label for="price">How much does this NFT cost?</label>
			<input id="price" type="number" step="0.1" required bind:this={inputElm} on:input={handleInput}/>
			<div class="tx-costs">
				<p>Transaction Cost</p>
				<strong>{`${stringToFixed(sellTxStamps_to_tau, 4)} ${config.currencySymbol}`}</strong>
			</div>

		{#if isOwner}
			<div class="royalty-calcs">
				<p>Royalty Percentage </p>
				<strong>{royalty_percent}%</strong>
				<p>Royalty Amount </p>
				<strong>{`${stringToFixed(royaltyAmount, 8)} ${config.currencySymbol}`}</strong>
				<p>You Get </p>
				<strong>{`${stringToFixed(netAmount, 8)} ${config.currencySymbol}`}</strong>
			</div>
		{/if}
		</form>
	</div>
</div>
