<script>
    import { txResults } from '../js/stores'

    let txResultMessage = ""

    const processTxResults = (data) => {
		if (typeof data.txBlockResult.status !== 'undefined'){
			if (data.txBlockResult.status == 0) {
				txResultMessage = "Thing Created!";
			}else{
				txResultMessage = "There was a problem sending your transaction :(";
			}
            //txResults.set({})
            setTimeout(() => {
                txResultMessage = ""
            }, 2000)
		}
	}

    txResults.subscribe(results => {
    	console.log(results)
		if (results.data) {
			if (results.data.txBlockResult) processTxResults(results.data)
		}
	})

</script>


<p>{txResultMessage}</p>