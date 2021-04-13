<script>
    import { getContext, onMount } from 'svelte'

	// Misc
	import { frames, showModal } from '../js/stores.js'
	import { createSnack, closeModel, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config } from '../js/config.js';

	// Components
	import Preview from './Preview.svelte'

	let inputElm

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
	const currentSellPrice = $showModal.modalData.thingInfo['price_amount']
    const thingName = $showModal.modalData.thingInfo['name']
	const royalty_percent = $showModal.modalData.thingInfo['royalty_percent']
	const thingInfo = $showModal.modalData.thingInfo

	$: price = toBigNumber("0")
	$: royaltyAmount = toBigNumber(price).multipliedBy(royalty_percent / 100)
	$: netAmount = toBigNumber(price).minus(royaltyAmount)
	$: isOwner = thingInfo.owner === thingInfo.creator

	onMount(() => {
		console.log($showModal.modalData.thingInfo)
		console.log(currentSellPrice)
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
        if (txResults.data.txBlockResult.status === 0) {
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
	p{
		color: var(--color-white-primary-tint);
		margin: 1rem 0 0 ;
		font-weight: 600;
	}
	strong {
		color: var(--primary-dark);
		font-weight: 600;
		font-size: 1.3em;
		margin-left: 8px;
	}

</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		<input type="submit" class="button_text outlined" value="List NFT!" form="sell" disabled="{price.isLessThanOrEqualTo(0) || price.isEqualTo(currentSellPrice)}"/>
	</div>
	<div class="flex-col">
		<form id="sell" class="flex-col" on:submit|preventDefault={sell}>
			<label for="price">How much does this NFT cost?</label>
			<input id="price" type="number" step="0.1" required bind:this={inputElm} on:input={handleInput}/>

		{#if !isOwner}
			<p>Royalty Percentage </p>
			<strong>{royalty_percent}%</strong>
			<p>Royalty Amount </p>
			<strong>{`${stringToFixed(royaltyAmount, 8)} ${config.currencySymbol}`}</strong>
			<p>You Get </p>
			<strong>{`${stringToFixed(netAmount, 8)} ${config.currencySymbol}`}</strong>
		{/if}
		</form>
	</div>
</div>
