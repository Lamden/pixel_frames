import {config} from 'dotenv'
config()
import { getDatabase, mongoose_models} from "../database/database.mjs";
import { runBlockGrabber } from './blockgrabber.mjs'
import {getUtils} from './bg-utils.mjs'

const MASTERNODE_URLS = {
    'testnet': "https://testnet-master-1.lamden.io",
    'mainnet' : "https://masternode-01.lamden.io"
}

/******* MONGO DB CONNECTION INFO **/
const DEBUG_ON = process.env.DEBUG_ON  || false
const NETWORK = process.env.NETWORK || 'testnet'
const START_AT_BLOCK_NUMBER = parseInt(process.env.START_AT_BLOCK_NUMBER) || 0
const RE_PARSE_BLOCKS = process.env.RE_PARSE_BLOCKS || false
const WIPE = process.env.WIPE || false
const MASTERNODE_URL = process.env.MASTERNODE_URL || MASTERNODE_URLS[NETWORK]
const INFO_CONTRACT = process.env.INFO_CONTRACT || null
const MASTER_CONTRACT = process.env.MASTER_CONTRACT || null

if (!INFO_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")
if (!MASTER_CONTRACT ) throw Error("Must pass MASTER_CONTRACT via .env file")

let grabberConfig = {
    DEBUG_ON, START_AT_BLOCK_NUMBER, MASTERNODE_URL, WIPE, RE_PARSE_BLOCKS, INFO_CONTRACT, MASTER_CONTRACT
}
grabberConfig.models = mongoose_models
grabberConfig.utils = getUtils(grabberConfig)

const start = async () => {
    grabberConfig.db = await getDatabase()
    let blockGrabber = runBlockGrabber(grabberConfig)
    let nextCheck = 15000
    var timer = setInterval(async () => {
        console.log(blockGrabber.lastCheckedTime())
        console.log(new Date() - blockGrabber.lastCheckedTime())
        if ((new Date() - blockGrabber.lastCheckedTime()) > 30000) {
            console.log('restarting blockgrabber')
            if (grabberConfig.WIPE === 'yes') grabberConfig.WIPE = undefined
            if (grabberConfig.RE_PARSE_BLOCKS === 'yes') grabberConfig.RE_PARSE_BLOCKS = undefined
            blockGrabber.stop()
            blockGrabber = runBlockGrabber(grabberConfig)
            nextCheck = 30000
        }else{
            nextCheck = 15000
        }
    }, nextCheck)
}

start()