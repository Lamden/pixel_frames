<!-- /frontend/src/routes/_layout.svelte -->

<script>
	import Nav from '../components/Nav.svelte';
	import {onMount, beforeUpdate, setContext} from 'svelte';
	//import WalletController from 'lamden_wallet_controller';
	import WalletController from '../js/walletController.js';
	import {walletInstalled, walletInfo, showModal, userAccount, stampRatio, currency, autoTx} from '../js/stores.js';
	import {processTxResults, createSnack} from '../js/utils.js';
	import { config } from '../js/config.js';
	import {approvalRequest} from '../js/wallet_approval';
	import Snackbar from "../components/Snackbar.svelte";
	import Modal from "../components/Modal.svelte";
	import CreatedWithLove from "../components/CreatedWithLove.svelte";

	export let segment;
	let lwc;

	onMount(() => {
		lwc = new WalletController(approvalRequest)
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

	beforeUpdate(() => {
		if (lwc) {
			if (!$userAccount && lwc.walletAddress) userAccount.set(lwc.walletAddress)
		}
		if ($stampRatio === 1) fetchStamps();
	})

	const fetchStamps = () => {
		fetch(`${config.blockExplorer}/lamden/stamps`)
				.then(res => res.json())
				.then(res => {
					if (res.value) stampRatio.set(parseInt(res.value))
				})
	}

	setContext('app_functions', {
		sendTransaction: (transaction, callback) => sendTransaction(transaction, callback),
		lwc: () => {
			return lwc
		}
	})

	const sendTransaction = (transaction, callback) => {
		transaction.stampLimit = determineStamps()
		lwc.sendTransaction(transaction, callback)
	}

	const determineStamps = () => {
		let maxStamps = $stampRatio * 5;
		if (($currency * $stampRatio) < maxStamps) return parseInt(($currency * $stampRatio) * 0.95)
		return parseInt(maxStamps)
	}

	const handleWalletInfo = (info) => {
		autoTx.set(lwc.autoTransactions)
		userAccount.set(lwc.walletAddress)
		walletInfo.set(info)
	}


	const handleTxResults = (results) => {
		let errors = processTxResults(results)
		if (errors.length > 0) {
			if (errors[0].includes('have not been approved for')) lwc.sendConnection(approvalRequest, true)
		}
	}


</script>

<style>
	main {
		position: relative;
		max-width: 95em;
		padding: 0 28px 10rem;
		margin: 1rem auto 0;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: center;
		flex-grow: 1;
	}
	@media (min-width: 450px) {
		main {
			padding: 0 28px 10rem;
			margin: 0 auto 0;
		}
	}
</style>
{#if $showModal.show}
	<Modal/>
{/if}
<Snackbar />
<Nav {segment} {lwc}/>
<main>
	<slot></slot>
</main>
<CreatedWithLove />
