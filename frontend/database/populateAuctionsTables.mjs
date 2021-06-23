import { config } from 'dotenv'
config()

import { getDatabase, mongoose_models } from "./database.mjs";
import { getDbUtils } from "../blockGrabber/db_utils.mjs";

const { AUCTION_CONTRACT, INFO_CONTRACT, MASTER_CONTRACT, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, PUSHBULLET_TOKEN } = process.env

if (!INFO_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")
if (!MASTER_CONTRACT ) throw Error("Must pass MASTER_CONTRACT via .env file")

let DB_CONFIG = {
    INFO_CONTRACT,
    MASTER_CONTRACT,
    AUCTION_CONTRACT,
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    PUSHBULLET_TOKEN,
    models: mongoose_models
}

const populateAuctionsTables = () => {
    const auctionTables = ['CurrentAuctions', 'AuctionHistory']

    const wipeTables = (models) => {
        auctionTables.forEach(table => {
            models[table].deleteMany({}).then((res) => {
				console.log(`${table} DB wiped`);
				console.log(res)
            });
        })
    }

    const process = async () => {
        await getDatabase()
        let models = mongoose_models
        let dbUitls = getDbUtils(DB_CONFIG)

        wipeTables(models)

        let all_blocks = await models.Blocks.aggregate([
            { $match: {} },
            { $sort: { blockNum: 1 } }
        ]).allowDiskUse(true)

        let last_block_processed = 0
        let number_of_blocks_processed = 0
        for (let i = 0; i < all_blocks.length; i++){
            let blockInfo = JSON.parse(all_blocks[i].rawBlock)
            await dbUitls.process_auction_block(blockInfo)
            last_block_processed = blockInfo.number
            number_of_blocks_processed = number_of_blocks_processed + 1
        }
        console.log({
            number_of_blocks: all_blocks.length,
            last_block_processed,
            number_of_blocks_processed
        })
    }

    return { process }
}

let start = populateAuctionsTables()
start.process().then(() => process.exit(1))