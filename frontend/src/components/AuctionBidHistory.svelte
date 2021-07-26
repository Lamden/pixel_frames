<script>
    // Misc
    import {config} from "../js/config";
    import { formatAccountAddress, stringToFixed, toBigNumber, getTimeAgo} from "../js/utils";
    import { userAccount} from "../js/stores";

    export let bidHistory

    $: amountOfBids = bidHistory.length

</script>
<style>
    div{
        margin-top: 1rem;
    }
    a{
        color: var(--primary-dark);
    }
    strong{
        color: var(--primary-dark);
        font-weight: 600;
    }
    p{
        margin: 0 0 1rem;
        font-weight: 600;
        font-size: 20px;
        color: var(--primary-dark);
    }
</style>
<div class="flex-col">
    <p>Bid History ({amountOfBids} {amountOfBids === 1 ? "bid" : "bids"})</p>
    {#each bidHistory as bidInfo}
        <span>
            <a href={`./owners/${bidInfo.bidder}`}>
                {$userAccount === bidInfo.bidder ? "YOU" : `${formatAccountAddress(bidInfo.bidder)}`}
            </a>
            bid
            <strong>
                {stringToFixed(toBigNumber(bidInfo.bid, 8))}
                {config.currencySymbol}
            </strong>
            {getTimeAgo(new Date(bidInfo.timestamp))}
        </span>
    {/each}
</div>
