<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'
    import { emptyFrame } from '../js/utils'
    import { config } from '../js/config'
    import FrameCanvas from './FrameCanvas.svelte'
    import AddFrame from './AddFrame.svelte'
    import MoveFrameButton from './MoveFrameButton.svelte'

    let pixelSize = 2;
    let gridSize = (pixelSize * config.frameWidth) + pixelSize;

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
    .frames{
        margin-bottom: 12px;
    }
    .frame {
        position: relative;
        line-height: 0;
        color: var(--primary);
        font-weight: bold;
        font-size: 0.8em;

        margin-right: 12px;
    }
    .frame::after {
        content: attr(title);
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translate(-50%, 0);
    }
    .selected{
        border: 2px solid var(--primary);
        box-shadow: 0px 10px 12px -7px rgb(0 0 0 / 50%);
		-webkit-box-shadow: 0px 10px 12px -7px rgb(0 0 0 / 50%);
		-moz-box-shadow: 0px 10px 12px -7px rgb(0 0 0 / 50%);
    }
    .not-selected{
        border: 2px solid #afafaf;
        box-shadow: 0px 8px 5px -7px rgb(0 0 0 / 50%);
		-webkit-box-shadow: 0px 8px 5px -7px rgb(0 0 0 / 50%);
		-moz-box-shadow: 0px 8px 5px -7px rgb(0 0 0 / 50%);
    }
    .add-button{
        border: 1px dashed var(--primary);
        display: flex;
        justify-content: center;
        align-items: center;

        position: relative;
        line-height: 0;

    }
    .add-button::after {
        content: 'add';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translate(-50%, 0);
        color: var(--primary);
        font-weight: bold;
        font-size: 0.8em;
    }
    span{
        width: 100px;
        line-height: 1.1;
    }
    span > strong {
        color: var(--primary);
        font-size: 1.2em;
        margin-left: 3px;
    }
</style>

<div class="flex-row frames">
    <span>Animation Frames <strong>{$frames.length}</strong></span>
    {#each $frames as pixels, index }
        <div class="frame" title={index + 1}>
            {#if $currentFrame === index}<MoveFrameButton direction="left" width="15px" {index}/> {/if}
            <div
                class:selected={$currentFrame === index}
                class:not-selected={$currentFrame !== index}
                on:click={() => currentFrame.set(index)}>
                <FrameCanvas {pixels} {pixelSize}/>
            </div>
            {#if $currentFrame === index}<MoveFrameButton direction="right" width="15px" {index}/>{/if}
        </div>
    {/each}
    {#if $frames.length < 8}
        <div class="add-button" style={`width: ${config.frameWidth * pixelSize }px;`}>
            <AddFrame />
        </div>
    {/if}

</div>