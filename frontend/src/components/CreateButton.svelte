<script>
	import { createEventDispatcher} from 'svelte'
	import { showModal, frames, released, userAccount } from '../js/stores.js'
	import FormCreate from './FormCreate.svelte'
	import { framesEmpty, hasNulls } from '../js/utils.js'

	const dispatch = createEventDispatcher();

	const created = () => {
		dispatch('created', true)
	}

    const show = () => {
		if (hasNulls($frames)){
			alert('Your art has bad data. Please check all pixels and replace any "E" values.')
			return
		}
		if (!$userAccount) {
			alert('You must be signed into the Lamden Wallet to upload your NFT to the blockchain.')
			return
		}
		showModal.set({modalData: {modal: FormCreate, created}, show: true})
	}

</script>

<style>
	button{
		margin-top: 1rem;
	}
</style>

<button class="button" on:click={show} disabled={framesEmpty($frames)}>MINT NFT</button>