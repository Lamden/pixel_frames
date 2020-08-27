<script>
    import {getContext, onMount, createEventDispatcher} from 'svelte'
    import {goto} from '@sapper/app';
    import {userAccount, autoTx} from '../js/stores.js'
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import Price from './Price.svelte'
    import {createSnack, alreadyLiked, createWatermark} from '../js/utils.js'

    //Pictures
    import like_filled from '../../static/img/like-filled.svg'
    import like_unfilled from '../../static/img/like-unfilled.svg'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'
    import Likes from "./Likes.svelte";

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
            networkType: 'testnet',
            stampLimit: 100000,
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
    .flex-row{
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
    h4{
        color: #ff5bb0;
        font-weight: bold;
        font-size: 0.8em;
        margin: 0 0 1rem;
        cursor: pointer;
    }
    h4:hover{
        text-decoration: underline;
    }
    .buy-like{
        flex-wrap: wrap;
    }
    a{
        text-decoration: none;
        align-self: center;
    }

</style>

<h4><a href="{`./frames/${thingInfo.uid}`}">{thingInfo.name}</a></h4>
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




