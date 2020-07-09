<script>
	import { userAccount, txResults } from '../js/stores'
	import { beforeUpdate } from 'svelte'
	import { goto } from '@sapper/app';

	import Title from './Title.svelte'

	export let segment;

	let tauAmount = 0;

	beforeUpdate(() => {
		if ($userAccount) refreshTAUBalance()
	})

	const refreshTAUBalance = async () => {
		return
		const res = await fetch("http://167.172.126.5:18080/contracts/currency/balances?key=" + $userAccount)
		const data = await res.json();
		if (!data.value) tauAmount = 0
		else tauAmount = data.value;
	}

	const updateTau = (data) => {
		if (typeof data.txBlockResult.status !== 'undefined'){
			if (data.txBlockResult.status == 0) {
				if (status === 0) refreshTAUBalance();
			}
		}
	}

	txResults.subscribe(results => {
		if (results.data) updateTau(results.data)
	})

	const logout = () => {
		userAccount.set("")
		goto(`.`);
	}
</script>

<style>
	nav {
		position: fixed;
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
	.brand{
		align-items: center;
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
		font-size: 1em;
		line-height: 1.2;
		text-align: right;
		flex-grow: 1;
		min-width: 20%
	}
	.account >  p > strong {
		font-size: 1em;
	}
	.address{
		width: 93%;
		font-size: 0.9em;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		align-self: flex-end;
		margin: 0;
	}
	.dtau{
		color: #161454;
		font-size: 0.8em;
		margin: 0;
	}
	.button_text {
		padding: 0;
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
		background-color: #ff5bb0;
		display: block;
		bottom: -1px;
	}
	li > a {
		text-decoration: none;
		padding: 1em 0.5em;
		display: block;
	}

	@media (min-width: 900px) {
		.links {
			display: block;
		}
	}

</style>

<nav class="flex-row">
	<div class="brand flex-row" on:click={logout}>
		<img src="logo-64.png" alt="nav logo">
		<Title fontSize={1}/>
	</div>
	<div class="links">
		<ul>
			{#if segment !== undefined && $userAccount !== ""}
				<li><a rel=prefetch aria-current="{segment === 'boards' ? 'page' : undefined}" href={'boards/' + $userAccount}>create</a></li>
			{/if}
			{#if $userAccount !== ""}
				<li><a rel=prefetch aria-current="{segment === 'owned' ? 'page' : undefined}" href={'owned/' + $userAccount}>owned</a></li>
			{/if}
			<li><a rel=prefetch aria-current="{segment === 'recent' ? 'page' : undefined}" href="recent">recent</a></li>
			<li><a rel=prefetch aria-current="{segment === 'forsale' ? 'page' : undefined}" href="forsale">for sale</a></li>
		</ul>
	</div>
	<div class="flex-col account">
		{#if $userAccount !== ""}
			<a href={`https://explorer.lamden.io/address/${$userAccount}`}
			   target="_blank"
			   rel="noopener noreferrer"
			   class="address">
				{$userAccount}
			</a>
			<p class="dtau"><strong>dTAU: </strong> {tauAmount}</p>
			<button class="button_text" on:click={logout}>sign out </button>
		{/if}
	</div>
</nav>
