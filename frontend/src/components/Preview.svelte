<script>
    import { onMount } from 'svelte'
    import Frame from './Frame.svelte'

    export let frames;
    export let title;
    export let pixelSize = 8;

    let switcher;
    $: show = 1

    onMount(() => {
        switcher = setTimeout(switchFrames, 1000)
    })

    const switchFrames = () => {
        if (show > frames.length) show = 1
        else show = show === frames.length ? 1 : show + 1;
        switcher = setTimeout(switchFrames, 1000)
    }

</script>
<style>
    .flex-col{
        align-items: center;
        margin-bottom: 2rem;
    }
</style>

<div class="flex-col">
    {#if title}<h2>preview</h2>{/if}
    <div>
        {#if frames.length >= show}
            <Frame {pixelSize} pixels={frames[show - 1]} preview={true}/>
        {/if}
    </div>
</div>