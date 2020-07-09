<script>
    import { frames, currentFrame } from '../js/stores'

    const addFrame = () => {
        if ($frames.length < 5) {
            frames.update(f => {
                f.push(Array.from(f[f.length - 1]));
                return f
            })
            currentFrame.set($frames.length - 1)
        }
    }
</script>

<style>
    .button{
        width: 24px;
        height: 24px;
        padding: 0;
    }
</style>

<button class="button" on:click={addFrame}>
    +
</button>
