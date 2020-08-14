import sirv from 'sirv';
import polka from 'polka';
import compression from 'compression';
import * as sapper from '@sapper/server';
global.fetch = require('node-fetch')
const fs = require('fs');

import {decodeFrames, letter_to_color, formatAccountAddress} from "./js/utils";

const GIFEncoder = require('gifencoder');

const { createCanvas } = require('canvas');


const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === 'development';

let dynamic = sirv('dynamic');
const dynamicRequest = /\/dynamic\/(\w+.gif)$/

async function create(req, res, next) {
	function createGifEncoder(resolution, frameSpeed) {
		var encoder = new GIFEncoder(resolution.x, resolution.y);

		var stream = encoder.createReadStream();
		res.setHeader('Content-Type', 'image/gif')
		console.log(req.headers['user-agent'])
		//if (req.headers['user-agent'].includes('facebookexternalhit')) res.setHeader('Content-Encoding', 'gzip')

		stream.pipe(res);
		encoder.start();

		// Set GIF parameters
		encoder.setRepeat(0);   // 0 for repeat, -1 for no-repeat
		encoder.setDelay(frameSpeed);  // frame delay in ms
		encoder.setQuality(15); // image quality. 10 is default.
		encoder.setTransparent('#ffffff00')

		return encoder;
	}

	function sendAsGIF(thingInfo) {
		let pixelSize = 20;
		let watermark = {text: formatAccountAddress(thingInfo.owner), fillColor: "#ff5bb0", strokeColor: "black"}
		const canvas = createCanvas(16 * pixelSize, 16  * pixelSize);
		var ctx = canvas.getContext("2d");
		let frames = decodeFrames(thingInfo.thing)

		try{
			var encoder = createGifEncoder({x: canvas.width, y: canvas.height}, thingInfo.speed);
		}catch (e){
			console.log(e)
		}

		frames.forEach((frame, index) => {
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			frame.forEach((letter, index) => {
				if (letter !== "B"){
					ctx.fillStyle = letter_to_color[letter];
					let rowBefore = Math.floor(index / 16)
					let rowAdj = (pixelSize * rowBefore)
					let y = Math.floor(index / 16)
					let x = (index - ( y * 16)) * pixelSize
					ctx.fillRect(x, rowAdj, pixelSize, pixelSize);
				}

			})
			ctx.font = `21pt Roboto`;

			ctx.textBaseline = 'middle';
			ctx.textAlign = 'center';
			ctx.strokeStyle = watermark.strokeColor;
			ctx.lineWidth = 1;
			ctx.miterLimit=2;
			ctx.strokeText('pixelframes.lamden.io', canvas.width / 2, canvas.height - (canvas.height / 4));
			ctx.fillStyle = watermark.fillColor;
			ctx.fillText('pixelframes.lamden.io', canvas.width / 2, canvas.height - (canvas.height / 4));
			encoder.addFrame(ctx);
		})

		encoder.finish();

	};

  	let pathMatch = req.path.match(dynamicRequest)
	if (pathMatch){
		let uid = pathMatch[1].split(".")[0]
		const thingInfo = await global.fetch('http://localhost:1337/things/con_pf_test/' + uid).then(data => data.json())
		if (thingInfo){
			try{
				sendAsGIF(thingInfo)
			}catch (e){
				console.log(e)
			}

		}else{
			next()
		}
	}else{
		next()
	}
}

polka() // You can also use Express
	.use(
		compression({ threshold: 0 }),
		create,
		sirv('static', { dev }),
		sapper.middleware()
	)
	.listen(PORT, err => {
		if (err) console.log('error', err);
	});
