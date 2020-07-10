<script>
	import { showModal, frames } from '../js/stores.js'
	import FormCreate from './FormCreate.svelte'
	import { framesEmpty } from '../js/utils.js'

    const show = () => showModal.set({modalData: {modal: FormCreate}, show: true})

</script>

<style>
	button{
		margin-top: 1rem;
	}
</style>

<button class="button" on:click={show} disabled={framesEmpty($frames)}>CREATE</button>