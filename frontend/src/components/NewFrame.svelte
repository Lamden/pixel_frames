<script>
    // MISC
    import { currentFrame, frameStore, activeFrame } from '../js/stores'
    import { newPixelFrame } from '../js/defaults'

    const reset = () => {
        let wipe = confirm("Wipe project and start again?")
        if (wipe){
            currentFrame.set(0)
            frameStore.update(currentValue => {
                currentValue[$activeFrame] = newPixelFrame()
                return currentValue

            })
        }
    }
</script>

<style>
</style>

<button class="button_text" value="clear" on:click ={reset}> Start Over </button>