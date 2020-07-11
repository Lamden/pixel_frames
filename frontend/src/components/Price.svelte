<script>
    import { userAccount, showModal } from '../js/stores.js'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    import FormSell from './FormSell.svelte'
    import FormBuy from './FormBuy.svelte'

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
    p{
        margin: 0;
        padding: 0;
    }
</style>

<div class="flex-row price">
    {#if thingInfo.price > 0}
        <div class="icon">
            {@html lamden_logo}
        </div>
        {thingInfo.price}
        {#if thingInfo.owner !== $userAccount}
            <button class="button_text" on:click={() => openModal(FormBuy)}>buy</button>
        {:else}
            <button class="button_text" on:click={() => openModal(FormSell)}>set</button>
        {/if}
    {:else}
        {#if thingInfo.owner !== $userAccount}
            <p class="button_text">not for sale</p>
        {:else}
            <button class="button_text" on:click={() => openModal(FormSell)}>sell</button>
        {/if}
    {/if}
</div>





