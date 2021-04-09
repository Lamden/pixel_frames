<script>
    import { currentFrame, frameStore, activeFrame } from '../js/stores'
    import { newPixelBoard } from '../js/defaults.js'

    const handleClick = () => {
        let wipe = confirm("Wipe current frame?")
        if (wipe) {
            frameStore.update(f => {
                f[$activeFrame].frames[$currentFrame] = newPixelBoard();
                return f
            })
        }
    }
</script>

<button class="button_text" value="clear" on:click ={handleClick}> Clear Current Frame </button>