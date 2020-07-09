<script>
    import { getContext } from 'svelte'

    const { sendTransaction } = getContext('app_functions')

    const upload = () => {


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

<style>
	button{
		margin-top: 1rem;
	}
</style>

<button class="button" on:click={upload}>CREATE</button>