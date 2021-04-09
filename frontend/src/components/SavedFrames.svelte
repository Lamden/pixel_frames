<script>
    import { onMount } from 'svelte'

    // Components
    import Preview from './Preview.svelte'
    // MISC
    import { frameStore, activeFrame } from '../js/stores'

    onMount(() => {
        console.log(activeFrame)
        console.log({activeFrame: $activeFrame})
        console.log({frameStore: $frameStore})
    })

    const handleLoad = (index) => {
        console.log(index)
        activeFrame.set(index)
    }

    const handleDelete = (index) => {
        let deleteFrame = confirm("Delete this saved Pixel Frame?")
        if(deleteFrame){
            let newIndex = index  - 1
            if (newIndex < 0 ) newIndex = 0
            activeFrame.set(newIndex)

            frameStore.update(currentValue => {
                currentValue.splice(index, 1)
                console.log({currentValue})
                return currentValue
            })
        }
    }
</script>

<style>
    h2{
        margin-top: 3rem;
    }
    .saved_item{
        padding: 1rem;
        margin: 1rem 0;
    }
    .current{
        background: var(--primary);
    }
    .shadowbox{
        max-width: unset;
    }
    p{
        margin: 0;
        color: var(--primary-dark);
        font-weight: 300;
    }
    p strong{
        color: var(--primary);
    }
    p strong.current{
        color: var(--color-white-primary-tint);
    }
    .details{
        justify-content: space-between;
        width: 100%;
        margin-left: 1rem;
    }
</style>

<div>
    <h2>Saved</h2>
    <hr>
    {#each $frameStore as frameInfo, index}
        <div class="saved_item flex-row shadowbox" class:current={$activeFrame === index}>
            <Preview frames={frameInfo.frames} speed={frameInfo.speed} showWatermark={false} pixelSize={3} border={false}/>
            <div class="flex-row details">
                <div class="flex-col">
                    <p>Started: <strong class:current={$activeFrame === index}>{new Date(frameInfo.created).toLocaleString()}</strong></p>
                    <p>Number of Frames: <strong class:current={$activeFrame === index}>{frameInfo.frames.length}</strong></p>
                    <p>Frame Speed: <strong class:current={$activeFrame === index}>{frameInfo.speed}</strong></p>
                </div>
                <div class="flex-row flex-align-center">
                    <button
                            class="button_text outlined" class:white={$activeFrame === index}
                            on:click={() => handleDelete(index)}>
                        delete
                    </button>
                    {#if $activeFrame !== index}
                        <button class="button_text outlined" on:click={() => handleLoad(index)}>load</button>
                    {/if}
                </div>
            </div>

        </div>
    {/each}
</div>