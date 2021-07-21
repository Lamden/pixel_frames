import mongoose from 'mongoose';

var stamps = new mongoose.Schema({
  contractName: String,
  functionName: String,
  max: Number,
  min: Number,
  avg: Number,
  numOfTxs: Number,
});

var pixelFrame = new mongoose.Schema({
    txCreationHash: String,
    creationBlock: Number,
    datetimeCreated: Date,
    uid: {
        type: String,
        unique: true,
        required: true,
        index: true
    },
    thing: String,
    type: String,
    name: String,
    name_uid: String,
    description: String,
    owner: String,
    creator: String,
    likes: Number,
    price_amount: String,
    price_hold: String,
    speed: Number,
    num_of_frames: Number,
    royalty_percent: Number,
    royalties_earned: String,
    num_of_owners: Number,
    stamps_used: Number,
    lastSaleDate: Date,
    lastUpdate: Date,
    blacklist: Boolean,
    tx_uid: String,
    last_likes_tx_uid: String
});

var likes = new mongoose.Schema({
    uid: {
        type: String,
        unique: true,
        required: true,
        index: true
    },
    liked_by: Array,
    last_likes_tx_uid: String
})

var likedByUser = new mongoose.Schema({
    vk: {
        type: String,
        unique: true,
        required: true,
        index: true
    },
    likes: Array,
    last_likes_tx_uid: String
})

var salesHistory = new mongoose.Schema({
    uid: {
        type: String,
        required: true,
        index: true
    },
    saleDate: Date,
    price: String,
    royaltyPaid: String,
    seller: String,
    buyer: String,
    wasHeld: Boolean,
    gift: Boolean,
    auction: Boolean
})

var processed = {
    loaderType: {
        type: String,
        unique: true,
        required: true,
        index: true
    },
    last_tx_uid_processed: String
}

var auctionHistory = new mongoose.Schema({
    uid: {
        type: String,
        required: true,
        index: true
    },
    created_date: Date,
    start_date: Date,
    scheduled_end_date: Date,
    ended: Boolean,
    actual_ended_date: {
        type: Date,
        required: false,
    },
    ended_early: Boolean,
    ended_early_date: Date,
    old_owner: String,
    new_owner: String,
    reserve_price: String,
    reserve_met: Boolean,
    winning_bid: String,
    bid_history: [Object],
    winner: String,
    paid_to_owner: String,
    paid_to_creator: String,
    royalty_percent: Number,
    creator: String,
    last_tx_uid: String
})

var shareLinks = new mongoose.Schema({
    uid: {
        type: String,
        required: true,
        index: true
    },
    owner: String,
    link: String,
    base64: String,
    dateCreated: Date
})

var authCodes = new mongoose.Schema({
    uid: {
        type: String,
        required: true,
        index: true
    },
    code: String,
    challenge: String,
    validated: Boolean,
    dateCreated: Date
})

var prices = new mongoose.Schema({
    symbol: {
        type: String,
        unique: true,
        required: true,
        index: true
    },
    currentPrice: Number,
    lastUpdated: Date
})

var stampRatio = new mongoose.Schema({
    symbol: String,
    currentRatio: Number,
    lastUpdated: Date
})

export default {
    Processed: mongoose.model('Processed', processed, 'processed'),
    Stamps: mongoose.model('Stamps', stamps, 'stamps'),
    PixelFrame: mongoose.model('PixelFrame', pixelFrame, 'pixelFrame'),
    Likes: mongoose.model('Likes', likes, 'likes'),
    LikedByUser: mongoose.model('LikedByUser', likedByUser, 'likedByUser'),
    SalesHistory: mongoose.model('SalesHistory', salesHistory, 'salesHistory'),
    ShareLinks: mongoose.model('ShareLinks', shareLinks, 'shareLinks'),
    AuthCodes: mongoose.model('AuthCodes', authCodes, 'authCodes'),
    Prices: mongoose.model('Prices', prices, 'prices'),
    StampRatio: mongoose.model('StampRatio', stampRatio, 'stampRatio'),
    AuctionHistory: mongoose.model('AuctionHistory', auctionHistory, 'auctionHistory')
};