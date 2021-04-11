<script>
	import { createEventDispatcher} from 'svelte'
	import { showModal, frames, released, userAccount } from '../js/stores.js'
	import FormCreate from './FormCreate.svelte'
	import { framesEmpty } from '../js/utils.js'

	const dispatch = createEventDispatcher();

	const created = () => {
		dispatch('created', true)
	}

    const show = () => {
		if (!$userAccount) alert('You must be signed into the Lamden Wallet to upload your art to the blockchain.')
		if ($released){
			showModal.set({modalData: {modal: FormCreate, created}, show: true})
		}else{
			fetch(`./checkWhitelistArtists.json?artist=${$userAccount}`)
				.then(res => res.json())
				.then(isWhitelisted => {
					console.log(isWhitelisted)
					if (isWhitelisted) showModal.set({modalData: {modal: FormCreate, created}, show: true})
					else alert('Only whitelisted artists can upload creations before release.  Contact @PixelWhaleIO on twitter to apply.')
				})
		}
	}



</script>

<style>
	button{
		margin-top: 1rem;
	}
</style>

<button class="button" on:click={show} disabled={framesEmpty($frames)}>CREATE</button>