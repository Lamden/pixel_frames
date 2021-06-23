import https from 'https';
import http from 'http';
import mongoose from "mongoose";

const runBlockGrabber = (config ) => {
	const { WIPE, RE_PARSE_BLOCKS, MASTERNODE_URL, START_AT_BLOCK_NUMBER, DEBUG_ON, utils, models, db } = config

	var wipeOnStartup = WIPE;
	var reParseBlocks = RE_PARSE_BLOCKS;

	let stop = false;
	let currBlockNum = START_AT_BLOCK_NUMBER;
	let checkNextIn = 0;
	let maxCheckCount = 10;
	let alreadyCheckedCount = 0;
	const route_getBlockNum = "/blocks?num=";
	const route_getLastestBlock = "/latest_block";
	let lastestBlockNum = 0;
	let currBatchMax = 0;
	let batchAmount = 49;
	let timerId;
	let lastCheckTime = new Date();
	let runID = Math.floor(Math.random() * 1000)

	const wipeDB = async (force = false) => {
		console.log("-----WIPING DATABASE-----");
		const toWipe = ['PixelFrame', 'Likes', 'LikedByUser', 'SalesHistory', 'AuthCodes']

		if (wipeOnStartup || force){
			await db.models.Blocks.deleteMany({}).then((res) => {
				console.log("Blocks DB wiped")
				console.log(res)
			});
		}
		toWipe.map(model => {
			return db.models[model].deleteMany({}).then((res) => {
				console.log(`${model} DB wiped`);
				console.log(res)
			});
		})
		currBlockNum = START_AT_BLOCK_NUMBER;
		console.log(`Set currBlockNum = ${START_AT_BLOCK_NUMBER}`);
		timerId = setTimeout(checkForBlocks, 500);


	};

	const sendBlockRequest = (url) => {
		return new Promise((resolve) => {
			let protocol = http;
			if (url.includes("https://")) protocol = https;
			protocol
				.get(url, (resp) => {
					let data = "";
					resp.on("data", (chunk) => {
						data += chunk;
					});
					resp.on("end", () => {
						try {
							// console.log(data);
							resolve(JSON.parse(data));
						} catch (err) {
							console.error("Error: " + err);
							resolve({ error: err.message });
						}
					});
				})
				.on("error", (err) => {
					console.error("Error: " + err.message);
					resolve({ error: err.message });
				});
		});
	};

	const processBlock = async (blockInfo) => {
		if (
			typeof blockInfo.error === "undefined" &&
			typeof blockInfo.number !== "undefined"
		) {
			let blockNum = blockInfo.number.__fixed__ ? parseInt(blockInfo.number.__fixed__) : blockInfo.number;
			let block = await models.Blocks.findOne({blockNum})
			if (!block){
				//console.log("Block doesn't exists, adding new BLOCK model")
				block = new models.Blocks({
					rawBlock: JSON.stringify(blockInfo),
					blockNum,
					hash: blockInfo.hash
				}).save();
			}else{
				//console.log("Block already exists, not adding BLOCK model")
			}
			/*
			console.log(
				"processing block " + blockNum + " - ",
				blockInfo.hash
			);
			*/

			if (typeof blockInfo.subblocks !== "undefined") {
				blockInfo.subblocks.forEach((sb) => {
                    sb.transactions.forEach( async (tx) => {
						if (utils.isPixelFramesContract(tx.transaction.payload.contract)) {
							//console.log(tx.result.length)
							if (!tx.result.includes('AssertionError(') && tx.status === 0){
								if (tx.transaction.payload.function === 'create_thing' && tx.result.length === 66) {
									await utils.create_new_thing(tx, blockNum)
								}
								if (tx.result === "None"){
									if (tx.transaction.payload.function === 'like_thing') {
										await utils.update_liked(tx)
									}
									if (tx.transaction.payload.function === 'sell_thing' || tx.transaction.payload.function === 'sell_thing_to') {
										await utils.update_price_info(tx)
									}
									if (tx.transaction.payload.function === 'buy_thing' ||
										tx.transaction.payload.function === 'transfer' ||
										tx.transaction.payload.function === 'transfer_from') {
										await utils.update_change_ownership(tx)
									}
									if (tx.transaction.payload.function === 'prove_ownership') {
										await utils.update_auth_codes(tx)
									}
								}
							}
						}else{
							await utils.process_auction_transaction(tx)
						}
                    })
				});
			}



			if (blockNum === currBatchMax) {
				currBlockNum = currBatchMax;
				timerId = setTimeout(checkForBlocks, 200);
			}
		}
	};

	const getBlock_MN = (blockNum, timedelay = 0) => {
		return new Promise(resolver => {
			setTimeout(async () => {
				const block_res = await sendBlockRequest(`${MASTERNODE_URL}${route_getBlockNum}${blockNum}`);
				resolver(block_res);
			}, timedelay)
		})
	};

	const getLatestBlock_MN = () => {
		return new Promise((resolve, reject) => {
			const returnRes = async (res) => {
				resolve(res);
			};

			const res = sendBlockRequest(
				`${MASTERNODE_URL}${route_getLastestBlock}`
			);
			returnRes(res);
		});
	};

	const checkForBlocks = async () => {
		if (stop) return
		lastCheckTime = new Date()
        if(DEBUG_ON){
            console.log(runID + ": checking")
        }
		let response = await getLatestBlock_MN();

		if (!response.error) {

			lastestBlockNum = response.number;
			if (lastestBlockNum.__fixed__) lastestBlockNum = parseInt(lastestBlockNum.__fixed__)
			if (lastestBlockNum < currBlockNum || wipeOnStartup || reParseBlocks) {
				await wipeDB();
				wipeOnStartup = false;
				reParseBlocks = false;
			} else {
                if (DEBUG_ON){
                    console.log("lastestBlockNum: " + lastestBlockNum);
                    console.log("currBlockNum: " + currBlockNum);
                }
				if (lastestBlockNum === currBlockNum) {
					if (alreadyCheckedCount < maxCheckCount)
						alreadyCheckedCount = alreadyCheckedCount + 1;
					checkNextIn = 200 * alreadyCheckedCount;
					timerId = setTimeout(checkForBlocks, checkNextIn);
				}

				let to_fetch = [];
				if (lastestBlockNum > currBlockNum) {
					currBatchMax = currBlockNum + batchAmount;
					if (currBatchMax > lastestBlockNum)
						currBatchMax = lastestBlockNum;
					if (currBatchMax > batchAmount) currBatchMax + batchAmount;
					let blocksToGetCount = 1
					for (let i = currBlockNum + 1; i <= currBatchMax; i++) {
						let blockInfo = await models.Blocks.findOne({blockNum: i})
						let blockData = null;
						if(blockInfo) {
							blockData = JSON.parse(blockInfo.rawBlock)
						}else{
                            const timedelay = blocksToGetCount * 250;
                            if (DEBUG_ON){
                                console.log("getting block: " + i + " with delay of " + timedelay + "ms");
                            }

							blockData = getBlock_MN(i, timedelay)
							blocksToGetCount = blocksToGetCount + 1
						}
						to_fetch.push(blockData);
					}

					let to_process = await Promise.all(to_fetch);
					to_process.sort((a, b) => a.number - b.number);
					for (let block of to_process) await processBlock(block);
				}

				if (lastestBlockNum < currBlockNum) {
					await wipeDB(true);
					timerId = setTimeout(checkForBlocks, 10000);
				}
			}
		} else {
			console.log(runID + ": Could not contact masternode, trying again in 10 seconds");
			timerId = setTimeout(checkForBlocks, 10000);
		}
	};

	models.Blocks.findOne()
		.sort({ blockNum: -1 })
		.then(async (res) => {
			if (res) currBlockNum = res.blockNum ? res.blockNum : 0;
			else currBlockNum = 0;
			timerId = setTimeout(checkForBlocks, 0);
		});

	return {
		lastCheckedTime: () => lastCheckTime,
		stop: () => {
			clearInterval(timerId)
			timerId = null
			stop = true
		}
	}
};

export {
	runBlockGrabber
}