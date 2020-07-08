<script>
    import { frames, currentFrame, totalPixels  } from '../js/stores'
    //import { onMount } from 'svelte'
    import closeIcon from '../../static/img/cancel-blend-filled.svg'

    export let pixels
    export let pixelSize = 5
    export let frameNum = null;
    export let preview = false;

    //let loaded1 = false

    //onMount (() => loaded1 = true)


    const close = () => {
        frames.update(f => {
            if (f.length === 1) f = [Array.from(Array($totalPixels).keys())];
            else f.splice(frameNum, 1)
            currentFrame.set($currentFrame > 0 ? frameNum - 1 : 0 )
            return f
        })
    }
</script>

<style>
    .board {
        position: relative;
    }
    .selected{
        border: 2px solid #b2d7b2;
    }
    button:focus{
        outline: 0;
    }
    .close{
        position: absolute;
        top: -8px;
        right: -3px;
        width: 17px;
        height: 17px;
        background: none;
        border: none;

    }
</style>

<div class="board"
     class:selected={frameNum !== null ? $currentFrame === frameNum : false}
     style={`grid-template-columns: repeat(16, ${pixelSize}px); grid-template-rows: repeat(16, ${pixelSize}px);`}
     on:click={() => currentFrame.set(frameNum)}>
    {#each pixels as pixel}
        <div class="pixel" style={`background: ${pixel}`} />
    {/each}
    {#if !preview}
        <button class="close" on:click={close}> {@html closeIcon} </button>
    {/if}
</div>