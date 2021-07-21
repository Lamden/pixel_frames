import axios from "axios";
import util from "util";

export const getBlockService = (url, port) => {
    const fullURL = `${url}:${port}`

    async function getCurrentKeyValue(contractName, variableName, key){
        try{
            let endpont = 'current/one'
            let res = await axios(`${fullURL}/${endpont}/${contractName}/${variableName}/${key}`)
            return res.data
        }catch(e){
            return e
        }
    }

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
        getRootKeyChanges,
        getCurrentKeyValue
    }
}