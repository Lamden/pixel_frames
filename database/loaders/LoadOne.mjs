import {config} from 'dotenv'
config({
    path: '../../frontend/.env'
})
import util from "util";

const INFO_CONTRACT = process.env.INFO_CONTRACT || null
if (!INFO_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")
const BLOCKSERVICE_URL = process.env.BLOCKSERVICE_URL || 'http://localhost'
const BLOCKSERVICE_PORT = process.env.BLOCKSERVICE_PORT || 3535

import { getDatabase} from "../database.mjs"
import { getBlockService } from "../../blockserviceAPI/blockservice.mjs"
import { infoContractProcessor } from "../processors/InfoContract.mjs"


export async function drop_collections(){
    let db = await getDatabase()
}

export const loadCollection = (tx_hash) => {
    const blockService = getBlockService(BLOCKSERVICE_URL, BLOCKSERVICE_PORT)
    const processor = infoContractProcessor()

    let db
    let done

    async function getUpdate(tx_hash){
        return await blockService.getTx(tx_hash)
    }

    async function processUpdate(transactionInfo){
        const { state_changes_obj, txInfo } = transactionInfo
        //console.log(util.inspect({state_changes_obj}, false, null, true))

        const contractUpdate = state_changes_obj[INFO_CONTRACT]["S"]
        const name_key = Object.keys(contractUpdate['names'])[0]
        const uid =  contractUpdate['names'][name_key]
        const update = contractUpdate[uid]
        const names = contractUpdate['names']

        let updateType = processor.determineUpdateType(update)

        if (updateType === "createNewThing") {
            const args =  {
                uid,
                update,
                names,
                transactionInfo: txInfo,
                blockNum: transactionInfo['blockNum'],
                loader: true
            }
            await processor.createNewThing(args)
        }
    }

    async function load(tx_hash){
        let transactionInfo = await getUpdate(tx_hash)
        console.log(util.inspect({transactionInfo}, false, null, true))
        await processUpdate(transactionInfo)
        done()
    }

    async function startLoading(resolver) {
        db = await getDatabase()
        processor.setDb(db)

        load(tx_hash)

        done = resolver
    }

    const finished = new Promise(startLoading)

    return {
        finished
    }
}
