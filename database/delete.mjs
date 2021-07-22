import { getDatabase, mongoose_models} from "./database.mjs";

var myArgs = process.argv.slice(2);
var itemID = myArgs[0]

const delete_it = () => {
    const process = async () => {
        let db = await getDatabase()
        let models = mongoose_models

        await models.PixelFrame.deleteOne({_id: itemID})
    }

    return { process }
}

let deleter = delete_it()
deleter.process().then(() => process.exit(1))