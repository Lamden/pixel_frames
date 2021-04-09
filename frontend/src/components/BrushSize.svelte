<script>
    import { brushSize, currentTool } from '../js/stores'

    $: size = $brushSize

    const handleInput = (e) => {
        brushSize.set(e.target.valueAsNumber)
    }
</script>

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

<div>
    <div class="flex-col" class:disabled={!$currentTool.includes("paint")}>
        <label >Brush Size <strong>{size}</strong></label>
        <input
            bind:value={size}
            on:input={handleInput}
            disabled={!$currentTool.includes("paint")}
            type="range"
            min="1"
            max="3"
            class="slider">
    </div>
</div>