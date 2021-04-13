<script>
    import { scale } from 'svelte/transition';
    import { blur } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    // MISC
    import { currentColor, frames, currentFrame, frameStore, activeFrame, currentTool, brushSize } from '../js/stores'
    import { indexToPos } from '../js/utils'
    import { config } from '../js/config'
    import { brushSizeMap } from '../js/defaults'

    // Components
    import Pixel from './Pixel.svelte'

    // Pictures
    import check_circle from '../../static/img/check-circle.svg'

    export let itemCreated;

    let painting = false;

    let pixelSize = "35";
    let num_of_pixels = config.frameWidth

    const handleClick = (e) => {
        if (painting) return;
        let index = e.detail.index
        let button = e.detail.button
        if ($currentTool === "paint-1") paint(index, button)
        if ($currentTool === "fill") fill(index, button)
    }

    const changeColor = (index, button) => {
        let color = $currentColor[button]
        if (!color) {
            console.log({index, color})
            return
        }
        frameStore.update(currentValue => {
            let framesInfo = currentValue[$activeFrame].frames
            framesInfo[$currentFrame][index] = color
            return currentValue
        })
    }

    const paint = (index, button) => {
        let painting = true;
        let center = index;
        let centerPos = indexToPos(index)
        let topLeft = (center - (brushSizeMap[$brushSize][0] * config.frameWidth)) - brushSizeMap[$brushSize][0]
        let minY = centerPos.y - brushSizeMap[$brushSize][0]
        if (minY < 0 ) minY = 0
        let maxY = centerPos.y + brushSizeMap[$brushSize][0]
        if (maxY > config.frameWidth - 1 ) maxY = config.frameWidth - 1
        let minX = centerPos.x - brushSizeMap[$brushSize][0]
        if (minX < 0 ) minX = 0
        let maxX = centerPos.x + brushSizeMap[$brushSize][0]
        if (maxX > config.frameWidth - 1 ) maxX = config.frameWidth - 1

        for (let y = 0; y <= brushSizeMap[$brushSize][1] ; y++){
            for (let x = 0; x <= brushSizeMap[$brushSize][1] ; x++){
                let pixelToPaint = (topLeft + (config.frameWidth * y)) + x
                let pixelToPaintPos = indexToPos(pixelToPaint)
                if (
                    pixelToPaintPos.y >= minY &&
                    pixelToPaintPos.y <= maxY &&
                    pixelToPaintPos.x >= minX &&
                    pixelToPaintPos.x <= maxX &&
                    pixelToPaint >= 0 &&
                    pixelToPaint <= config.totalPixels - 1) {
                    if ($frameStore[$activeFrame].frames[$currentFrame][pixelToPaint] !== $currentColor[button]) {
                        changeColor(pixelToPaint, button)
                    }
                }
            }
        }
        painting = false;
    }

    const fill = async (index, button) => {
        let painting = true;
        const colorFrom = $frameStore[$activeFrame].frames[$currentFrame][index]
        let checked = new Set([])

        const paintAround = async (pixelIndex) => {
            let row = parseInt(index / config.frameWidth )
            let leftBoundery = row * config.frameWidth
            let rightBoundery = (leftBoundery + config.frameWidth) - 1

            let center = pixelIndex
            let left = center - 1
            let right = center + 1
            let up = center - 25
            let down = center + 25
            let pixelsToPaint = [
                center,
                left >= leftBoundery ? left : null,
                right <= rightBoundery ? right : null,
                up,
                down
            ].filter(f => {
                if (f === null) return false
                let pixelColor = $frameStore[$activeFrame].frames[$currentFrame][f]
                return f >= 0 &&
                        f <= config.totalPixels - 1 &&
                        !checked.has(f) &&
                        pixelColor === colorFrom
            })
            checked = new Set([...checked, ...pixelsToPaint])
            pixelsToPaint.map(pixel => {
                changeColor(pixel, button)
                paintAround(pixel)
            })
        }
        await paintAround(index)
        painting = false;
    }
</script>

<style>
    .board {
        grid-template-columns: repeat(25, 25px);
        grid-template-rows: repeat(25, 25px);

    }
    .paint-cursor{
        cursor: url('/img/paint_brush.svg') 5 7, auto;
    }
    .fill-cursor{
        cursor: url('/img/paint_bucket.svg') 5 20, auto;
    }
    .checkmark{
        position: absolute;
    }
</style>

<div class="board"
     class:fill-cursor={$currentTool === 'fill'}
     class:paint-cursor={$currentTool.startsWith('paint')}
     on:drag|preventDefault
     on:contextmenu|preventDefault>
    {#if $frames && Array.isArray($frames[$currentFrame])}
        {#each $frames[$currentFrame] as pixel, index}
            <Pixel {pixel} {index} on:colorChange={handleClick}/>
        {/each}
    {/if}

    {#if itemCreated}
        <div in:scale="{{duration: 1000, delay: 0, opacity: 0.0, start: 0.2, easing: quintOut}}"
             out:blur="{{duration: 1000, delay: 0, opacity: 0.0, amount: 20, easing: quintOut}}"
             class="checkmark"
             style={`width: ${config.totalPixels}px`}>
            {@html check_circle}
        </div>
    {/if}
</div>