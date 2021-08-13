<script>
    import { afterUpdate } from 'svelte'
    import { drawFrame } from '../js/utils.js'
    import { config } from '../js/config.js'

    export let id = parseInt(Math.random() * 10000);
    export let watermark = undefined;
    export let pixels;
    export let pixelSize = 3;

    let canvasElm;

    afterUpdate(() => {
        drawFrame(canvasElm, pixels, pixelSize, watermark)
    })

    $: width = pixelSize * config.frameWidth
    $: height = pixelSize * config.frameWidth

</script>

<style>
    canvas{
        display: block;
    }
</style>

<canvas
        id="{id}"
        bind:this={canvasElm}
        {width} {height}
/>

