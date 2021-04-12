<script>
	import { walletInstalled, userAccount, currency, approvalAmount, stampRatio, autoTx, walletInfo } from '../js/stores'
	import { beforeUpdate, onMount } from 'svelte'
	import { goto } from '@sapper/app';

	import { refreshTAUBalance, checkForApproval, formatAccountAddress, stringToFixed } from '../js/utils.js'
	import { config } from '../js/config'

	import Title from './Title.svelte'
	import WalletConnectButton from './WalletConnectButton.svelte'

	export let segment;
	export let lwc;

	let initalize = false;
	let balance;
	let timer;
	setTimeout(() => initalize = true, 500)

	$: lwcInitialized = false;

	onMount(() => {
		timer = setTimeout(() => {
			if ($userAccount && !balance) {
				balance = refreshTAUBalance()
				checkForApproval()
				timer = null;
			}
		}, 1000)
	})


	beforeUpdate(() => {
		if (!lwc) {
			balance = undefined
			lwcInitialized = false;
		}
		if (lwc && !lwcInitialized) lwcInitialized = true;
	})

</script>

<style>
	nav {
		position: relative;
    	top: 0;
		left: 0;
		height: 92px;
		box-sizing: border-box;
    	width: 100%;
		padding: 1rem 3em;
		display: flex;
		flex-direction: row;
		align-items: center;
		background: white;
		border-bottom: 1px solid #ff5bb047;
		z-index: 1;
	}
	nav.flex-row{
		justify-content: center;
	}
	.desktop{
		display: none;
	}
	.brand{
		align-items: center;
		justify-content: center;
		font-weight: 300;
		font-size: 2em;
		min-width: max-content;
		cursor: pointer;
	}
	.brand > img {
		width: 37px;
		min-width: 37px;
		margin-right: 8px;
	}
	.account{
		color: #161454;
		height: 100%;
		align-items: flex-end;
		justify-content: space-evenly;
		font-weight: 200;
		font-size: 0.9em;
		line-height: 1.2;
		text-align: right;
		flex-grow: 1;
		min-width: 20%
	}
	.currency > strong {
		margin-left: 4px;
	}

	.account >  p > strong.account-info{
		color: var(--primary);
		font-weight: 400;
	}
	.address{
		width: 93%;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		align-self: flex-end;
		margin: 0;
		color: var(--primary);
	}
	.address:hover{
		color: var(--primary)
	}
	.currency{
		color: #161454;
		font-size: 1em;
		margin: 0;
	}

	.links{
		display: none;
		padding: 0 20px;
		min-width: max-content;
	}
	ul {
		margin: 0;
		padding: 0;
	}
	/* clearfix */
	ul::after {
		content: '';
		display: block;
		clear: both;
	}
	li {
		display: block;
		float: left;
	}
	[aria-current] {
		position: relative;
		display: inline-block;
	}
	[aria-current]::after {
		position: absolute;
		content: '';
		width: calc(100% - 1em);
		height: 2px;
		background-color: var(--primary);
		display: block;
		bottom: -1px;
	}
	li > a {
		text-decoration: none;
		padding: 1em 0.5em;
		display: block;
	}
	li > a:hover{
		color: var(--primary);
	}

	@media (min-width: 900px) {
		.links {
			display: block;
		}
	}
	@media (min-width: 450px) {
		.desktop {
			display: flex;
		}
		nav.flex-row{
			justify-content: unset;
		}
	}
	a.brand{
		text-decoration: none;
	}

</style>

<nav class="flex-row">
	<a class="brand flex-row" rel=prefetch  href=".">
		<img src="logo-64.png" alt="nav logo">
		<Title fontSize={1} subtitle={false}/>
	</a>
	<div class="links desktop">
		<ul>
			<li><a rel=prefetch aria-current="{segment === 'create' ? 'page' : undefined}" href="create">create</a></li>
			{#if $userAccount !== ""}
				<li><a rel=prefetch aria-current="{segment === 'owned' ? 'page' : undefined}" href={'owned/' + $userAccount}>owned</a></li>
			{/if}
			<li><a rel=prefetch aria-current="{segment === 'recent' ? 'page' : undefined}" href="recent">recent</a></li>
			<li><a rel=prefetch aria-current="{segment === 'forsale' ? 'page' : undefined}" href="forsale">for sale</a></li>
			<!--<li><a href="https://docs.pixelwhale.io">docs</a></li>-->
		</ul>
	</div>
	<div class="flex-col account desktop hide-mobile">
		{#if $userAccount !== "" && initalize && !$walletInfo.locked}
			<p class="currency">
				{stringToFixed($currency, 8)}<strong>{config.currencySymbol}</strong>
			</p>
			<a href={`${config.blockExplorer}/addresses/${$userAccount}`}
			   target="_blank"
			   rel="noopener noreferrer"
			   class="address">
				{`${formatAccountAddress($userAccount, 8, 4)}`}
			</a>
		{:else}
			{#if lwcInitialized && initalize}
				<WalletConnectButton {lwc} />
			{/if}
		{/if}

	</div>
</nav>
