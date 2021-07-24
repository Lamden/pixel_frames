<script>
    import { onMount, getContext } from 'svelte'

    // Misc
    import { toBigNumber, stringToFixed, formatAccountAddress, getTimeAgo } from '../js/utils'
    import {showModal, userAccount} from "../js/stores";
    import { config } from "../js/config"

    // Components
    import Preview from './Preview.svelte';
    import Likes from "./Likes.svelte";
    import AuctionEndDate from './AuctionEndDate.svelte'
    import FormBid from './FormBid.svelte'
    import FormAuctionClaim from './FormAuctionClaim.svelte'
    import FormAuctionCancel from './FormAuctionCancel.svelte'

    // Icons
    import CheckIcon from '../../static/img/check-filled.svg'

    export let auctionInfo
    export let thingInfo
    export let showInfo = true
    export let id

    //console.log({auctionInfo, thingInfo})

    let pixelSize = 2

    $: hasEnded = auctionHasEnded(auctionInfo)
    $: hasStarted = new Date() >= new Date(auctionInfo.start_date)
    $: timesUp = new Date() > new Date(auctionInfo.scheduled_end_date)
    $: notClaimed = auctionInfo.winner === ""
    $: reserveMet = auctionInfo.reserve_met
    $: bid_history = auctionInfo.bid_history
    $: winning_bid_info = bid_history.length > 0 ? bid_history[0] : null
    $: winning_bid = winning_bid_info ? toBigNumber(winning_bid_info.bid) : toBigNumber("0")
    $: winning_bidder = winning_bid_info ? winning_bid_info.bidder : ""
    $: winning_timestamp = winning_bid_info ? new Date(winning_bid_info.timestamp) : null
    $: timeAgo = getTimeAgo(winning_timestamp, hasEnded)
    $: canBeCancelled = determineCanBeCancelled(hasStarted, reserveMet)

    function determineCanBeCancelled(hasStarted, reserveMet){
        if (!hasStarted) return true
        if (!reserveMet) return true
        return false
    }

    function auctionHasEnded(info){
        // console.log(auctionInfo)
        if (info.ended) return true
        if (new Date() > new Date(info.scheduled_end_date)) return true
        return false
    }

    const handleBid = () => {
        showModal.set({
            modalData:{
                auctionInfo,
                thingInfo,
                winning_bid,
                modal: FormBid
            },
            show: true
        })
    }

    const handleEnd = (modal, claim=false) => {
        showModal.set({
            modalData:{
                auctionInfo,
                thingInfo,
                end_info: {
                    bid: winning_bid,
                    bidder: winning_bidder,
                    hasEnded,
                    winning_timestamp,
                    end_early: canBeCancelled,
                    claim,
                    reserveMet
                },
                modal
            },
            show: true
        })
    }

</script>

