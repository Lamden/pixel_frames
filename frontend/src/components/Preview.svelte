<script>
    import { onMount } from 'svelte'
    import FrameCanvas from './FrameCanvas.svelte'
    import { frameSpeed } from '../js/stores.js'

    export let frames;

    let switcher;
    $: show = 1

    onMount(() => {
        return(() => clearInterval((switcher)))
    })

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
    }

    frameSpeed.subscribe(update => {
        clearInterval((switcher))
        switcher = setInterval(switchFrames, update)
    })

</script>
<style>
    .preview-frame{
        border: 2px dashed #ff5bb0;
        line-height: 0;
    }
</style>

<div class="preview-frame">
    {#if frames.length >= show}
        <FrameCanvas pixelSize={10} pixels={frames[show - 1]}/>
    {:else}
        <FrameCanvas pixelSize={10} pixels={frames[show - 1]}/>
    {/if}
</div>