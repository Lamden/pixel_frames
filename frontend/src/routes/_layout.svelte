<!-- /frontend/src/routes/_layout.svelte -->

<script>
	import Nav from '../components/Nav.svelte';
	import { onMount, setContext } from 'svelte'
	import WalletController from 'lamden_wallet_controller';
	import { walletInstalled, walletInfo, txResults } from '../js/stores'
	import { approvalRequest } from '../js/wallet_approval'

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
		sendTransaction: (transaction) => lwc.sendTransaction(transaction)
	})

	const handleWalletInfo = (info) => {
		console.log(info)
		if (info.errors){
			if (info.errors[0].includes('lamdenWalletConnect')) lwc.sendConnection(approvalRequest)
			else alert(JSON.stringify(info.errors[0]))
		}else{
			walletInfo.set(info)
		}
	}

	const handleTxResults = (results) => txResults.set(results)
</script>

<style>
	main {
		position: relative;
		max-width: 95em;
		padding: 2rem 28px 0;
		margin: 0 auto;
		margin-top: 100px;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
</style>

<Nav {segment}/>
<main>
	<slot></slot>
</main>
