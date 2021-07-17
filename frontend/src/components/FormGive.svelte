<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal, stampRatio, currency } from '../js/stores.js'
	import { createSnack, closeModel, isLamdenKey, toBigNumber, stringToFixed } from '../js/utils.js'
	import { config, stampLimits } from '../js/config.js';

    // Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
    const thingName = $showModal.modalData.thingInfo['name']
	const transferTxStamps_to_tau = toBigNumber(stampLimits[config.masterContract].transfer).dividedBy($stampRatio)

	let recipient = ""
	let inputElm
	let sendTime

	const checkRecipient = (e) => {
		//console.log(e.target)
		//console.log(!isLamdenKey(recipient.trim()))
		if (!isLamdenKey(recipient.trim())) inputElm.setCustomValidity("Not a proper Lamden Address")
		else {
			inputElm.setCustomValidity("")
			give()
		}
		inputElm.reportValidity()
		return false
	}

    const give = () => {
		const transaction = {
			methodName: 'transfer',
			networkType: config.networkType,
			kwargs: {
				uid: $showModal.modalData.thingInfo.uid,
				new_owner: recipient.trim()
			}
		}
		sendTransaction(transaction, handleGiveTx)
		sendTime = new Date()
        closeModel()
    }

	const handleGiveTx = async (txResults) => {
    	console.log(txResults)
    	const checkForUpdate = () => new Promise((resolve) => {
    		let tries = 0
			let maxTries = 30
    		const get_thing_info = async () => {
    			let new_thing_info = await fetch(`./frames/${txResults.data.txInfo.kwargs.uid}.json`)
					.then(res => res.json())
					.catch(() => resolve(false))
				if (new_thing_info.lastUpdate > sendTime) resolve(new_thing_info)
				else {
					tries = tries + 1
					if (tries > maxTries) resolve(false)
					else setTimeout(get_thing_info, 500)
				}
			}
			get_thing_info()
		})

        if (txResults.data.txBlockResult.status === 0) {
        	updateInfo({
				"price_amount": "0",
				"price_hold": "",
				"owner": recipient.trim()
			})
        	let newThingInfo = await checkForUpdate()
			if (!newThingInfo) return

        	updateInfo(newThingInfo)
			createSnack({
				title: `NFT Sent!`,
				body: `You gifted ${thingName} to another user.`,
				type: "info"
			})
		}
    }
    const clearValidity = () => {
		inputElm.setCustomValidity("")
		inputElm.reportValidity("")
	}
</script>

<style>
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
	input[type="text"]{
		margin-bottom: 1rem;
	}
</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		<input type="submit" class="button_text outlined" disabled={transferTxStamps_to_tau.isGreaterThan($currency)}
			   value={transferTxStamps_to_tau.isGreaterThan($currency) ? `Insufficient ${config.currencySymbol}`: "Gift Item"}
			   form="give" />
	</div>
	<form id="give" class="flex-col" on:submit|preventDefault={checkRecipient}>
		<label for="recipient">Who would you like to Gift this to?</label>
		<input id="recipient" type="text" required bind:value={recipient} bind:this={inputElm} on:input={clearValidity}/>
		<div class="tx-costs">
			<p>Transaction Cost</p>
			<strong>{`${stringToFixed(transferTxStamps_to_tau, 4)} ${config.currencySymbol}`}</strong>
		</div>
	</form>
</div>
