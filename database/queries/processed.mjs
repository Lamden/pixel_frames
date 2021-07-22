import util from "util";

export const getProcessedQueries = (db) => {
    async function update_processed(loaderType, last_tx_uid){
        await db.models.Processed.updateOne({loaderType}, {
            loaderType,
            last_tx_uid_processed: last_tx_uid
        }, {upsert:true})
    }

    async function shouldProcess(loaderType, last_tx_uid){
        let last_tx_uid_processed = "0"
        let processedInfo = await db.models.Processed.findOne({loaderType})
        if (processedInfo) last_tx_uid_processed = processedInfo.last_tx_uid_processed
        return last_tx_uid > last_tx_uid_processed
    }

    async function delete_processed(loaderType){
        let res = await db.models.Processed.deleteMany({loaderType})
        console.log(`Processing History for ${loaderType} deleted: ${util.inspect(res, false, null, true)}`);
    }

    return {
        update_processed,
        shouldProcess,
        delete_processed
    }
}