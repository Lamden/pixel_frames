<script>
    import { onMount } from 'svelte';
    import { fly } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    // Misc
    import { snackbars } from '../js/stores.js';

    // Icons
    import CheckIcon from '../../static/img/check-filled.svg'
    import WarningIcon from '../../static/img/warning-filled.svg'
    import ErrorIcon from '../../static/img/error-filled.svg'
    import InfoIcon from '../../static/img/info-filled.svg'

    // Components
    import Preview from './Preview.svelte';

    const icons = {
        "warning": WarningIcon,
        "success": CheckIcon,
        "error": ErrorIcon,
        "info": InfoIcon
    }

    let remover;
    let screenHeight;

    onMount(() => {
        let remover = setInterval(autoClose, 1000)
        return(() => clearInterval(remover))
    })

    const autoClose = () => {
        snackbars.update( curr => {
             return curr.filter((snack ) => {return (new Date().getTime() - snack.time) < snack.delay})
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
        padding: 8px;
        margin-bottom: 1rem;
        box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	    -webkit-box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	    -moz-box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
        z-index: 1;
    }
    .top-bar{
        align-items: end;
    }
    .icon{
        width: 26px;
        padding: 0 21px 0 13px;
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
        color: var(--primary-dark);
    }
    .warning{
        background: khaki;
        border: 1px solid #dec157;
        color: #4b4b4b;
    }
    .snackbar > a {
        margin-right: 8px;
    }

</style>
<div class="snack-container" style={`height: ${screenHeight}px`}>
     {#each $snackbars as snack, index}
         <div class="flex-row snackbar flex-align-center"
              class:success={snack.type === "success"}
              class:error={snack.type === "error"}
              class:warning={snack.type === "warning"}
              class:info={snack.type === "info"}
              in:fly="{{delay: 0, duration: 400, x: 200, y: 0, opacity: 0.5, easing: quintOut}}"
              out:fly="{{delay: 0, duration: 200, x: 400, y: 0, opacity: 0.5, easing: quintOut}}">

             {#if snack.thingInfo}
                <a href="{`./frames/${snack.thingInfo.uid}`}">
                    <Preview
                            {index}
                            solidBorder={true}
                            solidBorderColor="#00d6a22b"
                            frames={snack.thingInfo.frames}
                            pixelSize={2}
                            thingInfo={snack.thingInfo}
                            showWatermark={false} border={false}
                    />
                </a>
             {:else}

                 <div class="icon flex flex-center-center">
                     <svelte:component this={icons[snack.type]} width="26" />
                 </div>
             {/if}
             <div class="flex-col">
                <div class="top-bar flex-row">
                    <p class="title">{snack.title}</p>
                </div>
                <p class="body">{snack.body}</p>
            </div>
         </div>
    {/each}
</div>
<svelte:window bind:innerHeight={screenHeight} />