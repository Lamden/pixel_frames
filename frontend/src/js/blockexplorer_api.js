import { config } from './config'

export const blockexplorer_api = (() => {
    let url = config.blockExplorer + '/api'

    async function getKeys (keyList){
        let options = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(keyList)
        }

        const data = await fetch(`${url}/states/history/getKeys`, options)
            .then(res => res.json())
            .catch(err => console.log(err))
        let keysObj = {}
        data.map(kvPair => {
            try{
                keysObj[kvPair.key] = kvPair.value.__fixed__
            }catch (e) {
                keysObj[kvPair.key] = kvPair.value
            }
        })
        return keysObj
    }

    return {
        getKeys
    }
})()