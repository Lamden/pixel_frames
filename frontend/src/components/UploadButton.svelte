<script>
    import { getContext } from 'svelte'
	import { frames, frameSpeed, snackbars } from '../js/stores.js'
	import { serializeFrames, createSnack } from '../js/utils.js'

    const { sendTransaction } = getContext('app_functions')

    const upload = () => {
    	const thing_string = serializeFrames($frames)
		let name = prompt("Give your creation a name!");

		const transaction = {
			methodName: 'create_thing',
			networkType: 'testnet',
			stampLimit: 1000000,
			kwargs: {
				thing_string,
				description: "This is rad.",
				name: name,
				meta: {
					speed: parseInt($frameSpeed),
					num_of_frames: $frames.length
				}
			}
		}
		console.log(transaction)
		sendTransaction(transaction)
		createSnack(
			"Transaction Submitted",
			"Attempting to store pixels on the Lamden Blockchain...",
			"info"
		)
    }

</script>

<button class="button" on:click={upload}>CREATE</button>