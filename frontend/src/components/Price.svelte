<script>
    import { userAccount } from '../js/stores.js'
    import { getContext } from 'svelte'
    import { serializeFrames } from '../js/utils'
    import { frames, frameSpeed } from '../js/stores'

    import lamden_logo from '../../static/img/lamden_logo_new.svg'

    export let thingInfo

    const { sendTransaction } = getContext('app_functions')


    const sell = () => {
        const thing_string = serializeFrames($frames, $frameSpeed)
		console.log(thing_string)
		console.log(thing_string.length)
		localStorage.setItem('frames', JSON.stringify($frames))
		localStorage.setItem('thing_string', thing_string)

		const transaction = {
			methodName: 'create_thing',
			networkType: 'testnet',
			stampLimit: 1000000,
			kwargs: {
				thing_string,
				description: "A test string"
			}
		}
		//sendTransaction(transaction)
    }

</script>

{#if thingInfo.price > 0}
    <div class="flex-row price">
        <div class="icon">
            {@html lamden_logo}
        </div>
        {thingInfo.price}
        {#if thingInfo.owner !== $userAccount}
            <a class="button_text" href={"buy/" + thingInfo.uid} >buy</a>
        {:else}
            <a class="button_text" href={"buy/" + thingInfo.uid} >set</a>
        {/if}
    </div>
{:else}
    <a class="button_text" href={"buy/" + thingInfo.uid} >sell</a>
{/if}