<!-- /frontend/src/routes/_layout.svelte -->

<script>
	import Nav from '../components/Nav.svelte';
	import {onMount, beforeUpdate, setContext} from 'svelte'
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

	beforeUpdate(() => {
		if (lwc){
			if (!$userAccount && lwc.walletAddress) userAccount.set(lwc.walletAddress)
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
			if (info.errors[0].includes('no matching vk is currently found in the wallet'))
				lwc.sendConnection(approvalRequest, true, true)
		} else {
			if (info.approvals){
				if (!info.approvals.testnet) lwc.sendConnection(approvalRequest, true)
				else {
					if (!$userAccount && lwc.walletAddress) userAccount.set(lwc.walletAddress)
				}
			}
			walletInfo.set(info)
		}
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
		padding: 0 28px;
		margin: 1rem auto 0;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: center;
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