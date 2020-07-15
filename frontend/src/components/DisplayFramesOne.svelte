<script>
    import { getContext, onMount } from 'svelte'
    import {goto} from '@sapper/app';
    import { userAccount } from '../js/stores.js'
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import Price from './Price.svelte'
    import { createSnack, decodeFrames } from '../js/utils.js'

    //Pictures
    import like_filled from '../../static/img/like-filled.svg'
    import like_unfilled from '../../static/img/like-unfilled.svg'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    const { sendTransaction } = getContext('app_functions')

    export let thingInfo;
    export let pixelSize = 17;

    let frames = thingInfo.frames

    let switcher;
    $: show = 1

    onMount(() => {
        switcher = setInterval(switchFrames, thingInfo.speed)
        return(() => clearInterval((switcher)))
    })

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
    }

    const like = () => {
		const transaction = {
			methodName: 'like_thing',
			networkType: 'testnet',
			stampLimit: 100000,
			kwargs: {
				uid: thingInfo.uid
			}
		}

		createSnack(
			`Liking ${thingInfo.name}`,
			"Please approve the Lamden Wallet transaction popup.",
			"info"
		)

        sendTransaction(transaction)
    }

</script>
<style>
    .container{
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
    }
    .display{
        align-items: center;
        margin: 0 auto;
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
        color: #ff5bb0;
        font-size: 1.2em;
    }
    .shadowbox{
        align-items: flex-start;
        width: 100%;
        min-width: unset;
        max-width: unset;
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
        color: #ff5bb0;
        font-weight: bold;
        margin: 1rem 0 2rem;
    }
    strong{
        color: #ff5bb0;
    }
</style>
<h1>{thingInfo.name}</h1>
<div class="flex-row container">
    <div class="flex-col display">
        <div>
            {#if frames.length >= show}
                <FrameCanvas {pixelSize} pixels={frames[show - 1]} id={thingInfo.uid}/>
            {/if}
        </div>
        <div class="flex-row likes-price">
            <div class="flex-row likes">
                <div class="icon" on:click={like}>
                    {@html like_unfilled}
                </div>
                {thingInfo.likes}
            </div>
            <div>
                <Price {thingInfo}/>
            </div>
        </div>
    </div>
    <div class="flex-col frameInfo">
        <p class="description">{thingInfo.description}</p>
        <div class="shadowbox">
            <p><strong>Creator</strong> <a href="{`./creator/${thingInfo.creator}`}">{thingInfo.creator}</a></p>
            <p><strong>Current Owner</strong> <a href="{`./owned/${thingInfo.owner}`}">{thingInfo.owner}</a></p>
            <p><strong>Unique Thing ID</strong> {thingInfo.uid}</p>
            <p><strong>Frame Speed</strong> {thingInfo.speed}ms</p>
            <p><strong>Number of Frames</strong> {thingInfo.num_of_frames}</p>
            <p class="price"><strong>Current Price</strong> <Price {thingInfo}/></p>
            {#if thingInfo['price:amount'] > 0 && thingInfo['price:hold'] !== ""}
                <p><strong></strong>Current held for buyer: {thingInfo['price:hold']}</p>
            {/if}
        </div>
    </div>
</div>

