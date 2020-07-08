<script>
    import { frames, currentFrame } from '../js/stores'

    const addFrame = () => {
        if ($frames.length < 4) {
            frames.update(f => {
                f.push(Array.from(f[f.length - 1]));
                console.log(f);
                return f
            })
            currentFrame.set($frames.length - 1)
        }
    }
</script>

<style>
    .button{
        width: 25px;
        height: 25px;
        padding: 0;
    }
</style>

<button class="button" on:click={addFrame}>
    +
</button>
