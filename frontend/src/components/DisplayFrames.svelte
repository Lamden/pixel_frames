<script>
    import {getContext, onMount, createEventDispatcher} from 'svelte'
    import {goto} from '@sapper/app';

    // Misc
    import {userAccount, autoTx} from '../js/stores.js'
    import {createSnack, alreadyLiked, createWatermark, formatAccountAddress} from '../js/utils.js'
    import { config } from '../js/config.js';

    // Components
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import Price from './Price.svelte'
    import Likes from "./Likes.svelte";

    //Pictures
    import like_filled from '../../static/img/like-filled.svg'
    import like_unfilled from '../../static/img/like-unfilled.svg'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'
    import artist from '../../static/img/artist.svg'
    import owner from '../../static/img/owner.svg'


    const {sendTransaction} = getContext('app_functions')
    const dispatch = createEventDispatcher();

    export let thingInfo;
    export let index;
    export let pixelSize = 5;

    let frames = thingInfo.frames

    let switcher;
    let liked = null;
    $: show = 1

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
        if (txResults.data.txBlockResult.status === 0) {
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
    }
    a{
        text-decoration: underline;
    }
    a.name{
        align-self: center;

    }
    .title{
        justify-content: space-between;
    }
    .title > a {
        align-self: end;
        color: var(--primary);
        font-weight: bold;
        font-size: 0.8em;
        margin: 0;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .icons{
        margin: 0 0 0.5rem 8px;
        align-items: center;
        justify-content: flex-end;
    }
    .icon{
        width: 20px;
        height: 20px;
    }

</style>
<div class="title flex-row">
    <a href="{`./frames/${thingInfo.uid}`}" class="name">{thingInfo.name}</a>
    <div class="icons text-color-gray-5 flex-row">
        <a href="{`./creator/${thingInfo.creator}`}" class="icon">{@html artist}</a>
        <a href="{`./creator/${thingInfo.creator}`}" class="icon">{@html owner}</a>
    </div>
</div>

<a href="{`./frames/${thingInfo.uid}`}">
    {#if frames.length >= show}
        <FrameCanvas {pixelSize} pixels={frames[show - 1]} {thingInfo} watermark={createWatermark(thingInfo, $userAccount)} }/>
    {/if}
</a>
<div class="flex-row buy-like">
    <div>
        <Likes {thingInfo} />
    </div>
    <div>
        <Price {thingInfo} updateInfo={updateThingInfo}/>
    </div>
</div>
<div class="description">
    <p>{thingInfo.description}</p>
</div>




