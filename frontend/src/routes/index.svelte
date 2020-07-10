<!-- /frontend/src/routes/index.svelte -->
<script context="module">
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
		const res = await this.fetch(`http://localhost:1337/things/recent`, options)
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
</style>

<Title fontSize={8}/>

{#if $walletInstalled !== 'checking'}
	<div in:fade="{{delay: 300, duration: 500, opacity: 0.0, easing: quintOut}}">
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
	<h2 transition:fade="{{delay: 0, duration: 300}}">... Checking for Lamden Wallet ...</h2>
{/if}

<Recent {recent}/>