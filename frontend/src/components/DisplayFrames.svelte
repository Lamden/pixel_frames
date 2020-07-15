<script>
    import { getContext, onMount } from 'svelte'
    import { goto } from '@sapper/app';
    import { userAccount } from '../js/stores.js'
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import Price from './Price.svelte'
    import { createSnack } from '../js/utils.js'

    //Pictures
    import like_filled from '../../static/img/like-filled.svg'
    import like_unfilled from '../../static/img/like-unfilled.svg'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    const { sendTransaction } = getContext('app_functions')

    export let thingInfo;
    export let pixelSize = 5;

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

    const showFrame = () => goto(`./frames/${thingInfo.uid}`)

</script>
<style>
    .flex-row{
        align-items: center;
        justify-content: space-between;
    }
    .display{
        align-items: center;
    }
    .icon {
        margin-right: 5px;
        width: 20px;
        height: 30px;
        cursor: pointer;
    }
    .description{
        overflow-y: auto;
        align-items: baseline;
        flex-wrap: wrap;
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
        margin: 0 0 0.5rem;
        cursor: pointer;
    }
    h4:hover{
        text-decoration: underline;
    }
</style>

<h4 on:click={showFrame}>{thingInfo.name}</h4>
<div class="flex-col display">
    <div on:click={showFrame}>
        {#if frames.length >= show}
            <FrameCanvas {pixelSize} pixels={frames[show - 1]} id={thingInfo.uid}/>
        {/if}
    </div>

</div>
<div class="flex-col meta">
    <div class="flex-row">
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
    <div class="flex-row description">
        <p>{thingInfo.description}</p>
    </div>
</div>



