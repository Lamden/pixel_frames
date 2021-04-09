import Lamden from 'lamden-js'

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
        "meta:num_of_frames": "num_of_frames"
    }

    const create_new_thing = async (transactionInfo, blockNmber) => {
        const {hash, result, transaction, stamps_used, state } = transactionInfo
        const { metadata } = transaction
        const uid = result.replaceAll("'", "")

        let stateValues = getStateValues(state, uid)

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
            num_of_owners: 1,
            stamps_used,
            lastSaleDate: null,
            lastUpdate: new Date(metadata.timestamp * 1000)
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
            num_of_owners: 1,
            stamps_used,
            lastSaleDate: null,
            lastUpdate: new Date(metadata.timestamp * 1000)
        })
    }

    const update_liked = async (transactionInfo) => {
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const uid =  payload.kwargs.uid
        const sender = payload.sender
        let pixel_frame = await models.PixelFrame.findOne({uid})
        pixel_frame.likes =  getStateValue(state, makeThingKey(uid, 'likes'))
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        await pixel_frame.save()

        await update_uid_likes(uid, sender)
        await update_user_likes(sender, uid)

    }
    const update_uid_likes = async (uid, vk) => {
        let likes = await models.Likes.findOne({vk})
        if (!likes) {
            likes = await new models.Likes({
                uid,
                liked_by: [vk]
            })
        }else{
            likes.liked_by.push(vk)
        }
        await likes.save()
    }

    const update_user_likes = async (vk, uid) => {
        let likedByUser = await models.LikedByUser.findOne({vk})
        if (!likedByUser) {
            likedByUser = await new models.LikedByUser({
                vk,
                likes: [uid]
            })
        }else{
            likedByUser.likes.push(uid)
        }
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

        await new models.SalesHistory({
            uid,
            saleDate: new Date(metadata.timestamp * 1000),
            price: pixel_frame.price_amount,
            seller,
            buyer: newOwner,
            wasHeld: wasHeld,
            gift: payload.function === "give_thing"
        }).save()

        pixel_frame.price_hold = ""
        pixel_frame.price_amount =  "0"
        pixel_frame.owner = newOwner
        pixel_frame.lastUpdate = new Date(metadata.timestamp * 1000)
        pixel_frame.lastSaleDate = new Date(metadata.timestamp * 1000)
        await pixel_frame.save()
    }

    const update_auth_codes = async (transactionInfo) => {
        const { transaction, state } = transactionInfo
        const {  payload, metadata } = transaction
        const { uid } = payload.kwargs
        console.log('!!!!!  FOUND AUTH CODE !!!!')
        let authCodeInfo = await models.AuthCodes.findOne({uid})
        console.log({authCodeInfo_UpdateAuthCodes: authCodeInfo, payload, state})
        if (!authCodeInfo) return

        let code = getStateValue(state, makeThingKey(uid, 'proof'))
        console.log({code})

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
        if (stateChange.value.__fixed__) return value.__fixed__
        return stateChange.value
    }

    function getNameUID(state){
        let names_uid_state_change = state.find(s => s.key.includes(`${INFO_CONTRACT}.S:names:`)).key
        return names_uid_state_change.split(":")[2]
    }

    function makeThingKey(uid, metaitem){
        return `${INFO_CONTRACT}.S:${uid}:${metaitem}`
    }

    return  {
        create_new_thing,
        update_liked,
        update_price_info,
        update_change_ownership,
        update_auth_codes
    }
}

