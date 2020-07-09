<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'

    const close = () => {
        frames.update(f => {
            if (f.length === 1) f = [emptyFrame($totalPixels)];
            else f.splice($currentFrame, 1)
            currentFrame.set($currentFrame > 0 ? $currentFrame - 1 : 0 )
            return f
        })
    }
</script>

<button class="button_text" value="delete" on:click ={close}> Delete Current Frame </button>