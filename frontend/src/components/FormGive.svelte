<script>
    import { getContext } from 'svelte'

	// Misc
	import { frames, showModal } from '../js/stores.js'
	import { createSnack, closeModel, isLamdenKey } from '../js/utils.js'
	import { config } from '../js/config.js';

    // Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
    const thingName = $showModal.modalData.thingInfo['name']

	let recipient = ""
	let inputElm
	let sendTime

	const checkRecipient = () => {
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
				console.log(new_thing_info)
				console.log(new_thing_info.lastUpdate)
				console.log(new_thing_info.lastUpdate > sendTime)
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
			console.log(newThingInfo)
			if (!newThingInfo) return

        	updateInfo(newThingInfo)
			createSnack({
				title: `NFT Sent!`,
				body: `You gifted ${thingName} to another user.`,
				type: "info"
			})
		}
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

</style>

<div class="flex-row">
	<div class="preview-row">
		{#if $showModal.modalData.thingInfo}
			<Preview frames={$showModal.modalData.thingInfo.frames} pixelSize={15} thingInfo={$showModal.modalData.thingInfo} />
		{/if}
		<input type="submit" class="button_text outlined" value="Gift Item" form="give" />
	</div>
	<form id="give" class="flex-col" on:submit|preventDefault={checkRecipient}>
		<label for="recipient">Who would you like to Gift this to?</label>
		<input id="recipient" type="text" required bind:value={recipient} bind:this={inputElm}/>
	</form>
</div>
