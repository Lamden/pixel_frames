<script>
    import { afterUpdate } from 'svelte'
    import { userAccount } from '../js/stores.js'
    import { drawFrame, formatAccountAddress } from '../js/utils.js'

    export let id;
    export let watermark = undefined;
    export let pixels;
    export let pixelSize = 5;

    let canvasElm;

    afterUpdate(() => drawFrame(canvasElm, pixels, pixelSize, watermark))

</script>


<canvas
        id="{id}"
        bind:this={canvasElm}
        width={pixelSize * 16}
        height={pixelSize * 16}
/>

