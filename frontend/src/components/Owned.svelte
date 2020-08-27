<script>
    import { beforeUpdate } from 'svelte';
    import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    import DisplayFrames from './DisplayFrames.svelte';

    import { decodeFrames, updateInfo } from "../js/utils.js";
    import { userAccount } from '../js/stores'

    export let owned;
    export let account;

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

    const updateThing = (e) => {
    	const { updates, index } = e.detail
    	updateInfo(formatted[index], updates)
		formatted = [...formatted]
	}

</script>

<style>
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
</style>

<h2>Pixel Frames Owned By</h2>
<p>{account === $userAccount ? 'You' : account}
    {formatted.length == 0 ? `${account === $userAccount ? "don't" : "doesn't"} own anything yet!` : ""}
</p>
<div class="flex-row display-card">
    {#each formatted as thingInfo, index}
        <div in:scale="{{duration: 200, delay: 0, opacity: 0, start: 0.75, easing: quintOut}}">
            <DisplayFrames pixelSize={12} {thingInfo} {index} on:update={updateThing}/>
        </div>
    {/each}
</div>

