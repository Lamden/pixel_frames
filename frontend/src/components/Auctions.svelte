<script>
	import {onMount, getContext} from 'svelte'

	// Components
	import Auction from './Auction.svelte';

	// Misc
	import {
		decodeFrames,
		createSnack,
		formatAccountAddress, stringToFixed
	} from "../js/utils";
	import { config } from '../js/config.js'
	import { userAccount } from '../js/stores.js'

	export let auctions;
	export let title = true;
	export let preview = false;

    let count = auctions.count;
    let sending = false;

	let scrollHeight;
	let innerHeight;

	$: auctionData = [...auctions.data.map(a => {
		a.thingInfo.frames = decodeFrames(a.thingInfo.thing)
		return a
	})]
	$: elements = []
	$: lastElementTop = elements.length > 0 ? elements[elements.length -1] === null ? null : elements[elements.length -1].offsetTop : null
	$: lastElementOffsetHeight = elements.length > 0 ? elements[elements.length -1] === null ? null : elements[elements.length -1].offsetHeight: null
	$: visibleHeight = scrollHeight + innerHeight
	$: checker = checkGetMore(elements)

	const { socket } = getContext('app_functions')

	onMount(() => {
		console.log({auctions})
        socket.joinRoom('auction-updates')
		socket.on('new-auction', (auctionInfo) => {
			auctions = [auctionInfo, ...auctions]
		})
        socket.on('new-bid', (auctionUpdate) => {
			if (!auctions) return
			announceNewBid(replaceAuctionInfo(auctionUpdate.auction))
        })
		socket.on('auction-ended', (auctionUpdate) => {
			//replaceAuctionInfo(replaceAuctionInfo(auctionUpdate))
        })
        return () => socket.leaveRoom('auction-updates')
    })

	function replaceAuctionInfo (auctionUpdate) {
		let found
		auctionData.forEach((auction, index) => {
			if(auction.uid === auctionUpdate.uid) {
				let auctionDataBefore = JSON.parse(JSON.stringify(auctionData[index]))
				auctionData[index] = {...auctionData[index], ...auctionUpdate};
				found = auctionData[index]
				/*
				console.log({
					auctionUpdate,
					auctionDataBefore,
					auctionDataAfter: found
				})*/
			}
		});
		return found
	}

	const checkGetMore = () => {
    	if (lastElementTop === null || lastElementOffsetHeight === null) return
		if (visibleHeight > lastElementTop - (lastElementOffsetHeight * 4)) getMore()
	}

    const getMore = async () => {
		return

		if (preview) return

		if (count === auctionData.length) return
    	if (sending) return;
		sending = true;
		const res = await fetch(`./auctions.json?limit=25&offset=${auctionData.length}`).then(() => res.json())

		if (!res.data) return

		sending = false;

		if (res.count) count = res.count
		auctionData = [...auctionData, res.data]
	}

	const announceNewBid = (auctionInfo) => {
		let [currentBidInfo, previousBidInfo] = auctionInfo.bid_history
		if (!currentBidInfo) return

		let auctionIsYours = false

		//console.log({currentBidInfo, previousBidInfo, auctionIsYours})

		if ($userAccount){
			if ($userAccount === auctionInfo.old_owner) auctionIsYours = true
		}

		let message = `${formatAccountAddress(currentBidInfo.bidder, 8)} bid ${stringToFixed(currentBidInfo.bid, 4)} ${config.currencySymbol}${auctionIsYours ? " on your auction" : ""}.`

		if (!previousBidInfo){
			createSnack({
                title: `First Bid!`,
                body: message,
				type: auctionIsYours ? 'success' : 'info',
                delay: 10000,
				thingInfo: auctionInfo.thingInfo
            })
			return
		}

		let lastBidYours = previousBidInfo.bidder === $userAccount

		if (lastBidYours){
			createSnack({
                title: `You have been OUTBID!`,
                body: message,
				type: 'warning',
                delay: 10000,
				thingInfo: auctionInfo.thingInfo
            })
			return
		}

		createSnack({
			title: `New higher bid!`,
			body: message,
			type: auctionIsYours ? 'success' : 'info',
			delay: 10000,
			thingInfo: auctionInfo.thingInfo
		})
    }

</script>

<style>
	h2{
		border-top: 1px solid lightgray;
		padding-top: 1rem;
		margin-top: 2rem;
	}
	button, a{
		max-width: fit-content;
		padding: 10px 20px;
    	margin: 0 auto;
	}
	.owned{
        border: 2px dashed var(--primary);
    }
</style>

{#if title}
	<h2 class="text-color-primary-dark">NFTs Auctions!</h2>
{/if}

<div class="flex-row flex-wrap">
	{#each auctionData as auctionInfo, index}
		{#if auctionInfo.thingInfo}
			<Auction {auctionInfo} thingInfo={auctionInfo.thingInfo} id={auctionInfo.thingInfo.uid}/>
		{/if}
	{/each}
</div>


{#if preview}
	<a class="button" rel=prefetch href="{'auctions'}">SEE MORE</a>
{:else}
	<!--<button disabled={sending} class="button" on:click={getMore}> GET MORE </button>-->
{/if}

<svelte:window bind:scrollY={scrollHeight} bind:innerHeight={innerHeight} on:scroll={checkGetMore}/>