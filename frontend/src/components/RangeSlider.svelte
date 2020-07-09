<script>
    import { frameSpeed } from '../js/stores.js'
    import { onMount } from 'svelte'

    onMount(() => {
        let lsSpeed = localStorage.getItem('frameSpeed')
        if (lsSpeed) frameSpeed.set(lsSpeed)
        else frameSpeed.set(1000)
        return (() => localStorage.setItem('frameSpeed', $frameSpeed))
    })

</script>

<div class="flex-row">
     <input
         bind:value={$frameSpeed}
         type="range"
         min="100"
         max="2000"
         class="slider">
    <label>{$frameSpeed}ms</label>
</div>

<style>
    .flex-row{
        justify-content: space-between;
        align-items: center;
        width: 160px;
    }
    label{
        font-size: 0.8em;
        font-weight: bold;
        color: var(--primary)
    }
    input[type=range] {
      -webkit-appearance: none;
      margin: 15px 0;
      width: 62%;
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