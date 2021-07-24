import {config} from 'dotenv'
config()

import {getQueries} from './db_queries.mjs'
import { getDatabase} from "./database.mjs"

const runQuery = async (queryName) => {
    const db = await getDatabase()
    console.log(db)
    const queries = getQueries(db)

    // Validate Args
    const availableQueries = Object.keys(queries)

     if (!availableQueries.includes(queryName)) {
        throw new Error(`Query doesn't exists. Queries available are: ${availableQueries.join(", ")}`)
    }

     let results =  await queries[queryName]()
    console.log({results})
    process.exit(1)
}

let [queryName] = process.argv.slice(2)
runQuery(queryName)
