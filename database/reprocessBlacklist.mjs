import fs from "fs";
import { getDatabase, mongoose_models} from "./database.mjs";

const updateBlacklist = () => {
    const process = async () => {
        let db = await getDatabase()
        let models = mongoose_models

        let allThings = await models.PixelFrame.find({})
        let blacklist = JSON.parse(fs.readFileSync('../blockGrabber/blacklist.json', 'utf8'));

        await Promise.all(allThings.map(async thing => {
            if (blacklist.art.includes(thing.uid) || blacklist.creators.includes(thing.creator)){
                if (!thing.blacklist) await models.PixelFrame.updateOne({uid: thing.uid}, {blacklist: true})
            }else{
                if (thing.blacklist) await models.PixelFrame.updateOne({uid: thing.uid}, {blacklist: false})
            }
            thing.save()
        }))

        let thing = await models.PixelFrame.findOne({uid: "9d0a831a5cd90b6f21f939850c50af05d34605f69a059fda0c4821b56ac1a7c1"})
        console.log(thing)
    }

    return { process }
}

let updater = updateBlacklist()
updater.process().then(() => process.exit(1))