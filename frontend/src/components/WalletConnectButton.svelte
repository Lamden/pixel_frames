<script>
    import { onMount } from 'svelte'
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	export let lwc ;

    $: installed = false;
    $: connected = false;
    $: locked = false;

    let storeURL = "https://chrome.google.com/webstore/detail/lamden-wallet-browser-ext/fhfffofbcgbjjojdnpcfompojdjjhdim"

    onMount(() => {
        setState()
		lwc.events.on('newInfo', setState)
        lwc.events.on('installed', (res) => installed = res)

		return () => {
			lwc.events.removeListener(setState)
		}
	})

    const setState = () => {
        installed = lwc.installed
        connected = lwc.approved
        locked = lwc.locked
    }

    const openLink = (url) => {
        if (!installed) window.open(storeURL, '_blank');
	}

</script>



{#if !installed}
    <a href="https://chrome.google.com/webstore/detail/lamden-wallet-browser-ext/fhfffofbcgbjjojdnpcfompojdjjhdim"
       target="_blank"
       rel="noopener noreferrer"
       class="button">Install Wallet</a>
{:else}
     {#if locked}
        <button class="button" on:click={() => location.reload()}>Wallet Locked</button>
    {:else}
         {#if !connected}
            <button class="button" on:click={() => lwc.sendConnection()}> Connect to Wallet</button>
         {/if}
    {/if}
{/if}





