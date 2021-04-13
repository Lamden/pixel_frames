<script>
    import { userAccount, showModal, released, tauPrice } from '../js/stores.js'
    import { stringToFixed, toBigNumber } from '../js/utils.js'

    // Pictures
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    // Components
    import FormSell from './FormSell.svelte'
    import FormBuy from './FormBuy.svelte'

    export let thingInfo
    export let updateInfo

    $: price = toBigNumber(thingInfo.price_amount)
    $: usdPrice = price.isGreaterThan(0) ? price.multipliedBy($tauPrice) : false

    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal, updateInfo}, show:true})
    }

    const handleBuy = () => {
        console.log($released)
        if ($released){
            openModal(FormBuy)
        }else{
            alert('Buying will be enabled when Pixel Whale releases, April 19th @ 8pm UTC.')
        }
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
        margin: 0.25rem 0;
    }
    .button_text{
        padding: 0 0 0 5px;
        display: none;
    }
    p{
        margin: 0;
        padding: 0;
    }
    @media (min-width: 450px) {
		.button_text{
            display: block;
        }
	}
    span{
        color: var(--gray-5);
        margin-left: 4px;
    }
</style>

<div class="flex-row price">
    {#if price.isGreaterThan(0)}
        <div class="icon">
            {@html lamden_logo}
        </div>
        {stringToFixed(price, 8)} {#if usdPrice && !usdPrice.isNaN()}<span>{` ($${stringToFixed(usdPrice, 2)})`}</span>{/if}
        {#if $userAccount}
            {#if thingInfo.owner !== $userAccount}
                <button class="button_text" on:click={handleBuy}>buy!</button>
            {:else}
                <button class="button_text" on:click={() => openModal(FormSell)}>set</button>
            {/if}
        {/if}
    {:else}
        {#if thingInfo.owner !== $userAccount}
            <p class="text-color-gray-5">not for sale</p>
        {:else}
            {#if $userAccount}
                <button class="button_text" on:click={() => openModal(FormSell)}>sell</button>
            {/if}
        {/if}
    {/if}
</div>





