<script>
    import { frameSpeed, frameStore, activeFrame } from '../js/stores.js'
    import { onMount } from 'svelte'

    $: speed = $frameSpeed

    onMount(() => {
/*
        let lsSpeed = localStorage.getItem('frameSpeed')
        if (lsSpeed) frameSpeed.set(lsSpeed)
        else frameSpeed.set(1000)
*/
        return (() => {
            //if ($frameSpeed) localStorage.setItem('frameSpeed', $frameSpeed)
        })
    })

    const handleInput = (e) => {
        frameStore.update(currentValue => {
            currentValue[$activeFrame].speed = e.target.valueAsNumber
            return currentValue
        })
    }

</script>

<div class="flex-col">
    <label>Amimation Speed <strong>{speed}ms</strong></label>
    <input
        bind:value={speed}
        on:input={handleInput}
        type="range"
        min="100"
        max="2000"
        class="slider">
</div>

<style>
    label{
        margin-top: 12px;
    }

    label > strong{
        font-size: 1.1em;
        font-weight: bold;
        color: var(--primary)
    }
</style>