<script>
    import { beforeUpdate } from 'svelte';
    import DisplayFrames from './DisplayFrames.svelte';

    import { decodeFrames  } from "../js/utils.js";
    import { userAccount } from '../js/stores'

    export let created;
    export let creator;

    let formatted = [];

    beforeUpdate(() => {
        formatThings();
    })

    const formatThings = () => {
        created.forEach(thing => {
            thing.frames = decodeFrames(thing.thing)
        })
        formatted =  created
    }

    formatThings();

</script>

<style>
	.created {
		width: 100%;
		padding: 2rem 1rem;
		flex-wrap: wrap;
		box-sizing: border-box;
		justify-content: space-evenly;
	}

	.created > div {
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
    p{
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .button_text{
        margin: 1px 0 0 5px;
        padding: 0;
    }
    .flex-row{
        flex-wrap: wrap;
        align-items: center;
    }

</style>

<h2>Pixel Frames Created by</h2>
<p class="flex-row">{creator === $userAccount ? 'You' : creator}
    {formatted.length == 0 ? `${creator === $userAccount ? "haven't" : "hasn't"} created anything yet!` : ""}
    {#if creator === $userAccount}
        <a href="{`/boards/${$userAccount}`}" class="button_text">CREATE!</a>
    {/if}
</p>
<div class="flex-row created">
    {#each formatted as thingInfo}
        <div>
            <DisplayFrames pixelSize={12} {thingInfo} />
        </div>
    {/each}
</div>

