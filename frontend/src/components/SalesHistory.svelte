<script>
    import { stringToFixed, timeDelta, formatAccountAddress} from '../js/utils'
    import { config } from '../js/config'

    import lamden_logo from '../../static/img/lamden_logo_new.svg'
    import gift from '../../static/img/gift.svg'

    export let salesHistory

</script>

<style>
    .history{
        width: 100%;
        text-align: left;
    }
    .header{
        justify-content: space-between;
    }
    .icon {
        margin: 0 0px 0 5px;
        width: 15px;
    }
    .icon-gift {
        margin: 0 0px 0 5px;
        width: 20px;
        position: relative;
        top: -2px;
    }
    strong {
        margin-left: 5px;
        color: var(--primary);
    }
    .timedelta{
        margin-left: 20px;
        font-size: 0.8em;
    }
    h3{
        margin: 0;
    }
    p{
        margin: 0;
    }
</style>

<h2>Ownership History</h2>
{#if salesHistory.data.length > 0}
    {#each salesHistory.data as history}
        <hr>
        <div class="flex-col history ">
            {#if history.gift}

                <div class="header flex-row flex-align-center">
                    <div class="flex-row">
                        <h3 class="flex-row">Gifted</h3>
                        <span class="icon-gift">
                            {@html gift}
                        </span>
                    </div>
                <span class="timedelta text-color-gray-5">{timeDelta(history.saleDate)}</span>
                </div>
                <p class="text-color-gray-6">
                    from:
                    <a href="{`${config.blockExplorer}/addresses/${history.seller}`}" target="_blank" rel="noopener noreferrer">
                        {formatAccountAddress(history.seller, 8, 4)}
                    </a>
                </p>
                <p class="text-color-gray-6">
                    to:
                    <a href="{`${config.blockExplorer}/addresses/${history.buyer}`}" target="_blank" rel="noopener noreferrer">
                        {formatAccountAddress(history.buyer, 8, 4)}
                    </a>
                </p>
            {:else}
                <div class="header flex-row flex-align-center">
                    <div class="flex-row">
                        <h3 class="flex-row">Sold for</h3>
                        <strong>{stringToFixed(history.price, 8)}</strong>
                        <span class="icon">
                            {@html lamden_logo}
                        </span>
                    </div>
                    <span class="timedelta text-color-gray-5">{timeDelta(history.saleDate)}</span>
                </div>

                <p class="text-color-gray-6">
                    seller:
                    <a href="{`${config.blockExplorer}/addresses/${history.seller}`}" target="_blank" rel="noopener noreferrer">
                        {formatAccountAddress(history.seller, 8, 4)}
                    </a>
                </p>
                <p class="text-color-gray-6">
                    buyer:
                    <a href="{`${config.blockExplorer}/addresses/${history.buyer}`}" target="_blank" rel="noopener noreferrer">
                        {formatAccountAddress(history.buyer, 8, 4) }
                    </a>
                </p>
            {/if}
        </div>
    {/each}
{:else}
    <hr>
    <h3 class="text-color-gray-5">This NFT has never been sold.</h3>
{/if}
