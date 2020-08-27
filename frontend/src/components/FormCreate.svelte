<script>
    import { getContext } from 'svelte'
	import { frames, frameSpeed, showModal } from '../js/stores.js'
	import { serializeFrames, createSnack, nameTaken, closeModel } from '../js/utils.js'
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
			networkType: 'testnet',
			kwargs: {
				thing_string,
				description: desc,
				name: name,
				meta: {
					speed: parseInt($frameSpeed),
					num_of_frames: $frames.length
				}
			}
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
        if (txResults.txBlockResult.status === 0) {
        	created()
			createSnack({
				title: `Created!`,
				body: `${name} is now on the blockchain.`,
				type: "info"
			})
		}
    }
</script>

<style>
	.flex-row{
		align-items: center;
		justify-content: space-evenly;
		height: 100%;
	}
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
		color: #ff5bb0;
	}

</style>

<div class="flex-row">
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
