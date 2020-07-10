<script>
    import { userAccount, showModal } from '../js/stores.js'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    import FormSell from './FormSell.svelte'

    export let thingInfo

    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal}, show:true})
    }
</script>

<style>
    .icon {
        margin-right: 5px;
        width: 20px;
        height: 30px;
    }
    .price{
        align-items: center;
        justify-content: flex-end;
    }
    .button_text{
        padding: 0 0 0 5px;
    }
</style>

<div class="flex-row price">
    <div class="icon">
        {@html lamden_logo}
    </div>
    {thingInfo.price}
    {#if thingInfo.owner !== $userAccount}
        <button class="button_text" on:click={() => openModal('FormBuy')}>buy</button>
    {:else}
        {#if thingInfo.price > 0}
            <button class="button_text" on:click={() => openModal(FormSell)}>set</button>
        {:else}
            <button class="button_text" on:click={() => openModal(FormSell)}>sell</button>
        {/if}
    {/if}
</div>





