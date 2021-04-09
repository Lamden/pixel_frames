<script>
    import { onMount } from 'svelte';
    import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    import { snackbars } from '../js/stores.js';

    import check_icon from '../../static/img/check-filled.svg'
    import warning_icon from '../../static/img/warning-filled.svg'
    import error_icon from '../../static/img/error-filled.svg'
    import info_icon from '../../static/img/info-filled.svg'

    const icons = {
        "warning": warning_icon,
        "success": check_icon,
        "error": error_icon,
        "info": info_icon
    }

    let remover;
    let screenHeight;

    onMount(() => {
        let remover = setInterval(autoClose, 2000)
        return(() => clearInterval(remover))
    })

    const autoClose = () => {
        snackbars.update( curr => {
             return curr.filter((snack ) => {return (new Date().getTime() - snack.time) < 5000})
        })
    }
</script>

<style>
    .snack-container{
        display: flex;
        flex-direction: column;
        justify-content: flex-end;

        position: fixed;
        pointer-events: none;
        top: 0;
        right: 0;
        width: 300px;
        z-index: 100;
        padding: 0 5px;
        box-sizing: border-box;
        overflow: hidden;
    }
    .snackbar{
        justify-content: space-evenly;
        padding: 8px;
        margin-bottom: 1rem;
        box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	    -webkit-box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	    -moz-box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
    }
    .top-bar{
        align-items: end;
    }
    .icon{
        width: 19px;
        margin-right: 5px;
    }
    .title{
        margin: 0 0 0.5rem;
        font-size: 0.8em;
        font-weight: 600;
    }
    .body{
        margin: 0;
        font-size: 0.8em;
        font-weight: 300;
    }
    .success{
        background: forestgreen;
        border: 1px solid darkgreen;
        color: #ebffec;
    }
    .error{
        background: indianred;
        border: 1px solid darkred;
        color: #ffecec;
    }
    .info{
        background: var(--primary);
        border: 1px solid #afafaf;
        color: #fff5fa;
    }
    .warning{
        background: khaki;
        border: 1px solid #dec157;
        color: #4b4b4b;
    }

</style>
<div class="snack-container" style={`height: ${screenHeight}px`}>
     {#each $snackbars as snack, index}
        <div class="flex-col snackbar"
             class:success={snack.type === "success"}
             class:error={snack.type === "error"}
             class:warning={snack.type === "warning"}
             class:info={snack.type === "info"}
             in:fly="{{delay: 0, duration: 400, x: 200, y: 0, opacity: 0.5, easing: quintOut}}"
             out:fly="{{delay: 0, duration: 200, x: 400, y: 0, opacity: 0.5, easing: quintOut}}">

            <div class="top-bar flex-row">
                <div class="icon">{@html icons[snack.type]}</div>
                <p class="title">{snack.title}</p>
            </div>
            <p class="body">{snack.body}</p>
        </div>
    {/each}
</div>
<svelte:window bind:innerHeight={screenHeight} />