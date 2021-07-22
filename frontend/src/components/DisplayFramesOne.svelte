<script>
    import {getContext, onMount, tick} from 'svelte';
    import {goto} from '@sapper/app';

    // Misc
    import {userAccount, showModal} from '../js/stores.js';
    import { config } from '../js/config.js';
    import {createSnack, createWatermark, alreadyLiked, formatAccountAddress} from '../js/utils.js';

    // Components
    import FormGive from './FormGive.svelte'
    import SalesHistory from './SalesHistory.svelte'
    import FrameCanvas from './FrameCanvas.svelte';
    import Price from './Price.svelte';
    import Likes from './Likes.svelte'
    import OwnerControls from './OwnerControls.svelte'
    import Auction from './Auction.svelte';

    // Pictures
    import SocialButtons from "./SocialButtons.svelte";

    const {sendTransaction} = getContext('app_functions')

    export let thingInfo;
    export let auctionInfo;

    //console.log({thingInfo, auctionInfo})
    export let salesHistory;
    export let pixelSize = 17;
    export let updateInfo

    let frames = thingInfo.frames
    let switcher;
    let liked = null;
    $: show = 1

    onMount(() => {
        if (window.location.hash){
            scrollToHash(window.location.hash.replace("#", "").toUpperCase())
        }
        console.log(window.location)
        checkAlreadyLiked()
        switcher = setInterval(switchFrames, thingInfo.speed)
        return (() => clearInterval((switcher)))
    })

    async function scrollToHash(hash){
        await tick()
        let elm = document.getElementById(hash)
        if (elm) setTimeout(() => elm.scrollIntoView(), 1);
    }

    const openModal = (modal) => {
        showModal.set({modalData:{thingInfo, modal: modal, updateInfo}, show:true})
    }

    const checkAlreadyLiked = () => {
        if (liked === null && $userAccount) {

            alreadyLiked(thingInfo.uid, localStorage).then(res => {
                console.log(res)
                liked = res

            })
        }
    }

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
    }

    const like = () => {
        const transaction = {
            methodName: 'like_thing',
            networkType: config.networkType,
            kwargs: {
                uid: thingInfo.uid
            }
        }

        createSnack({
            title: `Liking ${thingInfo.name}`,
            body: "Please approve the Lamden Wallet transaction popup.",
            type: "info"
        })

        sendTransaction(transaction)
    }

    userAccount.subscribe(account => checkAlreadyLiked())

</script>
<style>
    .container{
        flex-wrap: wrap;
        justify-content: center;
    }
    .frame-border{
        border: 1px solid #ff5bb033;
    }
    .likes-price{
        width: 100%;
        justify-content: space-between;
        margin: 1rem 0;
    }
    .likes{
        align-items: center;
    }
    .icon {
        margin-right: 5px;
        width: 20px;
        height: 30px;
        cursor: pointer;
    }
    .description{
        color: var(--primary);
        font-size: 1.2em;
        max-width: fit-content;

    }
    .shadowbox{
        align-items: flex-start;
        flex-grow: 1;
        min-width: fit-content;
        max-width: unset;
        margin: 0 50px;
        width: unset;
    }
    .price{
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .price > strong {
        margin-right: 5px;
    }
    p{
        margin: 0 0 1rem 0;
        word-break: break-word;
    }
    h1{
        color: var(--primary);
        font-weight: bold;
        margin: 2rem 0 2rem;
        text-align: center;
    }
    strong{
        color: var(--primary);
    }
    .sales-history{
        padding-top: 3rem;
        width: 100%;
    }
    .auction-info{
        margin-top: 3rem;
    }
    .auction{
        margin-top: 2rem;
    }
</style>

<h1>{thingInfo.name}</h1>
<div class="flex-row container">
    <div>
        <a rel="prefetch noopener noreferrer" href="{'gif/'+ thingInfo.uid + '.gif'}" target="_blank">
            {#if frames.length >= show}
                <FrameCanvas {pixelSize} pixels={frames[show - 1]} id={thingInfo.id} watermark={createWatermark(thingInfo, $userAccount)} />
            {/if}
        </a>
        <div class="flex-row likes-price">
            <div>
                <Likes {thingInfo}/>
            </div>
            <div>
                <Price {thingInfo} {updateInfo}/>
            </div>
        </div>
        <div>
            <OwnerControls {thingInfo} owner="" }/>
        </div>
    </div>
    <div class="shadowbox">
        <p><strong>Name</strong> {thingInfo.name}</p>
        <p><strong>Description</strong> {thingInfo.description}</p>
        <p><strong>ID</strong> {formatAccountAddress(thingInfo.uid, 8, 4)}</p>
        <p><strong>Current Owner</strong> <a href="{`./owned/${thingInfo.owner}`}">{formatAccountAddress(thingInfo.owner, 8, 4)}</a></p>
        <p><strong>Creator</strong> <a href="{`./creator/${thingInfo.creator}`}">{formatAccountAddress(thingInfo.creator, 8, 4)}</a></p>
        <p><strong>Date Created</strong> {new Date(thingInfo.datetimeCreated).toLocaleString()}</p>
        <p><strong>Frame Speed</strong> {thingInfo.speed}ms</p>
        <p><strong>Number of Frames</strong> {thingInfo.num_of_frames}</p>
        <p class="price"><strong>Current Price</strong> <Price {thingInfo} {updateInfo}/></p>
        {#if thingInfo['price_amount'] > 0 && thingInfo['price_hold'] !== ""}
            <p><strong></strong>Currently held for buyer: {thingInfo['price_hold']}</p>
        {/if}
        {#if thingInfo.owner === $userAccount}
            <button class="button" on:click={() => openModal(FormGive)}>Gift</button>
        {/if}
        <SocialButtons {thingInfo}/>
    </div>
</div>

<div class="auction-info" id="AUCTION" on:ready={() => console.log("READY")}>
    {#if auctionInfo}
        <h2 >There is an active Auction!</h2>
        <hr>
        <div class="flex flex-center-center auction">
            <Auction {auctionInfo} {thingInfo} showInfo={false}/>
        </div>
    {/if}
</div>

<div class="sales-history">
    <SalesHistory {salesHistory}/>
</div>

