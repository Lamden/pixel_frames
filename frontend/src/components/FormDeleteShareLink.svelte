<script>
    import { getContext } from 'svelte'

	// Pictures
	import info from '../../static/img/info-filled.svg'

	// Misc
	import { showModal } from '../js/stores.js'
	import { createSnack, closeModel, isLamdenKey } from '../js/utils.js'
	import { config } from '../js/config.js';

    const { sendTransaction } = getContext('app_functions')

	const updateInfo = $showModal.modalData.updateInfo
	const uid = $showModal.modalData.thingInfo['uid']
    const thingName = $showModal.modalData.thingInfo['name']

	let challenge;


    const proveOwnership = async () => {
		let authCodeInfo = await fetch(`./get-code.json?uid=${$showModal.modalData.thingInfo.uid}`).then(res => res.json())
		console.log({authCodeInfo_proveOwnership: authCodeInfo})
		if (!authCodeInfo || !authCodeInfo.code) {
			createSnack({
				title: `Error`,
				body: `Unable to get Auth Code from server.`,
				type: "error"
			})
			return
		}

		challenge = authCodeInfo.challenge

		const transaction = {
			methodName: 'prove_ownership',
			networkType: config.networkType,
			kwargs: {
				uid,
				code: authCodeInfo.code
			}
		}
		sendTransaction(transaction, handleAuthCode)
		closeModel()
    }

	const handleAuthCode = async (txResults) => {
    	console.log(txResults)
		if (txResults.data.txBlockResult.status === 0) {
			let authResponse = await checkForValidAuth()
			console.log("DONE AWAITING")
			console.log({authResponse})
			if (authResponse.error){
				createSnack({
					title: `Cannot delete share link!`,
					body: ` ${authResponse.error}`,
					type: "error"
				})
			}else{
				updateInfo({shareLink: null})
				createSnack({
					title: `Share Link Deleted!`,
					body: `You have deleted the shareable link for ${thingName}.`,
					type: "info"
				})
			}
		}
    }

    const checkForValidAuth = () => new Promise(resolver => {
    	const maxChecks = 15;
    	let checks = 0;
    	const check = async () => {
    		console.log("CHECKING!")
    		checks = checks + 1
    		let res = await fetch(`./delete_share_link.json?uid=${uid}&challenge=${challenge}`).then(res => res.json())
			console.log({res, checks, maxChecks, doneChecking: checks === maxChecks })
			if (res.deleted) return resolver(res)
			if (res.error === "Challenge not accepted.") return resolver(res)
			if (res.error === "Unknown Error. Code was not deleted!") return resolver(res)
			if (res.error === "Auth Code not valid." && checks === maxChecks) return resolver(res)
			if (checks === maxChecks) return resolver({error: "Unknown Error."})
			else {
				console.log("CHECKING AGAIN!")
				setTimeout(check, 2000)
			}
		}
		check()
	})
</script>


<style>
	.outlined{
		color: var(--color-white-primary-tint);
	}
	.outlined:disabled {
		background: var(--primary-dark);
		color: var(--gray-2);
	}
	input{
		max-width: 200px;
		margin: 0 auto;
	}
	hr{
		width: 100%;
		border: 2px solid white;
  		border-radius: 5px;
	}
	.icon{
		min-width: 150px;
		max-width: 200px;
		margin: 0 auto auto;
	}
	.info{
		margin-left: 1rem;
	}
	.info > p {
		margin-bottom: 0;
		max-width: 400px;
		color: var(--color-white-primary-tint);
	}
	.subtext{
		color: var(--color-white-primary-tint);
	}
</style>

<div class="flex-col text-color-white-primary-tint">
	<div class="flex-row">
		<div class="icon">
			{@html info}
		</div>
		<div class="flex-col flex-justify-center info weight-600">
			<p>Deleting this link will prevent anyone from accessing the GIF file.</p>
			<p>A new link can be created later, but it will be different.</p>
		</div>
	</div>
	<hr>
	<p class="subtext text-center text-color-black">
		Click below to send A PROOF transaction to validate your ownership.
	</p>
	<form id="delete_share_link" class="flex-col" on:submit|preventDefault={proveOwnership}>
		<input type="submit" class="button_text outlined" value="Prove Ownership" form="delete_share_link" />
	</form>
</div>