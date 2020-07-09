<script>
    import { currentColor, frames, currentFrame } from '../js/stores'
    import Pixel from './Pixel.svelte'

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

</style>

<div class="board"
     on:drag|preventDefault
     on:contextmenu|preventDefault
>
    {#each $frames[$currentFrame] as pixel, index}
        <Pixel {pixel} {index} on:colorChange={changeColor}/>
    {/each}
</div>