<script>
    import { getContext } from 'svelte'
    import { serializeFrames } from '../js/utils'
    import { frames, frameSpeed } from '../js/stores'

    const { sendTransaction } = getContext('app_functions')

    const upload = () => {
    	const thing_string = serializeFrames($frames, $frameSpeed)
		console.log(thing_string)
		console.log(thing_string.length)
		localStorage.setItem('frames', JSON.stringify($frames))
		localStorage.setItem('thing_string', thing_string)

		const transaction = {
			methodName: 'create_thing',
			networkType: 'testnet',
			stampLimit: 1000000,
			kwargs: {
				thing_string,
				description: "A test string"
			}
		}
		//sendTransaction(transaction)
    }

</script>

<button class="button" on:click={upload}>CREATE</button>