<script>
    import { afterUpdate } from 'svelte'
    import { userAccount } from '../js/stores.js'
    import { drawFrame, formatAccountAddress } from '../js/utils.js'
    import { config } from '../js/config.js'

    export let id;
    export let watermark = undefined;
    export let pixels;
    export let pixelSize = 3;

    let canvasElm;

    afterUpdate(() => drawFrame(canvasElm, pixels, pixelSize, watermark))

</script>

<style>
    canvas{
        display: block;
    }
</style>

<canvas
        id="{id}"
        bind:this={canvasElm}
        width={pixelSize * config.frameWidth}
        height={pixelSize * config.frameWidth}
/>

