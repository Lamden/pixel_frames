import fs from "fs";
import BN from 'bignumber.js'
import util from 'util'

const INFO_CONTRACT = process.env.INFO_CONTRACT || null
if (!INFO_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")
const AUCTION_CONTRACT = process.env.AUCTION_CONTRACT || null
if (!AUCTION_CONTRACT ) throw Error("Must pass INFO_CONTRACT via .env file")

const NETWORK = process.env.NETWORK || 'testnet'

export const infoContractProcessor = (database, socket_server, services) =>{
    const processorName = 'Info Contract'
    let db = database

    const updateProcessors = {
        createNewThing,
        soldThing,
        sellThing,
        likeThing,
        transferThing,
        updateAuthCodes
    }

    async function processUpdate(update, loader=false){
        if (!loader) console.log(util.inspect({processorName, update}, false, null, true))
        let last_tx_uid = update.tx_uid

        let { state_changes_obj } = update

        if (typeof state_changes_obj === 'string'){
            state_changes_obj = JSON.parse(state_changes_obj)
        }

        let auctionContractUpdates = {}
        try{
            auctionContractUpdates = state_changes_obj[AUCTION_CONTRACT]["S"]
        }catch (e){}

        if (await db.queries.shouldProcess('InfoContractUpdates', last_tx_uid)){
            let contractUpdate = {}
            try{
                contractUpdate = state_changes_obj[INFO_CONTRACT]["S"]
            }catch (e){}

            const { names } = contractUpdate

            for (const uid of Object.keys(contractUpdate || {})){
                if (uid.length === 64) {
                    let updateType = determineUpdateType(contractUpdate[uid])
                    if (Object.keys(updateProcessors).includes(updateType)) {
                        await updateProcessors[updateType]({
                            uid,
                            update: contractUpdate[uid],
                            names,
                            transactionInfo: update.txInfo,
                            auctionContractUpdates: auctionContractUpdates,
                            blockNum: update.blockNum,
                            loader
                        })
                    }
                }
            }
            await db.queries.update_processed('InfoContractUpdates', last_tx_uid)
        }
    }

    function determineUpdateType(update){
        if (!update || Object.keys(update).length === 0) return
        let updateKeys = Object.keys(update)

        if (updateKeys.includes("thing")) return 'createNewThing'
        if (updateKeys.length === 1 && updateKeys.includes("likes")) return 'likeThing'
        if (updateKeys.length === 1 && updateKeys.includes("proof")) return 'updateAuthCodes'
        if (updateKeys.length === 2 && updateKeys.every(i => ['owner', 'price'].includes(i))) return 'soldThing'
        if (updateKeys.length === 1 && updateKeys.includes("price")) return 'sellThing'
        if (updateKeys.length === 1 && updateKeys.includes("owner")) return 'transferThing'

        console.log('undetermined')
        console.log(util.inspect(update, false, null, true))
    }

    async function createNewThing(args){
        const { uid, update, names, transactionInfo, blockNum, loader } = args
        console.log({update: determineUpdateType(update)})
        if (determineUpdateType(update) !== "createNewThing") return

        const { hash, transaction, stamps_used } = transactionInfo
        const { metadata } = transaction

        var blacklist = JSON.parse(fs.readFileSync('./blacklist.json', 'utf8'));

        let exists = await db.models.PixelFrame.findOne({uid})
        if (exists) {
            console.log("Already exists in DB, ignoring update")
            return
        }else{
            console.log("Creating New Thing")
        }

        let thing = await new db.models.PixelFrame({
            txCreationHash: hash,
            creationBlock: blockNum,
            datetimeCreated: new Date(metadata.timestamp * 1000),
            uid,
            thing: update.thing,
            type: update.type,
            name: update.name,
            name_uid: names[uid],
            description: update.description,
            owner: update.owner,
            creator: update.creator,
            likes: 0,
            price_amount: "0",
            price_hold: "",
            speed: update.meta.speed,
            num_of_frames: update.meta.num_of_frames,
            royalty_percent: update.meta.royalty_percent,
            royalties_earned: "0",
            num_of_owners: 1,
            stamps_used,
            lastSaleDate: null,
            lastUpdate: new Date(metadata.timestamp * 1000),
            tx_uid: update.tx_uid,
            blacklist: blacklist.art.includes(uid) || blacklist.creators.includes(update.creator)
        })
        console.log(util.inspect({thing}, false, null, true))


        await thing.save()
            .then(async (err, doc) => {
                console.log("AFTER SAVE!")
                console.log({err})
                console.log(util.inspect({doc}, false, null, true))
                if (!loader) {
                    socket_server.to(`main-events`).emit("thing-update", {type: 'new-thing', update: doc})
                    if (NETWORK === 'mainnet' && services){
                        try{
                            // pusher.link("", "New #NFT Art!", `https://www.pixelwhale.io/frames/${uid}`);
                            let res = await services.twitterClient.tweets.statusesUpdate({
                                status: `New #NFT Art!\r\nhttps://www.pixelwhale.io/frames/${uid}\r\n\r\n#NFTartist #digitalartist #pixelart`
                            })
                            .catch(err => console.log(err))
                            console.log(res)
                        }catch (e) {}
                    }
                }
            })
            .catch(err => console.log(err))
    }

    async function sellThing(args){
        const { uid, update, loader, transactionInfo } = args

        const { transaction } = transactionInfo
        const { metadata } = transaction

        if (determineUpdateType(update) !== 'sellThing') return

        let pixel_frame = await db.models.PixelFrame.findOne({uid})
        if (!pixel_frame) return

        const { price } = update
        const { amount, hold } = price
        const { __fixed__ } = amount

        pixel_frame.price_hold = hold || ""
        pixel_frame.price_amount = __fixed__ || amount
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        pixel_frame.lastSaleDate = new Date(metadata.timestamp * 1000)


        await pixel_frame.save((err, doc) => {
            if (!loader) socket_server.to(`market-updates`).emit("market-update", {type: 'new-listing', update: doc})
        })

        return true
    }

    async function likeThing(args){
        const { uid, tx_uid, update, transactionInfo } = args

        if (determineUpdateType(update) !== "likeThing") return

        const { transaction } = transactionInfo
        const {  payload, metadata } = transaction

        const sender = payload.sender

        let pixel_frame = await db.models.PixelFrame.findOne({uid})

        if (!pixel_frame) {
            console.log("UID doesn't exist")
            return
        }
        if (pixel_frame.last_likes_tx_uid >= tx_uid) {
            console.log("Already processed this LIKE tx")
            return
        }

        pixel_frame.likes =  update.likes
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        pixel_frame.last_likes_tx_uid = tx_uid

        await pixel_frame.save((err, doc) => {
            // console.log({liked: err})
            // console.log({likedDoc: doc})
        })

        await update_uid_likes(uid, sender, tx_uid)
        await update_user_likes(uid, sender, tx_uid)
    }

    const update_uid_likes = async (uid, vk, tx_uid) => {
        let likes = await db.models.Likes.findOne({vk})
        if (!likes) {
            likes = await new db.models.Likes({
                uid,
                last_likes_tx_uid: tx_uid,
                liked_by: [vk]
            })
        }else{
            if (likes.last_likes_tx_uid >= tx_uid) {
                console.log("Already processed this LIKE tx")
                return
            }
            likes.liked_by.push(vk)
            likes.last_likes_tx_uid = tx_uid
            likes.isNew = false
        }

        await likes.save((err, doc) => {
            // console.log({"likes": err})
            // console.log({likesDoc: doc})
        })
    }

    const update_user_likes = async (uid, vk, tx_uid) => {
        let likedByUser = await db.models.LikedByUser.findOne({vk})
        if (!likedByUser) {
            likedByUser = await new db.models.LikedByUser({
                vk,
                last_likes_tx_uid: tx_uid,
                likes: [uid]
            })
        }else{
            if (likedByUser.last_likes_tx_uid >= tx_uid) {
                console.log("Already processed this LIKE tx")
                return
            }
            likedByUser.likes.push(uid)
        }
        await likedByUser.save((err, doc) => {
            // console.log({"likedByUser": err})
            // console.log({likedByUserDoc: doc})
        })
    }

    async function soldThing(args){
        const { uid, update, loader, transactionInfo } = args

        const { transaction } = transactionInfo
        const { metadata } = transaction

        if (determineUpdateType(update) !== 'soldThing') return

        let pixel_frame = await db.models.PixelFrame.findOne({uid})
        if (!pixel_frame) {
            console.log({uid_not_found: update})
            return
        }

        let newOwner = update.owner
        let seller = pixel_frame.owner
        let wasHeld = pixel_frame.price_hold !== ""
        let priceBN = new BN(pixel_frame.price_amount)
        let royaltyPaidBN = new BN("0")

        if (pixel_frame.royalty_percent > 0){
            royaltyPaidBN = priceBN.multipliedBy(pixel_frame.royalty_percent / 100)
            if (royaltyPaidBN.isNaN()) royaltyPaidBN = new BN("0")
            if (royaltyPaidBN.isGreaterThan(0)){
                let currentRoyaltiesBN = new BN(pixel_frame.royalties_earned)
                pixel_frame.royalties_earned = currentRoyaltiesBN.plus(royaltyPaidBN)
            }
        }

        await new db.models.SalesHistory({
            uid,
            saleDate: new Date(metadata.timestamp * 1000),
            price: pixel_frame.price_amount,
            royaltyPaid: royaltyPaidBN.toString(),
            seller,
            buyer: newOwner,
            wasHeld: wasHeld,
            gift: false,
            auction: false
        }).save()

        pixel_frame.price_hold = ""
        pixel_frame.price_amount =  "0"
        pixel_frame.owner = newOwner
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        pixel_frame.lastSaleDate = new Date(metadata.timestamp * 1000)

        await pixel_frame.save(async (err, doc) => {
            if (!loader) {
                socket_server.to(`market-updates`).emit("market-update", {type: 'new-sale', update: doc})
                if (NETWORK === 'mainnet' && services){
                    let priceData = await db.models.Prices.findOne({symbol: 'TAU'})
                    if (priceData){

                        /*
                        pusher.link(
                            "",
                            `#NFT Art Sold! ${priceBN.toFixed(3)} TAU ($${priceBN.multipliedBy(priceData.currentPrice).toFixed(2)} USD)`,
                            `https://www.pixelwhale.io/frames/${uid}`
                        );
                        */

                        let res = await services.twitterClient.tweets.statusesUpdate({
                            status: `#NFT Art Sold!\r\n${priceBN.toFixed(3)} TAU ($${priceBN.multipliedBy(priceData.currentPrice).toFixed(2)} USD)\r\n\r\nhttps://www.pixelwhale.io/frames/${uid} \r\n\r\n#NFTartist #digitalartist #pixelart`
                        })
                        .catch(err => console.log(err))
                        console.log(res)
                    }
                }
            }
        })

        return true
    }

    async function transferThing(args){
        const { uid, update, transactionInfo, auctionContractUpdates, loader } = args

        const { transaction } = transactionInfo
        const { metadata } = transaction

        if (determineUpdateType(update) !== 'transferThing') return

        // Check to see if this was a transfer due to auction. Logging this will be in the AuctionContract processor
        if (Object.keys(auctionContractUpdates || {}).includes(uid)){
                const { owner } = auctionContractUpdates[uid]
                if (owner === update.owner) return
        }

        let pixel_frame = await db.models.PixelFrame.findOne({uid})

        let newOwner = update.owner
        let seller = pixel_frame.owner

        pixel_frame.price_hold = ""
        pixel_frame.price_amount =  "0"

        if (newOwner !== AUCTION_CONTRACT && seller !== AUCTION_CONTRACT) {
            pixel_frame.owner = newOwner

            await new db.models.SalesHistory({
                uid,
                saleDate: new Date(metadata.timestamp * 1000),
                price: 0,
                royaltyPaid: 0,
                seller,
                buyer: newOwner,
                wasHeld: false,
                gift: true,
                auction: false
            }).save()
        }

        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)

        await pixel_frame.save(async (err, doc) => {
            if (!loader) {
                socket_server.to(`market-updates`).emit("market-update", {type: 'new-transfer', update: doc})

                if (NETWORK === 'mainnet' && services){
                    let priceData = await db.models.Prices.findOne({symbol: 'TAU'})
                    if (priceData){

                        /*
                        pusher.link(
                            "",
                            `#NFT Art Sold! ${priceBN.toFixed(3)} TAU ($${priceBN.multipliedBy(priceData.currentPrice).toFixed(2)} USD)`,
                            `https://www.pixelwhale.io/frames/${uid}`
                        );
                        */

                        let res = await services.twitterClient.tweets.statusesUpdate({
                            status: `#NFT Art Sold!\r\n${priceBN.toFixed(3)} TAU ($${priceBN.multipliedBy(priceData.currentPrice).toFixed(2)} USD)\r\n\r\nhttps://www.pixelwhale.io/frames/${uid} \r\n\r\n#NFTartist #digitalartist #pixelart`
                        })
                        .catch(err => console.log(err))
                        console.log(res)
                    }
                }
            }
        })

        return true
    }

    async function updateAuthCodes(args){
        const { uid, transactionInfo, update } = args

        const { transaction } = transactionInfo
        const {  metadata } = transaction

        let authCodeInfo = await db.models.AuthCodes.findOne({uid})

        if (!authCodeInfo) return

        if (authCodeInfo.code === update.proof){
            authCodeInfo.validated = true
            dateValidated: new Date(metadata.timestamp * 1000)
        }
        await authCodeInfo.save()
    }

    return {
        setDb: (database) => db = database,
        processUpdate,
        determineUpdateType,
        createNewThing
    }
}