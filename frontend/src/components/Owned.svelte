<script>
    import { beforeUpdate } from 'svelte';
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
	.owned {
		width: 100%;
		padding: 2rem 1rem;
		flex-wrap: wrap;
		box-sizing: border-box;
		justify-content: space-evenly;
	}

	.owned > div {
		padding: 20px 20px;
		width: 180px;
		margin: 10px;
		box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
		align-items: center;
	}
	h2{
		border-top: 1px solid lightgray;
		padding-top: 1rem;
		margin-top: 2rem;
	}

</style>

<h2>Pixel Frames You Own</h2>
<div class="flex-row owned">
    {#each formatted as thingInfo}
        <div>
            <DisplayFrames pixelSize={12} {thingInfo} />
        </div>
    {/each}
</div>

