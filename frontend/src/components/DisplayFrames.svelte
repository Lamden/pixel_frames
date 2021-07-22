<script>
    import {getContext, onMount, createEventDispatcher} from 'svelte'
    import {goto} from '@sapper/app';

    // Misc
    import {userAccount, autoTx, auctions} from '../js/stores.js'
    import {createSnack, alreadyLiked, createWatermark, formatAccountAddress} from '../js/utils.js'
    import { config, featureLocks } from '../js/config.js';

    // Components
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import Price from './Price.svelte'
    import Likes from "./Likes.svelte";

    //Pictures
    import ArtistIcon from '../../static/img/artist.svg'
    import OwnerIcon from '../../static/img/owner.svg'


    const {sendTransaction} = getContext('app_functions')
    const dispatch = createEventDispatcher();

    export let thingInfo;
    export let index;
    export let pixelSize = 5;

    let frames = thingInfo.frames

    let switcher;
    let liked = null;

    $: show = 1
    $: auctioninfo = $auctions.find(f => f.uid === thingInfo.uid)
    $: activeAuction = auctioninfo ? true : false

    onMount(() => {
        checkAlreadyLiked();
        switcher = setInterval(switchFrames, thingInfo.speed)
        return (() => clearInterval((switcher)))
    })

    const checkAlreadyLiked = () => {
        if (liked === null && $userAccount) alreadyLiked(thingInfo.uid, localStorage).then(res => liked = res)
    }

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
    }

    const like = () => {
        if (liked || !$userAccount) return;

        const transaction = {
            methodName: 'like_thing',
            networkType: config.networkType,
            kwargs: {
                uid: thingInfo.uid
            }
        }

        if (!$autoTx) {
            createSnack({
                title: `Liking ${thingInfo.name}`,
                body: 'Check for Lamden Wallet popup to approve transaction.',
                type: "info"
            })
        }

        sendTransaction(transaction, handleLikeTx)
    }

    const handleLikeTx = (txResults) => {
        if (txResults.txBlockResult.status === 0) {
            liked = true;
            thingInfo.likes = thingInfo.likes + 1;
            createSnack({
                title: `${thingInfo.name}`,
                body: 'You liked this creation!',
                type: "info"
            })
        }
    }

    const updateThingInfo = (updates) => {
        dispatch('update', {index, updates})
    }

    userAccount.subscribe(account => checkAlreadyLiked())

</script>
<style>
    .buy-like{
        align-items: center;
        justify-content: space-between;

    }
    .display{
        align-items: center;
    }
    .description{
        overflow-y: auto;
        align-items: baseline;
        flex-wrap: wrap;
        word-break: break-word;
        flex-grow: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .description > p{
        width: 100%;
        margin: 0;
        overflow-y: auto;
        height: 49px;
        position: relative;
        font-size: 0.7em;
    }

    .buy-like{
        flex-wrap: wrap;
        width: 100%;
    }
    a{
        text-decoration: underline;
    }
    .title{
        justify-content: space-between;
        align-items: center;
        margin: 0 0 0.25rem;
    }
    .title > a {
        align-self: center;
        color: var(--primary-dark);
        font-weight: bold;
        font-size: 0.8em;
        margin: -0.5rem 0 0;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .icons{
        margin: 0 0 0.5rem;
    }
    .icon{
        width: 20px;
        height: 20px;
    }

</style>
<div class="title flex-row">
    <a href="{`./frames/${thingInfo.uid}`}" class="name">{thingInfo.name}</a>

</div>
<div class="icons text-color-gray-5 flex-row flex-align-center">
    <a href="{`./creator/${thingInfo.creator}`}" class="icon">
        <ArtistIcon width="20"/>
    </a>
    <a href="{`./owned/${thingInfo.owner}`}" class="icon flex-grow">
        <OwnerIcon width="20"/>
    </a>
    <Likes {thingInfo} />

</div>

<a href="{`./frames/${thingInfo.uid}`}">
    {#if frames.length >= show}
        <FrameCanvas {pixelSize} pixels={frames[show - 1]} watermark={createWatermark(thingInfo, $userAccount)}/>
    {/if}
</a>
{#if activeAuction}
    <a href="{`./frames/${thingInfo.uid}#auction`}" class="auction">view active auction</a>
{:else}
    <div class="flex-row buy-like">
        <Price {thingInfo} updateInfo={updateThingInfo}/>
    </div>
{/if}
<div class="description">
    <p>{thingInfo.description}</p>
</div>




