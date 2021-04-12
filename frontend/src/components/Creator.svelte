<script>
    import { beforeUpdate } from 'svelte';
    import DisplayFrames from './DisplayFrames.svelte';

    // MISC
    import { decodeFrames, formatAccountAddress, isLamdenKey  } from "../js/utils.js";
    import { userAccount } from '../js/stores'
    import { config } from '../js/config'

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
        box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
	    -webkit-box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
	    -moz-box-shadow: 2px 6px 19px 0px var(--box-shadow-primary-dark);
		align-items: center;
        border-radius: 5px;
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
    a{
		color: var(--primary);
	}

</style>
<h2 class="text-color-primary-dark">
	All NFTs Created by
	{#if isLamdenKey(creator)}
		<a href="{`${config.blockExplorer}/addresses/${creator}`}" >{formatAccountAddress(creator, 8, 5)}</a>
	{:else}
		{creator.length > 15 && !creator.startsWith("con_") ? formatAccountAddress(creator, 8, 5) : creator}
	{/if}
</h2>

{#if formatted.length == 0}
	<p>
		{`${creator === $userAccount ? "You haven't" : "This user hasn't"} created anything yet!`}
	</p>
{/if}
<div class="flex-row created">
    {#each formatted as thingInfo}
        <div>
            <DisplayFrames pixelSize={7} {thingInfo} />
        </div>
    {/each}
</div>

