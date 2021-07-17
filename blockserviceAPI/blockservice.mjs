import axios from "axios";

export const getBlockService = (url, port) => {
    const fullURL = `${url}:${port}`

    async function getContractChanges(contractName, last_tx_uid, limit=10){
        let endpont = 'contract_history'
        let query = [
            `contract=${contractName}`,
            `last_tx_uid=${last_tx_uid}`,
            `limit=${limit}`
        ].join("&")
        let res = await axios(`${fullURL}/${endpont}?${query}`).then(res => res.data())
        //console.log(util.inspect(res.data, false, null, true))
        return res.data
    }

    async function getVariableChanges(contractName, variableName, last_tx_uid, limit=10){
        let endpont = 'variable_history'
        let query = [
            `contract=${contractName}`,
            `variable=${variableName}`,
            `last_tx_uid=${last_tx_uid}`,
            `limit=${limit}`
        ].join("&")
        let res = await axios(`${fullURL}/${endpont}?${query}`)
        //console.log(util.inspect(res.data, false, null, true))
        return res.data
    }

    async function getRootKeyChanges(contractName, variableName, root_key, last_tx_uid, limit=10){
        let endpont = 'rootkey_history'
        let query = [
            `contract=${contractName}`,
            `variable=${variableName}`,
            `root_key=${root_key}`,
            `last_tx_uid=${last_tx_uid}`,
            `limit=${limit}`
        ].join("&")
        let res = await axios(`${fullURL}/${endpont}?${query}`)
        //console.log(util.inspect(res.data, false, null, true))
        return res.data
    }

    return{
        getContractChanges,
        getVariableChanges,
        getRootKeyChanges
    }
}