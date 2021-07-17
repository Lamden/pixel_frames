import util from "util";

export const getMiscQueries = (db) => {
    async function drop_collection(collectionName){
        try{
            let res = await db.models[collectionName].deleteMany({})
            console.log(`${collectionName} DB wiped: ${util.inspect(res, false, null, true)}`);
        }catch(e){
            console.log(e)
        }
    }

    async function drop_collections(collections){
        for (const collectionName of collections){
            await drop_collection(collectionName)
        }
    }

    return {
        drop_collection,
        drop_collections
    }
}