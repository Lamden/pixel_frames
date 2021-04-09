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
    input[type=range] {
      -webkit-appearance: none;
      margin: 8px 0;
      width: 100%;
    }
    input[type=range]:focus {
      outline: none;
    }
    .disabled {
      opacity: 0.5;
    }
    input[type=range]::-webkit-slider-runnable-track {
      width: 100%;
      height: 8.4px;
      cursor: pointer;
      background: var(--primary);
      border-radius: 1.3px;
      border: 0.2px solid #afafaf;
    }
    input[type=range]::-webkit-slider-thumb {
      border: 1px solid #afafaf;
      height: 18px;
      width: 18px;
      border-radius: 15px;
      background: #ffffff;
      cursor: pointer;
      -webkit-appearance: none;
      margin-top: -6px;
    }
    input[type=range]:focus::-webkit-slider-runnable-track {
      background: var(--primary);
    }
    input[type=range]::-moz-range-track {
      width: 100%;
      height: 8.4px;
      cursor: pointer;
      background: var(--primary);
      border-radius: 1.3px;
      border: 0.2px solid #afafaf;
      box-shadow: none;
    }
    input[type=range]::-moz-range-thumb {
      border: 1px solid #afafaf;
      height: 18px;
      width: 18px;
      border-radius: 15px;
      background: #ffffff;
      cursor: pointer;
    }
    input[type=range]::-ms-track {
      width: 100%;
      height: 8.4px;
      cursor: pointer;
      background: transparent;
      border-color: transparent;
      border-width: 16px 0;
      color: transparent;
    }
    input[type=range]::-ms-fill-lower {
      background:  var(--primary);
      border: 0.2px solid #afafaf;
      border-radius: 2.6px;
    }
    input[type=range]::-ms-fill-upper {
      background:  var(--primary);
      border: 0.2px solid #afafaf;
      border-radius: 2.6px;
    }
    input[type=range]::-ms-thumb {
      border: 1px solid #afafaf;
      height: 18px;
      width: 18px;
      border-radius: 15px;
      background: #ffffff;
      cursor: pointer;
    }
    input[type=range]:focus::-ms-fill-lower {
      background:  var(--primary);
    }
    input[type=range]:focus::-ms-fill-upper {
      background:  var(--primary);
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