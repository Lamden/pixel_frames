<script>
    import { stringToFixed, timeDelta, formatAccountAddress} from '../js/utils'
    import { config } from '../js/config'

    // Icons
    import LamdenLogoIcon from '../../static/img/lamden_logo_new.svg'
    import GiftIcon from '../../static/img/gift.svg'
    import AuctionIcon from '../../static/img/auction.svg'

    export let salesHistory
    console.log(salesHistory)

</script>

<style>
    .history{
        width: 100%;
        text-align: left;
    }
    .header{
        justify-content: space-between;
    }

    :global(.saleshistory-icon){
        margin: 0 0px 0 5px;
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
        color: var(--primary);
        font-weight: 600;
    }
    p{
        margin: 0;
    }
    .winning-bid{
        margin-left: 8px;
    }
</style>

<h2 class="text-color-primary-dark">Ownership History</h2>
{#if salesHistory.data.length > 0}
    {#each salesHistory.data as history}
        <hr>
        <div class="flex-col history">
            {#if history.gift}
                <div class="header flex-row flex-align-center">
                    <div class="flex-row flex-align-center">
                        <h3>Gifted</h3>
                        <GiftIcon width="16" class="saleshistory-icon" />
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
            {/if}
            {#if history.auction}
                <div class="header flex-row flex-align-center">
                    <div class="flex-row flex-align-center">
                        <h3 class="flex-row">Auction</h3>
                        <AuctionIcon width="20" class="saleshistory-icon" />
                        <span class="winning-bid">Winning Bid</span>
                        <strong>{stringToFixed(history.price, 8)}</strong>
                        <LamdenLogoIcon width="20" class="saleshistory-icon" />

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
                    winner:
                    <a href="{`${config.blockExplorer}/addresses/${history.buyer}`}" target="_blank" rel="noopener noreferrer">
                        {formatAccountAddress(history.buyer, 8, 4) }
                    </a>
                </p>
            {/if}
            {#if !history.auction && !history.gift}
                <div class="header flex-row flex-align-center">
                    <div class="flex-row flex-align-center">
                        <h3 class="flex-row">Sold for</h3>
                        <strong>{stringToFixed(history.price, 8)}</strong>
                        <LamdenLogoIcon width="18" class="saleshistory-icon" />
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
