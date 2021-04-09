<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params, query }) {
		let things = await this.fetch(`./owned/${params.account}.json?limit=25`).then(res => res.json())

	    return {
			account: params.account,
			owned: things
		}
	}
</script>

<script>
    import Owned from "../../components/Owned.svelte";

    import { formatAccountAddress } from '../../js/utils'

    export let account
	export let owned

</script>

<svelte:head>
	<title>{`Pixel Frames owned by ${formatAccountAddress(account)}`}</title>
</svelte:head>

<Owned owned={owned} {account}/>


