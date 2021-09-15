import { infoContractProcessor } from './processors/InfoContract.mjs'
import { masterContractProcessor } from './processors/MasterContract.mjs'
import { auctionContractProcessor } from './processors/AuctionContract.mjs'

import { TwitterClient } from 'twitter-api-client';

const { TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET } = process.env

let services = {}

if (TWITTER_API_KEY && TWITTER_API_SECRET && TWITTER_ACCESS_TOKEN && TWITTER_ACCESS_TOKEN_SECRET){
    const twitterClient = new TwitterClient({
      apiKey: process.env.TWITTER_API_KEY,
      apiSecret: process.env.TWITTER_API_SECRET,
      accessToken: process.env.TWITTER_ACCESS_TOKEN,
      accessTokenSecret: process.env.TWITTER_ACCESS_TOKEN_SECRET,
    });
    services.twitterClient = twitterClient
}


export const getProcessors = (db, socket_server) => {
    const processors = {
        'InfoContractProcessor': infoContractProcessor(db, socket_server, services),
        'MasterContractProcessor': masterContractProcessor(db, socket_server, services),
        'AuctionContractProcessor': auctionContractProcessor(db, socket_server, services)
    }
    const runner = {}

    function setupProcessors (setupList){
        setupList.map(setup => {
            const [contractName, processorName] = setup
            if (typeof runner[contractName] !== 'undefined') throw new Error(`${contractName} already has a processor`)
            runner[contractName] = processors[processorName]
        })
    }
    return {
        setupProcessors,
        run: (contractName, update) => runner[contractName].processUpdate(update, false)
    }
}