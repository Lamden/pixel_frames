<script>
    import { currentColor } from '../js/stores'
    import { color_to_letter, letter_to_color } from '../js/utils.js'

    $: pallet = makePallet()

    const makePallet = () => {
        let colors = JSON.parse(JSON.stringify(color_to_letter))
        delete colors['#ffffff00']
        delete colors['#ffffff']
        return colors
    }

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
    .top-pallet {
        display: grid;
        width: fit-content;
        grid-template-columns: repeat(2, 30px);
        grid-template-rows: repeat(1, 30px);
        grid-gap: 4px;
        margin-bottom: 4px;
    }
    .pallet {
        display: grid;
        width: fit-content;
        grid-template-columns: repeat(5, 30px);
        grid-template-rows: repeat(11, 30px);
        grid-gap: 4px;
    }

    .color{
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid #afafaf;
        border-radius: 5px;
        font-weight: bold;
        color: darkgray;
    }
    .color:hover{
        position: relative;
        top: -2px;
        z-index: 1;
        box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
	    -webkit-box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
	    -moz-box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
    }
    .selected{
        border: 2px solid var(--primary);
    }
    .selected-colors{
        display: grid;
        width: fit-content;
        grid-template-columns: 46px 46px;
        grid-template-rows: 46px;
        grid-gap: 2px;
        padding: 1rem;
        border: 1px dashed var(--primary);
        margin-bottom: 3rem;
    }
    .selected-colors > div {
        position: relative;
        box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
	    -webkit-box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
	    -moz-box-shadow: 0px 10px 14px -7px rgba(0,0,0,0.75);
        border: 1px solid #afafaf;
        border-radius: 5px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: darkgray;
        font-size: 1.2em;
    }
    .flex-col{
        align-items: center;
        padding-left: 3rem;
    }
    label{
        position: absolute;
        top: -19px;
        left: 18px;
        font-size: 0.7em;
        color: var(--primary);
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
            {$currentColor[0] === "A" ? "X" : ""}
            <label>L</label>
        </div>
        <div
            style={`background: ${letter_to_color[$currentColor[1]]}`}
            on:click={e => changePrimary(e, $currentColor[1])}>
            {$currentColor[1] === "A" ? "X" : ""}
            <label>R</label>
        </div>
    </div>
    <div class="top-pallet" >
        <div class="color"
             style={`background: #ffffff00`}
             on:click={e => changePrimary(e, color_to_letter['#ffffff00'])}
             on:contextmenu|preventDefault={e => changeSecondary(e, color_to_letter['#ffffff00'])}>
             X
        </div>
        <div class="color"
             style={`background: white`}
             on:click={e => changePrimary(e, color_to_letter['white'])}
             on:contextmenu|preventDefault={e => changeSecondary(e, color_to_letter['white'])}>
        </div>
    </div>

    <div class="pallet" >
        {#each Object.keys(pallet) as color}
            <div class="color"
                 style={`background: ${color}`}
                 on:click={e => changePrimary(e, color_to_letter[color])}
                 on:contextmenu|preventDefault={e => changeSecondary(e, color_to_letter[color])}>
                {#if color === '#ffffff00'} X {/if}
            </div>
        {/each}
    </div>
</div>

