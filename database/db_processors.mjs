import { infoContractProcessor } from './processors/InfoContract.mjs'
import { masterContractProcessor } from './processors/MasterContract.mjs'
import { auctionContractProcessor } from './processors/AuctionContract.mjs'

export const getProcessors = (db, socket_server) => {
    const processors = {
        'InfoContractProcessor': infoContractProcessor(db, socket_server),
        'MasterContractProcessor': masterContractProcessor(db, socket_server),
        'AuctionContractProcessor': auctionContractProcessor(db, socket_server)
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