<script>
    import { writable} from 'svelte/store';
    // Components
    import Preview from './Preview.svelte'

    // MISC
    import { frameStore, activeFrame } from '../js/stores'

    let copied = writable({})

    const handleLoad = (index) => {
        activeFrame.set(index)
    }

    const handleDelete = (index) => {
        let deleteFrame = confirm("Delete this saved Artwork?")
        if(deleteFrame){
            let newIndex = index  - 1
            if (newIndex < 0 ) newIndex = 0
            activeFrame.set(newIndex)

            frameStore.update(currentValue => {
                currentValue.splice(index, 1)
                return currentValue
            })
        }
    }

    const handlePaste = () => {
        navigator.clipboard.readText()
        .then(text => {
            try {
                let frameData = JSON.parse(text)
                frameStore.add(frameData)
            }catch(e){
                console.log(e)
            }
        });
    }
    const handleCopy = (index) => {
        navigator.clipboard.writeText(JSON.stringify($frameStore[index]))
        copied.update(currstore => {
            currstore[index] = true
            return currstore
        })
        setTimeout(() => {
            copied.update(currstore => {
                delete currstore[index]
                return currstore
            })
        }, 1500)
    }

</script>

<style>
    .saved_container{
        padding: 0 28px;
    }
    h2{
        margin-top: 3rem;
    }
    .saved_item{
        padding: 1rem;
        margin: 1rem 0;
    }
    .outlined{
        border: 1px dotted var(--primary);
        margin-left: 10px;
    }
    .outlined.white{
        border: 1px dotted var(--color-white-primary-tint);
        margin-left: 10px;
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
    .paste_button{
        margin: 1rem 0 0.5rem;
    }
    .copied_button{
        transition: background-color 0.5s;
    }
    .copied{
        background: var(--color-success);
    }
</style>

<div class="saved_container">
    <h2>Saved</h2>
    <hr>
    <button class="button paste_button" on:click={handlePaste}>paste from clipboard</button>
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
                            class="button_text outlined"
                            class:white={$activeFrame === index}
                            on:click={() => handleDelete(index)}>
                        delete
                    </button>
                    <button
                            class="copied_button button_text outlined"
                            class:copied={$copied[index]}
                            class:white={$activeFrame === index}
                            on:click={() => handleCopy(index)}>
                        copy
                    </button>
                    {#if $activeFrame !== index}
                        <button class="button_text outlined" on:click={() => handleLoad(index)}>load</button>
                    {/if}
                </div>
            </div>

        </div>
    {/each}
</div>