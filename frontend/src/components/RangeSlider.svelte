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
        console.log(e.target.valueAsNumber)
        console.log(speed)
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
    input[type=range] {
      -webkit-appearance: none;
      margin: 8px 0;
      width: 100%;
    }
    input[type=range]:focus {
      outline: none;
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