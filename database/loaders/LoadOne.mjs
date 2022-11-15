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

    async function processUpdate(update){
        const { state_changes_obj } = update
        console.log(util.inspect({state_changes_obj}, false, null, true))
        let contractUpdate = state_changes_obj[INFO_CONTRACT]["S"]

        let names_uid_state_change = contractUpdate.find(s => s.key.includes(`${INFO_CONTRACT}.S:names:`)).key
        console.log(util.inspect({names_uid_state_change}, false, null, true))
        const uid =  names_uid_state_change.split(":")[2]

        let updateType = processor.determineUpdateType(uid)

        if (updateType === "createNewThing") {
            console.log(`NEW THING DETECTED! UID: ${uid}`)

        }
    }

    async function load(tx_hash){
        let update = await getUpdate(tx_hash)
        console.log(util.inspect({update}, false, null, true))
        await processUpdate(update)
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
