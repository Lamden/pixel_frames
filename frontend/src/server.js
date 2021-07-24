import polka from 'polka';
const http = require('http');
const io = require('socket.io')
const server = http.createServer();
import * as socketserver from './socketserver.js'
import { getBlockService } from '../../blockserviceAPI/blockservice.mjs'

import crypto from 'crypto'
import sirv from 'sirv';
let dynamicGIF = sirv('gif');
import * as sapper from '@sapper/server';
import Lamden from 'lamden-js'

import compression from 'compression';
import { getDatabase } from "../../database/database.mjs";
import {createGIF} from "./js/server_createGIF.mjs";

const { PORT, NODE_ENV, DATABASE_SERVICE_PORT, DATABASE_SERVICE_URL, BLOCKSERVICE_PORT } = process.env;
const dev = NODE_ENV === 'development';

const initGlobal = async () => {
	global.db = await getDatabase()

	global.blockservice = getBlockService('http://localhost', BLOCKSERVICE_PORT || 3535)
	global.fetch = require('node-fetch')

	global.randomHash = () => {
		return crypto.createHash("sha256")
			.update(Lamden.utils.randomString(16))
			.digest("hex");
	}

	let auctions = await global.db.models.AuctionHistory.find({})
	console.log({auctions})

	let things = await global.db.models.PixelFrame.find({})
		.sort({likes: -1})
		.limit(5)
	console.log({things})

}

initGlobal().then(() => {
	polka({server})
		.use(
			compression({ threshold: 0 }),
			createGIF,
			sirv('static', { dev }),
			sapper.middleware()
		)
		.listen(PORT, err => {
			if (err) console.log('error', err);
		});

	socketserver.start(io(server), DATABASE_SERVICE_URL, DATABASE_SERVICE_PORT, BLOCKSERVICE_PORT)
})
