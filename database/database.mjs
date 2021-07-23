import {config} from 'dotenv'
config()
import mongoose_models from './mongoose.models.mjs'
import { getQueries } from './db_queries.mjs'
import { getServices } from './db_services.mjs'

import mongoose from 'mongoose';

/******* MONGO DB CONNECTION INFO **/
const NETWORK = process.env.NETWORK || 'testnet'
const DBUSER = process.env.DBUSER || null;
const DBPWD = process.env.DBPWD  || null;
const DBURL = process.env.DBURL || '127.0.0.1'
const DBPORT = process.env.DBPORT || '27017'
const DBNAME = process.env.DBNAME || `${NETWORK}-pixelframes`

let connectionString = `mongodb://${DBURL}:${DBPORT}/${DBNAME}`;
console.log({connectionString})

if (DBUSER) {
    connectionString = `mongodb://${DBUSER}:${DBPWD}@${DBURL}:${DBPORT}/${DBNAME}?authSource=admin`;
}



export const getDatabase = () => new Promise(resolver => {
    let db = mongoose;

    db.connect(
        connectionString,
        { useNewUrlParser: true, useUnifiedTopology: true },
        (error) => {
            if (error) {
                console.log(error)
                throw new Error(error)
            }else {
                console.log("connection successful");
                db.models = mongoose_models
                db.queries = getQueries(db)
                //db.services = getServices()
                resolver(db);
            }
        }
    );
})


