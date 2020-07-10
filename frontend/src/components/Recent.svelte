

<script>
	import DisplayFrames from './DisplayFrames.svelte';
	import { decodeFrames  } from "../js/utils";

	export let recent;

    let formatted = [];

    const formatThings = () => {
        recent.forEach(thing => {
            thing.frames = decodeFrames(thing.thing)
        })
        formatted =  recent
    }

    formatThings();

</script>

<style>
	.recent {
		width: 100%;
		padding: 2rem 1rem;
		flex-wrap: wrap;
		box-sizing: border-box;
	}

	.recent > div {
		padding: 20px;
		margin: 10px;
		box-shadow: 2px 6px 19px 0px rgba(0,0,0,0.29);
	}
	h2{
		border-top: 1px solid lightgray;
		padding-top: 1rem;
		margin-top: 2rem;
	}
</style>

<h2>Recent Creations</h2>
<div class="flex-row recent">
    {#each formatted as thingInfo}
		<div>
			<DisplayFrames pixelSize={8} {thingInfo} title={false}/>
		</div>
    {/each}
</div>
