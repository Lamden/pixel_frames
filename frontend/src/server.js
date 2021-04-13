import polka from 'polka';
import crypto from 'crypto'
import sirv from 'sirv';
let dynamicGIF = sirv('gif');
import * as sapper from '@sapper/server';
import Lamden from 'lamden-js'

import compression from 'compression';
import { getDatabase, mongoose_models} from "../database/database.mjs";
const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === 'development';

global.db = getDatabase()
global.models = mongoose_models
global.fetch = require('node-fetch')
global.randomHash = () => {
	return crypto.createHash("sha256")
		.update(Lamden.utils.randomString(16))
		.digest("hex");
}

import { createGIF } from './js/server_createGIF.mjs'

polka() // You can also use Express
	.use(
		compression({ threshold: 0 }),
		createGIF,
		sirv('static', { dev }),
		sapper.middleware()
	)
	.listen(PORT, err => {
		if (err) console.log('error', err);
	});
