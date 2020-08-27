<script>
	import { createEventDispatcher} from 'svelte'
	import { showModal, frames } from '../js/stores.js'
	import FormCreate from './FormCreate.svelte'
	import { framesEmpty } from '../js/utils.js'

	const dispatch = createEventDispatcher();

	const created = () => {
		dispatch('created', true)
	}

    const show = () => showModal.set({modalData: {modal: FormCreate, created}, show: true})



</script>

<style>
	button{
		margin-top: 1rem;
	}
</style>

<button class="button" on:click={show} disabled={framesEmpty($frames)}>CREATE</button>