import * as InfoContractLoader from './loaders/InfoContractLoader.mjs'
import * as AuctionContractLoader from './loaders/AuctionContractLoader.mjs'

const runLoader = async (loaderList, drop, starting_tx_uid) => {
    console.log({loaderList, drop, starting_tx_uid})
    const loaders = {
        InfoContractLoader,
        AuctionContractLoader,
        LoadOne
    }

    // Validate Args
    const availableLoaders = Object.keys(loaders)

    if (loaderList === "all"){
        loaderList = availableLoaders
    }else{
        try{
            loaderList = loaderList.split(":")
        }catch (e){
            throw new Error(`No Loader name provided. Loaders available are ${availableLoaders.join(", ")}`)
        }
    }

    if (loaderList.length === 0) {
        throw new Error(`No Loader name provided. Loaders available are ${availableLoaders.join(", ")}`)
    }

    for (const loaderName of loaderList){
        if (!Object.keys(loaders).includes(loaderName)) {
            throw new Error(`Loader doesn't exists. Loaders available are: ${availableLoaders.join(", ")}`)
        }
    }

    // Drop Collections
    if (drop) {
        for (const loaderName of loaderList){
            await loaders[loaderName].drop_collections()
        }
    }

    // Load Collections
    for (const loaderName of loaderList){
        console.log(`Running ${loaderName}...`)
        let loader =  loaders[loaderName].loadCollection(starting_tx_uid)
        await loader.finished
        console.log(`Finished Running ${loaderName}...`)
    }

    process.exit(0)
}

let [loaderList, drop, starting_tx_uid] = process.argv.slice(2)

if (drop === "drop") drop = true
else drop = false

runLoader(loaderList, drop, starting_tx_uid)
