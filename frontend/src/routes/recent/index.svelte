<script context="module">
	export async function preload(parms) {
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
		const res = await this.fetch(`http://localhost:1337/things/recent`, options)
		let data = await res.json()
		if (!data) data = []
	    return {recent: data}
	}
</script>

<script>
    import Recent from '../../components/Recent.svelte'

    export let recent;
</script>

<Recent {recent}/>