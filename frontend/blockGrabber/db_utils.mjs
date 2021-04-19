import Lamden from 'lamden-js'
import fs from "fs";

import PushBullet from 'pushbullet';
var pusher = new PushBullet('o.mMOJzuOmDBQpWrhpplu44dVsmhOx1M7o');

export const getDbUtils = (config) => {
    const { models } = config
    const { INFO_CONTRACT, MASTER_CONTRACT } = config
    const PIXEL_FRAMES_META = {
        thing: "thing",
        type: "type",
        name: "name",
        description: "description",
        owner: "owner",
        creator: "creator",
        likes: "likes",
        "price:amount": "price_amount",
        "price:hold": "price_hold",
        "meta:speed": "speed",
        "meta:num_of_frames": "num_of_frames",
        "meta:royalty_percent": "royalty_percent"
    }

    const create_new_thing = async (transactionInfo, blockNmber) => {
        const {hash, result, transaction, stamps_used, state } = transactionInfo
        const { metadata } = transaction
        console.log({result})

        const uid = result.replace(/'/g, '');
        var blacklist = JSON.parse(fs.readFileSync('./blockGrabber/blacklist.json', 'utf8'));

        let stateValues = getStateValues(state, uid)

        let exists = await models.PixelFrame.findOne({uid})
        if (exists) return

        await new models.PixelFrame({
            txCreationHash: hash,
            creationBlock: blockNmber,
            datetimeCreated: new Date(metadata.timestamp * 1000),
            uid,
            thing: stateValues.thing,
            type: stateValues.type,
            name: stateValues.name,
            name_uid: getNameUID(state),
            description: stateValues.description,
            owner: stateValues.owner,
            creator: stateValues.creator,
            likes: 0,
            price_amount: "0",
            price_hold: "",
            speed: stateValues.speed,
            num_of_frames: stateValues.num_of_frames,
            royalty_percent: stateValues.royalty_percent,
            royalties_earned: "0",
            num_of_owners: 1,
            stamps_used,
            lastSaleDate: null,
            lastUpdate: new Date(metadata.timestamp * 1000),
            blacklist: blacklist.art.includes(uid) || blacklist.creators.includes(stateValues.creator)
        }).save()

        console.log({
            txCreationHash: hash,
            creationBlock: blockNmber,
            lastUpdateBlock: blockNmber,
            datetimeCreated: new Date(metadata.timestamp * 1000),
            uid,
            thing: stateValues.thing,
            type: stateValues.type,
            name: stateValues.name,
            name_uid: getNameUID(state),
            description: stateValues.description,
            owner: stateValues.owner,
            creator: stateValues.creator,
            likes: 0,
            price_amount: "0",
            price_hold: "",
            speed: stateValues.speed,
            num_of_frames: stateValues.num_of_frames,
            royalty_percent: stateValues.royalty_percent,
            royalties_earned: "0",
            num_of_owners: 1,
            stamps_used,
            lastSaleDate: null,
            lastUpdate: new Date(metadata.timestamp * 1000)
        })
        try{
            pusher.link("", "New Art", `https://www.pixelwhale.io/frames/${uid}`);
        }catch (e) {}
    }

    const update_liked = async (transactionInfo) => {
        //console.log({})
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const uid =  payload.kwargs.uid
        const sender = payload.sender
        let pixel_frame = await models.PixelFrame.findOne({uid})
        if (!pixel_frame) return
        pixel_frame.likes =  getStateValue(state, makeThingKey(uid, 'likes'))
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        await pixel_frame.save()
        //console.log({transaction, state, payload, uid})
        await update_uid_likes(uid, sender)
        await update_user_likes(sender, uid)

    }
    const update_uid_likes = async (uid, vk) => {
        //console.log({vk, uid})
        let likes = await models.Likes.findOne({vk})
        if (!likes) {
            likes = await new models.Likes({
                uid,
                liked_by: [vk]
            })
        }else{
            likes.liked_by.push(vk)
        }
        //console.log({likes})
        await likes.save()
    }

    const update_user_likes = async (vk, uid) => {
        //console.log({vk, uid})
        let likedByUser = await models.LikedByUser.findOne({vk})
        if (!likedByUser) {
            likedByUser = await new models.LikedByUser({
                vk,
                likes: [uid]
            })
        }else{
            likedByUser.likes.push(uid)
        }
        //console.log({likedByUser})
        await likedByUser.save()
    }

    const update_price_info = async (transactionInfo) => {
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const uid =  payload.kwargs.uid
        let pixel_frame = await models.PixelFrame.findOne({uid})
        pixel_frame.price_amount =  getStateValue(state, makeThingKey(uid, 'price:amount'))
        pixel_frame.price_hold = getStateValue(state, makeThingKey(uid, 'price:hold')) || ""
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        await pixel_frame.save()
    }

    const update_change_ownership = async (transactionInfo) => {
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const uid =  payload.kwargs.uid

        let pixel_frame = await models.PixelFrame.findOne({uid})
        let newOwner = getStateValue(state, makeThingKey(uid, 'owner'))
        let seller = pixel_frame.owner
        let wasHeld = pixel_frame.price_hold !== ""
        let priceBN = toBigNumber(pixel_frame.price_amount)
        let royaltyPaid = "0"
        if (priceBN.isGreaterThan(0)) {
            royaltyPaid = priceBN.multipliedBy(pixel_frame.royalty_percent / 100)
            if (royaltyPaid.isNaN()) royaltyPaid = toBigNumber("0")
            if (royaltyPaid.isGreaterThan(0)){
                let currentRoyalties = toBigNumber(pixel_frame.royalties_earned)
                pixel_frame.royalties_earned = currentRoyalties.plus(royaltyPaid)
            }
        }


        await new models.SalesHistory({
            uid,
            saleDate: new Date(metadata.timestamp * 1000),
            price: pixel_frame.price_amount,
            royaltyPaid: royaltyPaid.toString(),
            seller,
            buyer: newOwner,
            wasHeld: wasHeld,
            gift: payload.function === "transfer" || payload.function === "transfer_from"
        }).save()

        pixel_frame.price_hold = ""
        pixel_frame.price_amount =  "0"
        pixel_frame.owner = newOwner
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        pixel_frame.lastSaleDate = new Date(metadata.timestamp * 1000)
        await pixel_frame.save()

        if (payload.function !== "transfer" && payload.function !== "transfer_from"){
            try{
                pusher.link("", `Sale - ${priceBN.toFixed(8)}`, `https://www.pixelwhale.io/frames/${uid}`);
            }catch (e) {}
        }
    }

    const update_auth_codes = async (transactionInfo) => {
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const { uid } = payload.kwargs
        console.log('!!!!!  FOUND AUTH CODE !!!!')
        let authCodeInfo = await models.AuthCodes.findOne({uid})
        //console.log({authCodeInfo_UpdateAuthCodes: authCodeInfo, payload, state})
        if (!authCodeInfo) return

        let code = getStateValue(state, makeThingKey(uid, 'proof'))
        //console.log({code})

        if (authCodeInfo.code === code){
            authCodeInfo.validated = true
            dateValidated: new Date(metadata.timestamp * 1000)
        }
        await authCodeInfo.save()
    }

    function getStateValues(state, uid) {
        let stateValues = {}
        Object.keys(PIXEL_FRAMES_META).map(meta_item => {
            stateValues[PIXEL_FRAMES_META[meta_item]] = getStateValue(state, `${INFO_CONTRACT}.S:${uid}:${meta_item}`)
        })
        return stateValues;
    }

    function getStateValue(state, key) {
        let stateChange = state.find(s => s.key === key)
        if (!stateChange) return null
        if (!stateChange.value) return null
        if (stateChange.value.__fixed__) return stateChange.value.__fixed__
        return stateChange.value
    }

    function getNameUID(state){
        let names_uid_state_change = state.find(s => s.key.includes(`${INFO_CONTRACT}.S:names:`)).key
        return names_uid_state_change.split(":")[2]
    }

    function makeThingKey(uid, metaitem){
        return `${INFO_CONTRACT}.S:${uid}:${metaitem}`
    }

    function toBigNumber (value) {
      if (Lamden.Encoder.BigNumber.isBigNumber(value)) return value
      return Lamden.Encoder.BigNumber(value)
    }

    return  {
        create_new_thing,
        update_liked,
        update_price_info,
        update_change_ownership,
        update_auth_codes,
        toBigNumber
    }
}

