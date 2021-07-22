<script>
    import { getContext, onMount } from 'svelte'

    // Misc
    import { alreadyLiked } from '../js/utils.js'
    import { config } from '../js/config.js';
    import { userAccount } from '../js/stores.js'

    //Pictures
    import LikeFilledIcon from '../../static/img/like-filled.svg'
    import LikeUnfilledIcon from '../../static/img/like-unfilled.svg'

    const { sendTransaction } = getContext('app_functions')

    export let thingInfo;
    export let width = 20;

    let liked = null;

    $: height = width * 1.5

    onMount(() => {
        checkAlreadyLiked();
    })

    const checkAlreadyLiked = () => {
        alreadyLiked(thingInfo.uid)
        if (liked === null && $userAccount)  alreadyLiked(thingInfo.uid).then(res => liked = res)
    }


    const like = () => {
        if (liked || !$userAccount) return;

		const transaction = {
			methodName: 'like_thing',
			networkType: config.networkType,
			kwargs: {
				uid: thingInfo.uid
			}
		}

        sendTransaction(transaction, handleLikeTx)
    }

    const handleLikeTx = (txResults) => {
        console.log(txResults)
        if (txResults.txBlockResult.status === 0) {
            liked = true;
            thingInfo.likes = thingInfo.likes + 1;
            localStorage.setItem(`${thingInfo.uid}:${$userAccount}:liked`, true)
        }
    }

    userAccount.subscribe(account => checkAlreadyLiked())

</script>
<style>
    .flex-row{
        align-items: center;
        justify-content: space-between;
    }
    .icon {
        margin-right: 6px;
        position: relative;
        top: 3.5px;
    }
    .logged-in{
        cursor: pointer;
    }

</style>


<div class="flex-row flex-align-center likes">
    <div class="hide-mobile icon"
         class:logged-in={$userAccount}
         on:click={like}
         style={`width: ${width}px; height: ${height}px;`}>

        {#if liked !== null}
            {#if liked}
                <LikeFilledIcon width="21"/>
            {:else}
                <LikeUnfilledIcon width="21"/>
            {/if}
        {:else}
            <LikeUnfilledIcon width="21"/>
        {/if}
    </div>

    <div class="show-mobile icon">
        <LikeUnfilledIcon width="22" />
    </div>
    {thingInfo.likes}
</div>





