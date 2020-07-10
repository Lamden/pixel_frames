<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params }) {
		let env = process.env.NODE_ENV
		const options = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				contractName: 'con_pf_test',
				variableName: 'S'
			})
		}
		const res = await this.fetch(`${config.blockExplorer[env]}/things/owned/${params.account}`, options)
		let data = await res.json()
		if (!data) data = []
	    return {account: params.account, owned: data}
	}
</script>

<script>
	import { beforeUpdate } from 'svelte'
    import Designer from "../../components/Designer.svelte";

    import { userAccount } from '../../js/stores'

    export let account
	export let owned

	beforeUpdate(() => {
		userAccount.set(account)
	})

</script>

<Designer {account}/>


