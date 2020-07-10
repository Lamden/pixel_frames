<script>
    import { onMount } from 'svelte'
    import { scale, fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
    import { showModal } from '../js/stores.js'

    $: buttons = []

    onMount(() => {
        buttons = $showModal.modalData.buttons
    })
</script>

<style>
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 600px;
        max-width: 100%;
        height: 400px;
        max-height: 100%;
        background: #ff5bb0;
        border-radius: 5px;
        box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
        z-index: 500;
    }
    .data{
        flex-grow: 1;
    }
    .buttons{
        padding: 1rem 0;
        align-items: center;
        justify-content: center;
        background: white;
        border-radius: 0 0 5px 5px;
    }
</style>


<div class="flex-col modal"
     transition:scale="{{duration: 200, delay: 0, opacity: 0, start: 0.8, easing: quintOut}}">
    <div class="data">
        {#if $showModal.modalData}
         <svelte:component this={$showModal.modalData.modal} />
        {/if}
    </div>
    <div class="flex-col buttons">
        <button class="button" on:click={() => showModal.set({modalData: {}, show: false})}>cancel</button>
    </div>
</div>