<style>
    .auction-container{
        position: relative;
        margin:  1.1rem;
        box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
        -webkit-box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
        -moz-box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
        background: #fdfffe;
        background: linear-gradient(170deg, var(--color-white-primary-tint) 0%, rgb(241 241 241) 100%);
        display: flex;
        flex-direction: column;
        border-radius: 10px;
        width: 350px;
    }
    .top-content{
        padding: 20px 20px 0.5rem 20px;
    }
    .title{
        font-size: 18px;
        margin-bottom: 1rem;
    }
    .title > a{
        font-weight: 600;
        color: var(--primary-dark);
        text-decoration: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .description{
        margin-top: 0.5rem;
        color: var(--primary-dark);
        max-height: 85px;
        overflow-y: auto;
    }
    p{
        margin: 0;
    }
    p > strong {
        color: var(--primary-dark);
        font-size: 22px;
    }
    .bid-details{
        margin-left: 20px;
    }
    button{
        width: 130px;
        align-self: center;
        letter-spacing: 1px;
    }
    .buttons{
        padding: 1rem 0;
    }
    .current-winner{
        background: var(--primary);
        padding: 5px 17px;
        border-radius: 10px;
    }
    .current-winner > span {
        width: max-content;
    }
    p.reserve-not-met{
        position: absolute;
        top: -10px;
        right: 50%;
        width: max-content;
        background: var(--primary-dark);
        color: var(--color-white-primary-tint);
        padding: 3px 9px;
        border-radius: 10px;
        font-size: 12px;
        transform: translate(50%, 0);
    }
    .no-bid{
        font-size: 14px;
        color: var(--gray-5);
    }
    :global(.auction-check-icon){
        margin-left: 8px;
    }
</style>
<div class="auction-container" {id}>
    <div class="top-content flex-grow">
        {#if !reserveMet}
            <p class="reserve-not-met">Resereve Not Met</p>
        {/if}
        {#if showInfo}
            <div class="title flex-row">
                <a href="{`./frames/${thingInfo.uid}`}" class="name">{thingInfo.name}</a>
            </div>
        {/if}
        <!--
        <div class="icons text-color-gray-5 flex-row flex-align-center">
            <a href="{`./creator/${thingInfo.creator}`}" class="icon">{@html artist}</a>
            <a href="{`./owned/${thingInfo.owner}`}" class="icon">{@html owner}</a>
            <Likes {thingInfo} width={25}/>
        </div>
        -->
        <div class="flex-row">
            <a href="{`./frames/${thingInfo.uid}`}">
                <Preview solidBorder={true} solidBorderColor="#00d6a22b" frames={thingInfo.frames} pixelSize={4} {thingInfo} showWatermark={true} border={false}/>
            </a>
            <div class="bid-details">
                    <p class="text-color-gray-6">{hasEnded ? auctionInfo.reserve_met ? "Winning Bid" : "Last Bid" : "Current Bid" }</p>
                    <p><strong>{`${stringToFixed(winning_bid, 8)} ${config.currencySymbol}`} </strong></p>
                {#if winning_bidder}
                    <p class="text-color-gray-5">{hasEnded ? `Won ${getTimeAgo(winning_timestamp)}by` : `${getTimeAgo(winning_timestamp)}by` }</p>
                    {#if $userAccount === winning_bidder}
                        <a href="{`./owned/${winning_bidder}`}" class="text-color-gray-5">
                            {$userAccount === winning_bidder ? "YOU!" : formatAccountAddress(winning_bidder, 8, 4)}
                        </a>
                    {/if}
                {:else}
                    {#if hasEnded}
                        <p><strong class="no-bid">Auction Expired</strong></p>
                    {:else}
                        <p><strong class="no-bid">Be the first to bid!</strong></p>
                    {/if}
                {/if}
            </div>
        </div>
        {#if showInfo}
            <p class="description">{thingInfo.description}</p>
        {/if}
    </div>
    <div class="buttons flex-row flex-justify-spaceevenly">
        {#if !hasEnded}
            {#if $userAccount === winning_bidder}
                <div class="flex-row flex-center-center current-winner">
                    <span>You are winning this auction!</span>
                    <CheckIcon class="auction-check-icon" width="17" />
                </div>
            {:else}
                {#if $userAccount !== auctionInfo.old_owner}
                    <button class="button" on:click={handleBid} > BID </button>
                {/if}
            {/if}
        {/if}
        {#if notClaimed && hasEnded}
            {#if winning_bidder !== "" && $userAccount === winning_bidder}
                <button class="button" on:click={() => {handleEnd(FormAuctionClaim, true)}}>CLAIM</button>
            {:else}
                {#if $userAccount === auctionInfo.old_owner}
                    <button class="button" on:click={() => {handleEnd(FormAuctionClaim)}}>RESOLVE AUCTION</button>
                {/if}
            {/if}
        {/if}
        {#if $userAccount === auctionInfo.old_owner && canBeCancelled && !hasEnded}
                <button class="button" on:click={() => {handleEnd(FormAuctionCancel)}}>{hasEnded ? "" : "CANCEL"}</button>
        {/if}
    </div>
    <AuctionEndDate {auctionInfo}/>
</div>