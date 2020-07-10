<script context="module">
	import { config } from '../../js/config.js'
	export async function preload({ params, query }) {
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
	import { beforeUpdate, onMount } from 'svelte'
	import { userAccount } from '../../js/stores'
    import Owned from "../../components/Owned.svelte";

    export let account
	export let owned

	const thing = {
    	uid: "09777890871012081029371927389237412093812",
    	likes: 10,
		price: 100,
		owner: "69f445839163c7adef2baac101f8e34e07f9397e0d8cbc6197a1477b2d6853f2",
		description: "The Letter J getting colorized. I made this to do something like this and this is supposed to be a really long description."
	}

	onMount(() => {
		/*
		let things = []
		things[0] = {...thing, "thing": localStorage.getItem('thing_string')}
		owned = things
		*/

	})

	beforeUpdate(() => {
		userAccount.set(account)
	})

</script>

<Owned {owned}/>


