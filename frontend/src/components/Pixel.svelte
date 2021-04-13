<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    // MISC
    import { currentColor, brushSize } from '../js/stores'
    import { letter_to_color } from '../js/utils.js'

    export let pixel
    export let index

    const colorChange = (e) => {
        if (e.button == 0) dispatchColorChange(0)
        if (e.button == 2) dispatchColorChange(1)
    }

    const colorChangeOver = (e) => {
        if (e.buttons == 1) dispatchColorChange(0)
        if (e.buttons == 2) dispatchColorChange(1)
    }

    const dispatchColorChange = (button) => {
        if ($currentColor[button] == pixel && $brushSize === 1) return
        dispatch('colorChange', {index, button})
    }
</script>

<style>
    div{
        color: var(--gray-2);
    }
    .pixel{
        transition: color, 0.5s;
        transition: border, 0s;
    }
    .pixel:hover{
        border: 1px dotted var(--primary);
    }
    .errorPixel{
        background: #7fff5b!important;
        color: red!important;
    }
    .noselect {
      -webkit-touch-callout: none; /* iOS Safari */
        -webkit-user-select: none; /* Safari */
         -khtml-user-select: none; /* Konqueror HTML */
           -moz-user-select: none; /* Old versions of Firefox */
            -ms-user-select: none; /* Internet Explorer/Edge */
                user-select: none; /* Non-prefixed version, currently
                                      supported by Chrome, Edge, Opera and Firefox */
    }
</style>

<div class="pixel pixel__border noselect"
     style={`background: ${letter_to_color[pixel]}`}
     class:errorPixel={pixel === null}
     on:mousedown={colorChange}
     on:mouseover={colorChangeOver}
     on:drag|preventDefault
     title={index}>
    {#if pixel === "A"} x {/if}
    {#if pixel === null} E {/if}
</div>

