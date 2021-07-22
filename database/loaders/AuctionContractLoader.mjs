import {config} from 'dotenv'
config({
    path: '../../frontend/.env'
})

import { getDatabase} from "../database.mjs"
import { getBlockService } from "../../blockserviceAPI/blockservice.mjs"
import { auctionContractProcessor } from "../processors/AuctionContract.mjs"
import util from "util";

const AUCTION_CONTRACT = process.env.AUCTION_CONTRACT || null
if (!AUCTION_CONTRACT ) throw Error("Must pass AUCTION_CONTRACT via .env file")

const BLOCKSERVICE_URL = process.env.BLOCKSERVICE_URL || 'http://localhost'
const BLOCKSERVICE_PORT = process.env.BLOCKSERVICE_PORT || 3535


export async function drop_collections(){
    let db = await getDatabase()
    await db.queries.drop_collection('AuctionHistory')
    await db.queries.delete_processed('AuctionHistoryContract')
}

export const loadCollection = (starting_tx_uid = "000000000000.00000.00000", drop=false) => {
    const blockService = getBlockService(BLOCKSERVICE_URL, BLOCKSERVICE_PORT)
    const processor = auctionContractProcessor()

    let db
    let done

    async function getUpdates(last_tx_uid){
        return await blockService.getVariableChanges(AUCTION_CONTRACT, "S", last_tx_uid, 1)
    }

    async function processUpdates(updates){
        let last_tx_uid
        for (const update of updates){
            last_tx_uid = update.tx_uid
            await processor.processUpdate(update, true)
        }
        load(last_tx_uid)
    }

    async function load(last_tx_uid){
        let updates = await getUpdates(last_tx_uid)
        if (updates.history.length > 0) await processUpdates(updates.history)
        else done()
    }

    async function startLoading(resolver) {
        db = await getDatabase()
        processor.setDb(db)

        done = resolver
        load(starting_tx_uid)
    }

    const finished = new Promise(startLoading)

    return {
        finished
    }
}
