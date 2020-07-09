<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'
    import { emptyFrame } from '../js/utils.js'

    const reset = () => {
        let wipe = confirm("Wipe project and start again?")
        if (wipe){
            currentFrame.set(0)
            frames.set([emptyFrame($totalPixels)])
        }
    }
</script>

<style>
</style>

<button class="button_text" value="clear" on:click ={reset}> Start Over </button>