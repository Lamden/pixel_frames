import {config} from 'dotenv'
config()

import { getDatabase} from "./database.mjs"

const runQuery = async (queryName) => {
    const db = await getDatabase()

    // Validate Args
    const availableQueries = Object.keys(db.queries)

     if (!availableQueries.includes(queryName)) {
        throw new Error(`Query doesn't exists. Queries available are: ${availableQueries.join(", ")}`)
    }

     let results =  await db.queries[queryName]()
    console.log({results})
    process.exit(1)
}

let [queryName] = process.argv.slice(2)
runQuery(queryName)
