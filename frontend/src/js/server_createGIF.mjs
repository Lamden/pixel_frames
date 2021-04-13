import {decodeFrames, letter_to_color} from "./utils";
const GIFEncoder2 = require('gif-encoder-2')
var {Base64Encode} = require('base64-stream');
import fs from 'fs'
const { createCanvas, registerFont } = require('canvas');
process.env.FONTCONFIG_PATH = '/etc/fonts'
registerFont('../frontend/src/fonts/Roboto-Medium.ttf', { family: 'Roboto' })
import { config } from './config'

const dynamicRequest = /\/dynamic\/(\w+.gif)$/

export const createGIF = async  (req, res, next) => {
  	let pathMatch = req.path.match(dynamicRequest)
  	let shareLink;
	if (pathMatch){
		let uid = pathMatch[1].split(".")[0]
        if (uid.substring(0, 5) === "share"){
            uid = uid.split("_")[1]
            shareLink = pathMatch[1].split(".")[0]
            let shareLinkRes = await global.models.ShareLinks.findOne({link: shareLink})

            if (shareLink && !shareLinkRes) {
                next()
                return
            }
        }
		const thingInfo = await global.models.PixelFrame.findOne({uid})
		if (thingInfo){
		    try{
                let fileName = shareLink || uid
		        if(fs.existsSync(`./GIFS/${fileName}.gif`)) sendGifFromDisk(res, thingInfo, fileName)
                else createAndSendGIF2(res, thingInfo, shareLink)
            }catch (e){
                console.log(e)
                createAndSendGIF2(res, thingInfo, shareLink)
            }
		}else{
			next()
		}
	}else{
		next()
	}
}

function createAndSendGIF2(res, thingInfo, shareLink = false) {
    console.log("CREATING NEW")
    res.setHeader('Content-Type', 'image/gif')
    //if (req.headers['user-agent'].includes('facebookexternalhit')) res.setHeader('Content-Encoding', 'gzip')

    let pixelSize = 15;
    let numOfPixels = config.frameWidth
    let watermark = {fillColor: "#21d6ab", strokeColor: "black"}
    const canvas = createCanvas(numOfPixels * pixelSize, numOfPixels  * pixelSize);
    let ctx = canvas.getContext("2d");
    let frames = decodeFrames(thingInfo.thing)
    let fileName = shareLink || thingInfo.uid

    let encoder = new GIFEncoder2(canvas.width, canvas.height);

    let stream = encoder.createReadStream();

    stream.pipe(res)
    stream.pipe(fs.createWriteStream(`./GIFS/${fileName}.gif`))

    encoder.start();

    encoder.setRepeat(0);   // 0 for repeat, -1 for no-repeat
    encoder.setDelay(thingInfo.speed);  // frame delay in ms
    encoder.setQuality(1); // image quality. 10 is default.
    encoder.setThreshold(0);
    encoder.setTransparent("0x00FF15")

    frames.forEach((frame, index) => {
        if (index <= frames.length){
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            frame.forEach((letter, index) => {
                if (letter === "A") ctx.fillStyle = "#00ff15"
                else ctx.fillStyle = letter_to_color[letter];

                let rowBefore = Math.floor(index / numOfPixels)
                let rowAdj = (pixelSize * rowBefore)
                let y = Math.floor(index / numOfPixels)
                let x = (index - (y * numOfPixels)) * pixelSize
                ctx.fillRect(x, rowAdj, pixelSize, pixelSize);

                if (!shareLink){
                    ctx.font = `21pt Roboto`;
                    ctx.textBaseline = 'middle';
                    ctx.textAlign = 'center';
                    ctx.strokeStyle = watermark.strokeColor;
                    ctx.lineWidth = 1;
                    ctx.miterLimit=2;
                    ctx.strokeText(config.watermark, canvas.width / 2, canvas.height - (canvas.height / 7));
                    ctx.fillStyle = watermark.fillColor;
                    ctx.fillText(config.watermark, canvas.width / 2, canvas.height - (canvas.height / 7));
                }
            })
            encoder.addFrame(ctx);

        }

    })
    encoder.finish();
};


function sendGifFromDisk(res, thingInfo, shareLink){
    console.log("SENDING FROM FILE SYSTEM")
    const stat = fs.statSync(`./GIFS/${shareLink}.gif`);
    res.writeHead(200, {
        'Content-Type': 'image/gif',
        'Content-Length': stat.size
    });
    let readStream = fs.createReadStream(`./GIFS/${shareLink}.gif`);
    readStream.pipe(res);
}

/*
    Old Gif creation method

 */


/*
const GIFEncoder = require('gifencoder');

function createAndSendGIF(res, thingInfo, shareLink = false) {
    console.log("CREATING NEW")
    res.setHeader('Content-Type', 'image/gif')
    //if (req.headers['user-agent'].includes('facebookexternalhit')) res.setHeader('Content-Encoding', 'gzip')

    let pixelSize = 15;
    let numOfPixels = config.frameWidth
    let watermark = {fillColor: "#21d6ab", strokeColor: "black"}
    const canvas = createCanvas(numOfPixels * pixelSize, numOfPixels  * pixelSize);
    let ctx = canvas.getContext("2d");
    let frames = decodeFrames(thingInfo.thing)
    let fileName = shareLink || thingInfo.uid

    let encoder = new GIFEncoder(canvas.width, canvas.height);

    let stream = encoder.createReadStream();

    stream.pipe(res)
    //stream.pipe(fs.createWriteStream(`./GIFS/${fileName}.gif`))

    encoder.start();

    encoder.setRepeat(0);   // 0 for repeat, -1 for no-repeat
    encoder.setDelay(thingInfo.speed);  // frame delay in ms
    encoder.setQuality(1); // image quality. 10 is default.
    //encoder.setTransparent("#FEE2E2")

    frames.forEach((frame, index) => {
        if (index <= 1){
            //ctx.clearRect(0, 0, canvas.width, canvas.height);
            frame.forEach((letter, index) => {
                //if (letter !== "A"){
                    ctx.fillStyle = letter_to_color[letter];
                    console.log({color: ctx.fillStyle, letter} )
                    let rowBefore = Math.floor(index / numOfPixels)
                    let rowAdj = (pixelSize * rowBefore)
                    let y = Math.floor(index / numOfPixels)
                    let x = (index - ( y * numOfPixels)) * pixelSize
                    ctx.fillRect(x, rowAdj, pixelSize, pixelSize);
                //}
            })
            if (!shareLink){
                ctx.font = `21pt Roboto`;
                ctx.textBaseline = 'middle';
                ctx.textAlign = 'center';
                ctx.strokeStyle = watermark.strokeColor;
                ctx.lineWidth = 1;
                ctx.miterLimit=2;
                ctx.strokeText(config.watermark, canvas.width / 2, canvas.height - (canvas.height / 8));
                ctx.fillStyle = watermark.fillColor;
                ctx.fillText(config.watermark, canvas.width / 2, canvas.height - (canvas.height / 8));
            }

            encoder.addFrame(ctx);
        }

    })
    encoder.finish();
};
*/