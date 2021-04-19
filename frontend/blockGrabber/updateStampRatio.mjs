import fetch from 'node-fetch'

export const update_stamp_ratio = (models, blockexplorer_url) => {
    const updateStampRatio = async  () => {
		fetch(`${blockexplorer_url}/api/lamden/stamps`)
				.then(res => res.json())
				.then(async (res) => {
				    if (!res || !res.value){
                        checkAgain()
                        return
                    }
				    let stampRatio = await models.StampRatio.findOne({symbol: 'TAU'})

                    if (!stampRatio){
                        stampRatio = await new models.StampRatio({
                            symbol: 'TAU',
                        })
                    }

                    stampRatio.currentRatio = parseInt(res.value)
                    stampRatio.lastUpdated = new Date()

                    await stampRatio.save()
                    checkAgain()
                })
                .catch(() => checkAgain());
    }

    const checkAgain = () => setTimeout(updateStampRatio, 3600000)
    return { updateStampRatio }
}

