<script>
    import { afterUpdate } from 'svelte'
    import { letter_to_color } from '../js/utils.js'

    export let id;
    export let pixels;
    export let pixelSize = 5;

    let canvasElm;

    afterUpdate(() => drawFrame())

    const drawFrame = () => {
        if (!pixels || !canvasElm) return
        let ctx = canvasElm.getContext('2d')
        ctx.clearRect(0, 0, canvasElm.width, canvasElm.height);

        pixels.forEach((letter, index) => {
            ctx.fillStyle = letter_to_color[letter];
            let rowBefore = Math.floor(index / 16)
            let rowAdj = (pixelSize * rowBefore)
            let y = Math.floor(index / 16)
            let x = (index - ( y * 16)) * pixelSize
            ctx.fillRect(x, rowAdj, pixelSize, pixelSize);
        })
    }
</script>


<canvas
        id={id}
        bind:this={canvasElm}
        width={pixelSize * 16}
        height={pixelSize * 16}
/>
