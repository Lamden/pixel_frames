import { getDatabase, mongoose_models} from "./database.mjs";

var myArgs = process.argv.slice(2);
var uid = myArgs[0]

const sales_history = () => {
    const process = async () => {
        let db = await getDatabase()
        let models = mongoose_models

        let things = await models.SalesHistory.find({uid})
        console.log(things)
    }

    return { process }
}

let salesHistory = sales_history()
salesHistory.process().then(() => process.exit(1))