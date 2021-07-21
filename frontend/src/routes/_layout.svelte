<!-- /frontend/src/routes/_layout.svelte -->

<script>
	// TODO - Royalties displayed on buy page
	// TODO - Backup Warning for Wallet connection
	// TODO - disclaimer when creating NFT
	// TODO - disclaimer when buying NFT
	// TODO - disclaimer when selling NFT

	import {onMount, beforeUpdate, setContext} from 'svelte';

	// Components
	import Nav from '../components/Nav.svelte';
	import WalletController from 'lamden_wallet_controller';
	import Snackbar from "../components/Snackbar.svelte";
	import Modal from "../components/Modal.svelte";
	import CreatedWithLove from "../components/CreatedWithLove.svelte";
	import AuctionUpdates from "../components/AuctionUpdates.svelte";

	// Misc
	import {approvalRequest} from '../js/wallet_approval';
	import { config, stampLimits } from '../js/config.js';
	import { walletInstalled, walletInfo, showModal, userAccount, stampRatio, currency, autoTx, tabHidden, tauPrice, approvalAmount } from '../js/stores.js';
	import {processTxResults, createSnack, refreshTAUBalance, checkForApproval, stringToFixed, toBigNumber} from '../js/utils.js';
	import { TransactionResultHandler } from '../js/transaction_result_handler'
	import * as socketservice from '../js/socketservice'


	export let segment;

	let lwc;
	let lastCurrencyCheck = new Date()
	let txResultsHandler = TransactionResultHandler(createSnack)
	let socket = socketservice.start()

	onMount(() => {
		lwc = new WalletController(approvalRequest)
		lwc.events.on('newInfo', handleWalletInfo)
		lwc.events.on('txStatus', handleTxResults)

		lwc.walletIsInstalled()
				.then(installed => {
					if (installed) walletInstalled.set('installed')
					else walletInstalled.set('not-installed')
				})

		document.addEventListener("visibilitychange", setTabActive);
		refreshCurrencyBalance()
		refreshTauPrice()
		checkForApproval(config.masterContract)

		socket.on('')

		return () => {
			lwc.events.removeListener(handleWalletInfo)
			lwc.events.removeListener(handleTxResults)
			document.removeEventListener("visibilitychange", setTabActive);
		}
	})

	beforeUpdate(() => {
		if (lwc) {
			if (!$userAccount && lwc.walletAddress) userAccount.set(lwc.walletAddress)
		}
		if (!$stampRatio) fetchStampRatio();
	})

	const fetchStampRatio = () => {
		fetch(`./stampRatio.json`)
				.then(res => res.json())
				.then(res => stampRatio.set(res.currentRatio))
	}

	setContext('app_functions', {
		sendTransaction: (transaction, callback) => sendTransaction(transaction, callback),
		lwc: () => {
			return lwc
		},
		socket
	})

	const sendTransaction = (transaction, callback) => {
		let usersStamps = determineUsersTotalStamps()
		let contractName = transaction.contractName || config.masterContract
		let stampsToSendTx = transaction.stampLimit;
		if (!stampsToSendTx) stampsToSendTx = stampLimits[contractName][transaction.methodName]

		if (usersStamps < stampsToSendTx){
			createSnack({
                title: `Insufficient ${config.currencySymbol}`,
                body: `
					It will cost ${stringToFixed(toBigNumber(stampsToSendTx / $stampRatio), 4)} ${config.currencySymbol} to send this transaction.
					Please transfer more ${config.currencySymbol} to your Pixel Whale account using the Lamden Wallet.
                `,
                type: "error",
				delay: 7000
            })
		}else{
			transaction.stampLimit = stampsToSendTx
			lwc.sendTransaction(transaction, (txResult) => txResultsHandler.parseTxResult(txResult.data, callback))
		}
	}

	const determineUsersTotalStamps = () => {
		return parseInt($currency * $stampRatio)
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

	const refreshCurrencyBalance = async  () => {
		if ($tabHidden || !$userAccount) setTimeout(refreshCurrencyBalance, 10000)
		else{
			await refreshTAUBalance()
			lastCurrencyCheck = new Date()
			setTimeout(refreshCurrencyBalance, 10000)
		}
	}

	const refreshTauPrice = async  () => {
		if ($tabHidden || !$userAccount) setTimeout(refreshTauPrice, 60000)
		else{
			tauPrice.refreshPrice()
			setTimeout(refreshTauPrice, 60000)
		}
	}

	const setTabActive = () => {
		tabHidden.set(document.hidden)
		if (!$tabHidden && $userAccount && new Date() - lastCurrencyCheck > 5000 ) refreshTAUBalance()
		if (!$tabHidden && $userAccount && new Date() - tauPrice.lastCheck > 60000 ) tauPrice.refreshPrice()
	}
</script>

<style>
	main {
		position: relative;
		max-width: 1600px;
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
<AuctionUpdates />
