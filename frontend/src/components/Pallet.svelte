<script>
    import { currentColor } from '../js/stores'
    import { color_to_letter, letter_to_color } from '../js/utils.js'

    const changeCurrentColor = (index, letter) => {
        currentColor.update( curr => {
            curr[index] = letter;
            return curr
        })
    }

    const changePrimary = (e, letter) => {
        changeCurrentColor(0, letter)
    }
    const changeSecondary = (e, letter) => {
        changeCurrentColor(1, letter)
    }
</script>

<style>
    .pallet {
        display: grid;
        width: fit-content;
        grid-template-columns: repeat(3, 30px);
        grid-template-rows: repeat(9, 30px);
        grid-gap: 2px;
    }

    .color{
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #afafaf;
        border-radius: 5px;
    }
    .color:hover{
        position: relative;
        top: -2px;
        z-index: 1;
        box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
    }
    .selected{
        border: 2px solid #ff5bb0;
    }
    .selected-colors{
        display: grid;
        width: fit-content;
        grid-template-columns: 46px 46px;
        grid-template-rows: 46px;
        grid-gap: 2px;
        padding: 1rem;
        border: 1px dashed #ff5bb0;
        margin-bottom: 3rem;
    }
    .selected-colors > div {
        position: relative;
        box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
        border: 1px solid #afafaf;
        border-radius: 5px;
    }
    .flex-col{
        align-items: center;
        padding-left: 3rem;
    }
    label{
        position: absolute;
        top: -18px;
        left: 20px;
        font-size: 0.8em;
        color: #ff5bb0;
        font-weight: bold;
    }
</style>

<div class="flex-col"
     on:drag|preventDefault
     >
    <div class="selected-colors">
        <div
            style={`background: ${letter_to_color[$currentColor[0]]}`}
            on:contextmenu|preventDefault={e => changeSecondary(e, $currentColor[0])}>
            <label>L</label>
        </div>
        <div
            style={`background: ${letter_to_color[$currentColor[1]]}`}
            on:click={e => changePrimary(e, $currentColor[1])}>
            <label>R</label>
        </div>
    </div>
    <div class="pallet" >
        {#each Object.keys(color_to_letter) as color}
            <div class="color"
                 class:selected={color_to_letter[color] === $currentColor}
                 style={`background: ${color}`}
                 on:click={e => changePrimary(e, color_to_letter[color])}
                 on:contextmenu|preventDefault={e => changeSecondary(e, color_to_letter[color])}>
                {#if color === '#ffffff00'} X {/if}
            </div>
        {/each}
    </div>

</div>

