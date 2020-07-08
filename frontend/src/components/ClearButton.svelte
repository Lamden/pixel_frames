<script>
    import { frames, currentFrame, totalPixels } from '../js/stores'

    const clear = () => {
        frames.update(f => {f[$currentFrame] = Array.from(Array($totalPixels).keys()); return f})
    }
</script>

<style>
    .button_text {
        padding: 5px;
        margin: 5px;
    }
</style>

<button class="button_text" value="clear" on:click ={clear}> Clear </button>