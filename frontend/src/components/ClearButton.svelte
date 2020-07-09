<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'
    import { emptyFrame } from '../js/utils.js'

    const clear = () => {
        let wipe = confirm("Wipe current frame?")
        if (wipe) {
            frames.update(f => {
                f[$currentFrame] = emptyFrame($totalPixels);
                return f
            })
        }
    }
</script>

<button class="button_text" value="clear" on:click ={clear}> Clear Current Frame </button>