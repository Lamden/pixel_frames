<script>
    import { getContext } from 'svelte'
    import { serializeFrames } from '../js/utils'
    import { frames } from '../js/stores'

    const { sendTransaction } = getContext('app_functions')

    const upload = () => {
    	const thing_string = serializeFrames($frames)
		const transaction = {
			methodName: 'create_thing',
			networkType: 'testnet',
			stampLimit: 1000000,
			kwargs: {
				thing_string,
				description: "A test string"
			}
		}
		sendTransaction(transaction)
    }

</script>

<button class="button" on:click={upload}>Upload</button>