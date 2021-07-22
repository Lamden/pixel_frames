<script>

    // Misc
    import { userAccount, showModal, released, tauPrice, auctions } from '../js/stores.js'
    import { stringToFixed, toBigNumber } from '../js/utils.js'
    import { config, featureLocks } from '../js/config.js'

    // Pictures
    import LamdenLogoIcon from '../../static/img/lamden_logo_new.svg'

    // Components
    import FormSell from './FormSell.svelte'
    import FormBuy from './FormBuy.svelte'
    import FormAuctionCreate from './FormAuctionCreate.svelte'

    export let thingInfo
    export let updateInfo

    $: price = toBigNumber(thingInfo.price_amount)
    $: usdPrice = price.isGreaterThan(0) ? price.multipliedBy($tauPrice) : false
    $: auctionFeatureLocked = featureLocks.auctions.locked

    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal, updateInfo}, show:true})
    }

</script>

<style>
    .flex-row{
        width: 100%;
        margin: 0.5rem 0;
    }
    .icon {
        margin-right: 5px;
        width: 20px;
        height: 30px;
    }
    .price{
        align-items: center;
        justify-content: flex-end;
        flex-wrap: wrap;
    }
    .button_text{
        display: none;
        color: var(--primary-dark);
        background: var(--gray-2);
        padding: 0.25rem 0.5rem;
        border-radius: 10px;
    }

    .auction_button{
        margin-left: 8px;
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
        margin: 0 4px;
    }
</style>


{#if price.isGreaterThan(0)}
    <div class="flex-row price">
        <LamdenLogoIcon class="icon" width="20"/>
        {stringToFixed(price, 8)}

        {#if usdPrice && !usdPrice.isNaN()}
            <span>{` ($${usdPrice.toFixed(2)})`}</span>
        {/if}

        {#if $userAccount}
            {#if thingInfo.owner !== $userAccount}
                <button class="button_text" on:click={() => openModal(FormBuy)}>buy!</button>
            {:else}
                <button class="button_text" on:click={() => openModal(FormSell)}>set</button>
            {/if}
        {/if}
    </div>
{:else}
    <div class="flex-row flex-justify-spacebetween">
        {#if thingInfo.owner !== $userAccount}
            <p class="text-color-gray-5">not for sale</p>
        {:else}
            {#if $userAccount}
                <button class="button_text" on:click={() => openModal(FormSell)}>sell</button>
                {#if auctionFeatureLocked && featureLocks.auctions.whitelist.includes($userAccount)}
                    <button class="auction_button button_text" on:click={() => openModal(FormAuctionCreate)}>start auction</button>
                {/if}
            {/if}
        {/if}
    </div>
{/if}







