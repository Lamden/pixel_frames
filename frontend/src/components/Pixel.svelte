<script>
    import { createEventDispatcher } from 'svelte';
    import { currentColor } from '../js/stores'
    import { letter_to_color } from '../js/utils.js'
    const dispatch = createEventDispatcher();
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
        if ($currentColor[button] == pixel) return
        dispatch('colorChange', {index, button})
    }


</script>

<style>
    .pixel{
        transition: color, 0.5s;
        transition: border, 0s;
    }
    .pixel:hover{
        border: 1px dotted #ff5bb0;
    }
</style>

<div class="pixel pixel__border" 
     style={`background: ${letter_to_color[pixel]}`}
     on:mousedown={colorChange}
     on:mouseover={colorChangeOver}
     on:drag|preventDefault />

