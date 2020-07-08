<script>
    import { currentColor } from '../js/stores'
    const colors = [
        '#ffffff00', 'black', 'white', 'gray', 'red', 'maroon', 'pink', 'greenyellow', 'green', 'forestgreen', 'blue', 'darkblue', 'aqua', 'purple', 'orange', 'yellow'
    ]

    const changeCurrentColor = (color) => {
        currentColor.set(color)
    }
</script>

<style>
    .pallet {
        display: grid;
        width: fit-content;
        grid-template-columns: 30px;
        grid-template-rows: repeat(16, 30px);
        grid-gap: 5px;
        color: black;
        padding: 0 20px;
    }

    .color{
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid black;
        border-radius: 99px;
    }
</style>

<div class="pallet" on:drag|preventDefault>
    {#each colors as color, index}
        <div class="color" style={`background: ${color}`} on:click={() => changeCurrentColor(color)} >
            {#if color === '#ffffff00'} X {/if}
        </div>
    {/each}
</div>