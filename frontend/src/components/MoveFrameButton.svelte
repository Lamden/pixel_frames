<script>
    import { tick } from 'svelte'
    import { activeFrame, frameStore, frames, currentFrame } from '../js/stores'
    export let index
    export let width = "10px"
    export let direction = "right"

    $: firstFrame = index <= 0
    $: lastFrame = index >= ($frames.length - 1)


    const handleClick = () => {
        if (direction === "left" && !firstFrame) moveArrayItemToNewIndex(index, index - 1)
        if (direction === "right" && !lastFrame) moveArrayItemToNewIndex(index, index + 1)
    }

    const moveArrayItemToNewIndex = async (old_index, new_index) => {
        frameStore.update(currentValue => {
            if (new_index >= currentValue[$activeFrame].frames.length) {
                var k = new_index - currentValue[$activeFrame].frames.length + 1;
                while (k--) {
                    currentValue[$activeFrame].frames.push(undefined);
                }
            }
            currentValue[$activeFrame].frames.splice(new_index, 0, currentValue[$activeFrame].frames.splice(old_index, 1)[0]);
            return currentValue
        })
        await tick()
        currentFrame.set(new_index)
    };

</script>

<style>
    div{
        cursor: pointer;
    }
    .right{
        position: absolute;
        top: 50%;
        right: -14px;
        transform: translate(0, -50%);
    }
    .left{
        position: absolute;
        top: 50%;
        left: -14px;
        transform: translate(0, -50%);
    }
    path:hover{
        fill: var(--primary);
    }

</style>

<div on:click={handleClick}>
   {#if direction === "right" && !lastFrame}
        <svg {width} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="right">
            <path fill="#221b38" d="M8 4V20L16 12L8 4Z" undefined="1"></path>
        </svg>
    {/if}

    {#if direction === "left" && !firstFrame}
        <svg {width} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="left">
            <path fill="#221b38" d="M16 4V20L8 12L16 4Z" undefined="1"></path>
        </svg>
    {/if}
</div>
