import {config} from 'dotenv'
config()
import mongoose_models from './mongoose.models.mjs'
import mongoose from 'mongoose';
let db = mongoose;

/******* MONGO DB CONNECTION INFO **/
const NETWORK = process.env.NETWORK || 'testnet'
const DBUSER = process.env.DBUSER || null;
const DBPWD = process.env.DBPWD  || null;
const DBURL = process.env.DBURL || '127.0.0.1'
const DBPORT = process.env.DBPORT || '27017'
const DBNAME = process.env.DBNAME || `${NETWORK}-pixelframes`

let connectionString = `mongodb://${DBURL}:${DBPORT}/${DBNAME}`;

if (DBUSER) {
    connectionString = `mongodb://${DBUSER}:${DBPWD}@${DBURL}:${DBPORT}/${DBNAME}?authSource=admin`;
}

const getDatabase = () => new Promise(resolver => {
    db.connect(
        connectionString,
        { useNewUrlParser: true, useUnifiedTopology: true },
        (error) => {
            if (error) {
                console.log(error)
                throw new Error(error)
            }else {
                console.log("connection successful");
                resolver(db);
            }
        }
    );
})

export {
    mongoose_models,
    getDatabase
}

