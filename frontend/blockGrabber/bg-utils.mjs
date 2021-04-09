import { validateTypes } from 'types-validate-assert'
import { getDbUtils } from './db_utils.mjs'

export const getUtils = (config) => {
    const { INFO_CONTRACT, MASTER_CONTRACT } = config

    const isLamdenKey = ( key ) => {
        if (validateTypes.isStringHex(key) && key.length === 64) return true;
        return false;
    }

    const isPixelFramesContract =  (contractName) => {
        //console.log({contractName, MASTER_CONTRACT})

        return contractName === MASTER_CONTRACT
    }

    return {
        isLamdenKey,
        isPixelFramesContract,
        ...getDbUtils(config)
    }
}