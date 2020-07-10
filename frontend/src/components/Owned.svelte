<script>
    import { onMount, beforeUpdate } from 'svelte';
    import DisplayFrames from './DisplayFrames.svelte';

    import { decodeFrames  } from "../js/utils.js";

    export let owned;


    let formatted = [];

    beforeUpdate(() => {
        formatThings();
    })

    const formatThings = () => {
        owned.forEach(thing => {
            thing.frames = decodeFrames(thing.thing)
        })
        formatted =  owned
    }

    formatThings();

</script>

<style>
    .owned{
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        width: 100%;
        margin-bottom: 2rem;
        justify-content: space-evenly;
    }
    .owned {
		width: 100%;
		padding: 2rem 1rem;
		flex-wrap: wrap;

	}

	.owned > div {
        height: 300px;
        width: min-content;
		padding: 20px;
		margin: 10px;
		box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	}

</style>

<div class="owned">
    {#each formatted as thingInfo}
        <div>
            <DisplayFrames pixelSize={12} {thingInfo} />
        </div>
    {/each}
</div>

