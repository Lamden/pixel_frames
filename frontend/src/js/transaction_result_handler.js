import {createSnack} from "./utils";

export const TransactionResultHandler = (createSnack) => {

	function parseTxResult(txResults, callback = undefined) {
		console.log(txResults)
		if (txResults.errors) {
			parseTxErrors(txResults.errors)
            return
		}
		if (txResults?.txBlockResult?.errors?.length > 0) {
			let errors = txResults?.txBlockResult?.errors
			parseTxErrors(errors)
            return
		}
		if (txResults.resultInfo.title === "Transaction Pending"){
			return
		}
		if (typeof txResults.txBlockResult.status !== 'undefined') {
			if (txResults.txBlockResult.status === 0) {
			    callback(txResults)
			}
			if (txResults.txBlockResult.status === 1) {
				parseTxErrors(txResults.txBlockResult.errors)
			}
		}
	}
	function parseTxErrors(errors){
		if (Array.isArray(errors)){
			errors.forEach(error => {
				let toastType = 'info'
				if (error.includes("AssertionError('")) {
					let match = error.match(/AssertionError\('(.*)',\)/)
					if (match){
						error = match[1]
						toastType = 'error'
					}else return
				}
				createSnack({
                    title: 'Transaction Error',
                    body: error,
                    type: toastType === 'info' ? 'info' : 'error'
			    })
			})
		}else{
			if (typeof errors === 'string'){
                createSnack({
                    title: 'Transaction Error',
                    body: errors,
                    type: 'error'
			    })
			}else{
                createSnack({
                    title: 'Unknown Transaction Error',
                    body: 'Something happened and we couldn\'t get the status of your transaction.',
                    type: 'error'
			    })
			}
		}
	}
	return {
	    parseTxResult
	}
}



