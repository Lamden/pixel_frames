<script>
    import { frames } from '../js/stores'
    import Frame from './Frame.svelte'
    import AddFrame from './AddFrame.svelte'
</script>
<style>
    .flex-col{
        align-items: center;
    }
    .frames > div {
        margin-bottom: 10px;
    }
</style>

<div class="flex-col">
    <h2>frames</h2>
    <div class="flex-col frames">
        {#each $frames as pixels, index }
            <div>
                <Frame {pixels} frameNum={index} />
            </div>
        {/each}
        {#if $frames.length < 3}
            <AddFrame />
       {/if}
    </div>
</div>