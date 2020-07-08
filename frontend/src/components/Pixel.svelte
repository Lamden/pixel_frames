<script>
    import { createEventDispatcher } from 'svelte'; 
    const dispatch = createEventDispatcher();
    export let pixel
    export let index

    const colorChange = () => {
        dispatch('colorChange', index)
    }

</script>

<div class="pixel pixel__border" 
     style={`background: ${pixel}`} 
     on:click={colorChange}
     on:mouseover={(e) => {e.buttons === 1 ? colorChange() : null}}
     on:drag|preventDefault />