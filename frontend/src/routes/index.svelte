<!-- /frontend/src/routes/index.svelte -->
<script context="module">
	import { config } from '../js/config.js'
	export async function preload(parms) {
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				contractName: 'con_pf_test',
				variableName: 'S'
			})
		}
		const res = await this.fetch(`${config.blockExplorer}/things/recent`, options)
		let data = await res.json()
		if (!data) data = []
	    return {recent: data}
	}
</script>

<script>
	import {goto} from '@sapper/app';
	import {fade} from 'svelte/transition';
	import {quintOut} from 'svelte/easing';
	import {walletInstalled, walletInfo, snackbars} from '../js/stores'
	import Recent from '../components/Recent.svelte'

	//Components
	import GetWallet from '../components/GetWallet.svelte'
	import Unlock from '../components/Unlock.svelte'
	import Title from "../components/Title.svelte";

	export let recent;

	$: account = $walletInfo.wallets ? $walletInfo.wallets[0] : undefined;
	$: locked = $walletInfo.locked ? $walletInfo.locked : undefined;
	$: installed = $walletInstalled

	const login = () => goto('/boards/' + account)

</script>

<style>
	*{
		text-align: center;
	}
	.wallet-messages{
		display: none;
	}
	@media (min-width: 450px) {
		.wallet-messages {
			display: block;
		}
		.mobile-message{
			display: none;
		}

	}
</style>

<div class="wallet-messages">
	<Title class="wallet-messages" fontSize={8}/>
</div>

<div class="mobile-message">
	<strong>This site is not mobile optimized.</strong>>
	Please visit us on a desktop for the full experience including integration with the Lamden Wallet to enable
	<strong>buying, selling and creating Pixel Frames animations!</strong>
</div>

{#if $walletInstalled !== 'checking'}
	<div class="wallet-messages"
		 in:fade="{{delay: 300, duration: 500, opacity: 0.0, easing: quintOut}}">
		{#if $walletInstalled === 'installed'}
			{#if $walletInfo.locked == true}
				<Unlock />
			{/if}
			{#if $walletInfo.locked == false}
				<button class="button" on:click={login}>Create!</button>
			{/if}
			{#if $walletInfo.locked == undefined}
				<h2>Please Approve My Token website!</h2>
			{/if}
		{/if}

		{#if $walletInstalled === 'not-installed'}
			<GetWallet />
		{/if}
	</div>
{:else}
	<h2 class="wallet-messages" transition:fade="{{delay: 0, duration: 300}}">... Checking for Lamden Wallet ...</h2>
{/if}

<Recent {recent}/>