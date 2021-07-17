import {config} from 'dotenv'
config()
import io_client from "socket.io-client"
import util from 'util'

import { getDatabase} from "./database.mjs"
import { update_tau_price } from './price-updater.mjs'
import { update_stamp_ratio } from './updateStampRatio.mjs'
import { getProcessors } from "./db_processors.mjs";
import * as SocketServer from './services/socketserver.mjs'

const MASTERNODE_URLS = {
    'testnet': "https://testnet-master-1.lamden.io",
    'mainnet' : "https://masternode-01.lamden.io"
}

const BLOCKEXPLORER_URLS = {
    'testnet': "https://testnet.lamden.io",
    'mainnet' : "https://mainnet.lamden.io"
}

/******* BLOCKSERVICE CONNECTION INFO **/
const BLOCKSERVICE_URL = process.env.BLOCKSERVICE_URL || 'http://localhost'
const BLOCKSERVICE_PORT = process.env.BLOCKSERVICE_PORT || 3535

/******* SOCKET_SERVER CONNECTION INFO **/
const DATABASE_SERVICE = process.env.DATABASE_SERVICE || 3536

/******* MONGO DB CONNECTION INFO **/
const NETWORK = process.env.NETWORK || 'testnet'
const MASTERNODE_URL = process.env.MASTERNODE_URL || MASTERNODE_URLS[NETWORK]
const BLOCKEXPLORER_URL = process.env.BLOCKEXPLORER_URL || BLOCKEXPLORER_URLS[NETWORK]
const INFO_CONTRACT = process.env.INFO_CONTRACT || null
const MASTER_CONTRACT = process.env.MASTER_CONTRACT || null
const AUCTION_CONTRACT = process.env.AUCTION_CONTRACT || null

if (!INFO_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")
if (!MASTER_CONTRACT ) throw Error("Must pass MASTER_CONTRACT via .env file")
if (!AUCTION_CONTRACT ) throw Error("Must pass AUCTION_CONTRACT via .env file")

const { TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, PUSHBULLET_TOKEN } = process.env

const start = async () => {
    const db = await getDatabase()

    let socket_server = SocketServer.start(DATABASE_SERVICE, db)
    let socket_client = io_client(`${BLOCKSERVICE_URL}:${BLOCKSERVICE_PORT}`);

    const processor = getProcessors(db, socket_server)

    processor.setupProcessors([
        [INFO_CONTRACT, 'InfoContractProcessor'],
        [MASTER_CONTRACT, 'MasterContractProcessor'],
        [AUCTION_CONTRACT, 'AuctionContractProcessor']
    ])

    let tauUpdater = update_tau_price(db.models)
    let stampRatioUpdater = update_stamp_ratio(db.models, BLOCKEXPLORER_URL)

    tauUpdater.updatePrice()
    stampRatioUpdater.updateStampRatio()

    socket_client.on('connect', () => {
        console.log("CONNECTED TO BLOCKSERVICE")

        socket_client.emit('join', INFO_CONTRACT);
        socket_client.emit('join', MASTER_CONTRACT);
        socket_client.emit('join', AUCTION_CONTRACT);
    })

    socket_client.on('new-state-changes-by-transaction', (data) => {
        console.log(util.inspect({socket: 'new-state-changes-by-transaction', data}, false, null, true))
        processor.run(data.room, data.message)
    })
}

start()