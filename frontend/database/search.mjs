import { getDatabase, mongoose_models} from "../database/database.mjs";

var myArgs = process.argv.slice(2);
var searchItem = myArgs[0]

const search = () => {
    const process = async () => {
        let db = await getDatabase()
        let models = mongoose_models

        let things = await models.PixelFrame.find({uid: searchItem})
        console.log(things)
    }

    return { process }
}

let searcher = search()
searcher.process().then(() => process.exit(1))