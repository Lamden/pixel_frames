<!-- /frontend/src/routes/_layout.svelte -->

<script>
	import Nav from '../components/Nav.svelte';
	import {onMount, afterUpdate, setContext} from 'svelte'
	import WalletController from 'lamden_wallet_controller';
	import {walletInstalled, walletInfo, showModal, userAccount} from '../js/stores.js'
	import {processTxResults} from '../js/utils.js'
	import {approvalRequest} from '../js/wallet_approval'
	import Snackbar from "../components/Snackbar.svelte";
	import Modal from "../components/Modal.svelte";

	export let segment;
	let lwc;

	onMount(() => {
		lwc = new WalletController()
		lwc.events.on('newInfo', handleWalletInfo)
		lwc.events.on('txStatus', handleTxResults)

		lwc.walletIsInstalled()
				.then(installed => {
					if (installed) walletInstalled.set('installed')
					else walletInstalled.set('not-installed')
				})

		return () => {
			lwc.events.removeListener(handleWalletInfo)
			lwc.events.removeListener(handleTxResults)
		}
	})

	setContext('app_functions', {
		sendTransaction: (transaction) => lwc.sendTransaction(transaction),
		lwc: () => {
			return lwc
		}
	})

	const handleWalletInfo = (info) => {
		if (info.errors) {
			if (info.errors[0].includes('lamdenWalletConnect')) lwc.sendConnection(approvalRequest)
		} else {
			walletInfo.set(info)
			if (!$userAccount && lwc.walletAddress) userAccount.set(lwc.walletAddress)
		}
	}


	const handleTxResults = (results) => processTxResults(results)
</script>

<style>
	main {
		position: relative;
		max-width: 95em;
		padding: 0 28px;
		margin: 1rem auto 0;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	@media (min-width: 450px) {
		.wallet-messages {
			display: block;
		}
	}
</style>
{#if $showModal.show}
	<Modal/>
{/if}
<Snackbar />
<Nav {segment}/>
<main>
	<slot></slot>
</main>