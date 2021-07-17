<script>
    import { userAccount, showModal, released, tauPrice } from '../js/stores.js'
    import { stringToFixed, toBigNumber } from '../js/utils.js'
    import { config } from '../js/config.js'

    // Pictures
    import LamdenLogoIcon from '../../static/img/lamden_logo_new.svg'

    // Components
    import FormSell from './FormSell.svelte'
    import FormBuy from './FormBuy.svelte'
    //import FormAuctionCreate from './FormAuctionCreate.svelte'

    export let thingInfo
    export let updateInfo

    $: price = toBigNumber(thingInfo.price_amount)
    $: usdPrice = price.isGreaterThan(0) ? price.multipliedBy($tauPrice) : false

    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal, updateInfo}, show:true})
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
        flex-wrap: wrap;
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
        <LamdenLogoIcon class="icon" width="20"/>

        {stringToFixed(price, 8)} {#if usdPrice && !usdPrice.isNaN()}<span>{` ($${usdPrice.toFixed(2)})`}</span>{/if}
        {#if $userAccount}
            {#if thingInfo.owner !== $userAccount}
                <button class="button_text" on:click={() => openModal(FormBuy)}>buy!</button>
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
                <!--<button class="button_text" on:click={() => openModal(FormAuctionCreate)}>auction</button>-->
            {/if}
        {/if}
    {/if}
</div>





