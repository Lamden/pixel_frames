<script>
    import { onMount } from 'svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import { frameSpeed, userAccount } from '../js/stores.js'
    import { isEmptyFrame, createWatermark } from '../js/utils.js'

    export let frames;
    export let thingInfo = false;
    export let pixelSize = 10
    export let showWatermark = true;
    export let border = true;
    export let solidBorder = false;
    export let solidBorderColor = "";
    export let speed = null

    let switcher;
    $: show = 1
    $: animationSpeed = setSpeed(speed || $frameSpeed)

    onMount(() => {
        if (thingInfo){
            switcher = setInterval(switchFrames, thingInfo.speed)
        }
        return(() => clearInterval((switcher)))
    })

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
    }

    const setSpeed = (s) => {
        if (!thingInfo){
            clearInterval((switcher))
            switcher = setInterval(switchFrames, s)
        }
    }

</script>

<style>
    .preview-frame{
        line-height: 0;
        width: max-content;
    }
    .preview-frame.border{
        border: 2px dashed var(--primary);
    }
    .preview-frame.solid-border{
        border: 1px solid;
    }
</style>

<div class="preview-frame" class:border={border} class:solid-border={solidBorder} style={solidBorderColor !== "" ? `border-color: ${solidBorderColor};`: ""}>
    <FrameCanvas {pixelSize} pixels={frames[show - 1]}  watermark={showWatermark ? createWatermark(thingInfo, $userAccount) : undefined}/>
</div>