<script>
    import { getContext } from 'svelte'
	import { goto } from '@sapper/app';

    //MISC
	import { frames, frameSpeed, showModal, frameStore, activeFrame } from '../js/stores.js'
	import { serializeFrames, createSnack, nameTaken, closeModel } from '../js/utils.js'
	import { config } from '../js/config.js';

    // Components
	import Preview from './Preview.svelte'

    const { sendTransaction } = getContext('app_functions')

	let name = "";
	let desc = "";
	let formElm;

	const created = $showModal.modalData.created

    const upload = () => {
    	const thing_string = serializeFrames($frames)

		const transaction = {
			methodName: 'create_thing',
			networkType: config.networkType,
			kwargs: {
				thing_string,
				description: desc,
				name: name,
				meta: {
					speed: parseInt($frameSpeed),
					num_of_frames: $frames.length
				}
			},
			stampLimit: 130 + (20 * $frames.length)
		}

		sendTransaction(transaction, handleCreateTx)
		closeModel()
    }

	const checkName = async (e) => {
		if (await nameTaken(name)) e.target.setCustomValidity("Name already taken")
		else {
			e.target.setCustomValidity("")
		}
		e.target.reportValidity()
	}

	const handleCreateTx = (txResults) => {
		console.log(txResults)
        if (txResults.txBlockResult.status === 0) {
        	created()
			createSnack({
				title: `Created!`,
				body: `${name} is now on the blockchain.`,
				type: "info"
			})

			const oldIndex = $activeFrame
			let newIndex = oldIndex  - 1
            if (newIndex < 0 ) newIndex = 0
            activeFrame.set(newIndex)

            frameStore.update(currentValue => {
                currentValue.splice(oldIndex, 1)
                console.log({currentValue})
                return currentValue
            })
			let stateChange = txResults.txBlockResult.state.find(f => f.key.includes(':names:'))
			if (stateChange && stateChange.value) redirect(stateChange.value, window.location.href)
		}
    }

    const redirect = (uid, location) =>  {
    	let maxChecks = 30
		let checks = 0
    	const checkForThing = async () => {
    		if (window.location.href !== location) return
    		checks = checks + 1
    		let res = await fetch(`./frames/${uid}.json`).then(res => res.json())
			if (res === null) {
				if (checks < maxChecks)setTimeout(checkForThing, 500)
			}else {
				if (window.location.href === location) goto(`/frames/${uid}`)
			}
		}
		checkForThing()
	}
</script>

<style>
	.preview-row{
		text-align: center;
	}
	textarea{
		resize: none;
	}

	.button_text{
		color: white;
	}
	.outlined:hover{
		color: var(--primary);
	}


</style>

<div class="modal-form flex-row">
	<div class="preview-row">
		<Preview frames={$frames} pixelSize={15} showWatermark={false}/>
		<input type="submit" class="button_text outlined" value="Create Frames!" form="create" />
	</div>
	<form id="create" class="flex-col" on:submit|preventDefault={upload} bind:this={formElm}>
		<label for="name">Give your creation a unique name</label>
		<input id="name" type="text" placeholder="Name" required on:blur={checkName} bind:value={name}/>
		<label for="desc">Tell People about your creation!</label>
		<textarea id="desc" type="textarea" rows="8" maxlength="128" placeholder="(max 128 chars)" required bind:value={desc}/>
	</form>
</div>
