import { decodeFrames } from "../pixelwhale_utils.mjs";

export const getPixelWhaleQueries = (db) => {
    async function drop_table(){
        db.models.PixelFrame.deleteMany({}).then((res) => {
            console.log(`PixelFrame DB wiped`);
            console.log(res)
        });
    }

    async function populateThingInfo(uidList){
        return await Promise.all(uidList.map(async (info) => {
            let thingInfo = await db.models.PixelFrame.findOne({uid: info.uid})
            if (info._doc) return {...info._doc, thingInfo}
            else return {...info, thingInfo}
        }))
    }

    return {
        drop_table,
        populateThingInfo
    }
}