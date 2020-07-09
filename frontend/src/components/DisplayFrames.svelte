<script>
    import { onMount } from 'svelte'
    import {goto} from '@sapper/app';
    import Frame from './Frame.svelte'
    import FrameCanvas from './FrameCanvas.svelte'

    //Pictures
    import like_filled from '../../static/img/like-filled.svg'
    import like_unfilled from '../../static/img/like-unfilled.svg'
    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    export let thingInfo;
    export let pixelSize = 5;

    let frames = thingInfo.frames

    let switcher;
    $: show = 1

    onMount(() => {
        switcher = setTimeout(switchFrames, 1000)
    })

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
        switcher = setTimeout(switchFrames, 1000)
    }

</script>
<style>
    .flex-row{
        align-items: center;
        justify-content: space-between;
    }
    .icon {
        margin-right: 5px;
        width: 20px;
        height: 30px;
    }
    .button_text{
        font-weight: 100;
        margin: 0 0 0 5px;
        padding: 0;
        font-size: 0.9em;

    }
    .description{
        overflow-y: auto;
        align-items: baseline;
        flex-wrap: wrap;
    }
    p{
        width: 100%;
        margin: 0;
        overflow-y: auto;
        height: 107px;
        position: relative;
        font-size: 0.7em;
    }
</style>

<div class="display flex-col">
    <div>
        {#if frames.length >= show}
            <FrameCanvas {pixelSize} pixels={frames[show - 1]} id={thingInfo.uid}/>
        {/if}
    </div>

</div>
<div class="flex-col meta">
    <div class="flex-row">
        <div class="flex-row likes">
            <div class="icon">
                {@html like_unfilled}
            </div>
            {thingInfo.likes}
        </div>

        {#if thingInfo.price > 0}
            <div class="flex-row price">
                <div class="icon">
                    {@html lamden_logo}
                </div>
                {thingInfo.price}
                <a class="button_text" href={"buy/" + thingInfo.uid} >buy</a>
            </div>
        {/if}
    </div>
    <div class="flex-row description">
        <p>{thingInfo.description}</p>
    </div>
</div>



