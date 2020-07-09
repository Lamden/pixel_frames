<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'
    import { emptyFrame } from '../js/utils'
    import FrameCanvas from './FrameCanvas.svelte'
    import AddFrame from './AddFrame.svelte'
    import closeIcon from '../../static/img/cancel-blend-filled.svg'

    let pixelSize = 4;
    let gridSize = (pixelSize * 16) + pixelSize;

    const close = (frameNum) => {
        frames.update(f => {
            if (f.length === 1) f = [emptyFrame($totalPixels)];
            else f.splice(frameNum, 1)
            currentFrame.set($currentFrame > 0 ? frameNum - 1 : 0 )
            return f
        })
    }
</script>

<style>
    .flex-col{
        align-items: center;
    }
    .frames {
        display: grid;
        width: fit-content;
        grid-gap: 10px;
    }
    .frame {
        position: relative;
        line-height: 0;
        color: #ff5bb0;
        font-weight: bold;
        font-size: 0.8em;
        box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
    }
    .frame:nth-child(1)::after {
        content: "1";
        position: absolute;
        top: 35px;
        left: -14px;
    }
    .frame:nth-child(2)::after {
        content: "2";
        position: absolute;
        top: 35px;
        right: -14px;
    }
    .frame:nth-child(3)::after {
        content: "3";
        position: absolute;
        top: 35px;
        left: -14px;
    }
    .frame:nth-child(4)::after {
        content: "4";
        position: absolute;
        top: 32px;
        right: -14px;
    }
    .selected{
        border: 2px solid #ff5bb0;
    }
    .not-selected{
        border: 2px solid #afafaf;
    }
    button:focus{
        outline: 0;
    }
    .close{
        position: absolute;
        top: -1px;
        right: 3px;
        width: 17px;
        height: 17px;
        background: none;
        border: none;

    }
    .add-button{
        border: 1px dashed #ff5bb0;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>

<div class="flex-col">
    <div class="frames"
        style={`grid-template-columns: repeat(2, ${gridSize}px); grid-template-rows: repeat(2, ${gridSize}px`}>
        {#each $frames as pixels, index }
            <div class="frame">
                <div
                    class:selected={$currentFrame === index}
                    class:not-selected={$currentFrame !== index}
                    on:click={() => currentFrame.set(index)}>
                    <FrameCanvas {pixels} pixelSize={4}/>
                </div>
            </div>
        {/each}
        {#if $frames.length < 4}
            <div class="add-button">
                <AddFrame />
            </div>
        {/if}
    </div>
</div>