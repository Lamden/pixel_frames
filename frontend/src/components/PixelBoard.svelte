<script>
    import { currentColor, frames, currentFrame } from '../js/stores'
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    import Pixel from './Pixel.svelte'

    import check_circle from '../../static/img/check-circle.svg'

    export let itemCreated;

    let pixelSize = "35";
    let num_of_pixels = "16"

    const changeColor = (e) => {
        let index = e.detail.index
        let button = e.detail.button
        frames.update(f => {f[$currentFrame][index] = $currentColor[button]; return f})
    }
</script>

<style>
.board {
    grid-template-columns: repeat(16, 35px);
    grid-template-rows: repeat(16, 35px);
}
.checkmark{
    position: absolute;
}
</style>

<div class="board"
     on:drag|preventDefault
     on:contextmenu|preventDefault>
    {#each $frames[$currentFrame] as pixel, index}
        <Pixel {pixel} {index} on:colorChange={changeColor}/>
    {/each}

    {#if itemCreated}
        <div in:scale="{{duration: 500, delay: 0, opacity: 0.0, start: 0.2, easing: quintOut}}"
             class="checkmark"
             style={`width: ${pixelSize * num_of_pixels}px`}>
            {@html check_circle}
        </div>
    {/if}
</div>