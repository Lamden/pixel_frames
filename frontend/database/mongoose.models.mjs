import mongoose from 'mongoose';

var blocks = new mongoose.Schema({
  hash: String,
  blockNum: Number,
  rawBlock: String
});

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
    uid: String,
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
    blacklist: Boolean
});

var likes = new mongoose.Schema({
    uid: String,
    liked_by: Array
})

var likedByUser = new mongoose.Schema({
    vk: String,
    likes: Array
})

var salesHistory = new mongoose.Schema({
    uid: String,
    saleDate: Date,
    price: String,
    royaltyPaid: String,
    seller: String,
    buyer: String,
    wasHeld: Boolean,
    gift: Boolean,
    auction: Boolean
})

var blocksProcessed = {
    contractType: String,
    blockNum: Number
}

var currentAuctions = new mongoose.Schema({
    uid: String,
    end_date: Date,
    current_owner: String,
    reserve_price: String,
    current_bid: String,
    current_winner: String,
    royalty_percent: Number,
    creator: String,
    lastUpdate: Date
})

var auctionHistory = new mongoose.Schema({
    uid: String,
    scheduled_end_date: Date,
    end_triggered: Date,
    old_owner: String,
    new_owner: String,
    reserve_price: String,
    reserve_met: Boolean,
    winning_bid: String,
    winner: String,
    paid_to_owner: String,
    paid_to_creator: String,
    royalty_percent: Number,
    creator: String
})

var shareLinks = new mongoose.Schema({
    uid: String,
    owner: String,
    link: String,
    base64: String,
    dateCreated: Date
})

var authCodes = new mongoose.Schema({
    uid: String,
    code: String,
    challenge: String,
    validated: Boolean,
    dateCreated: Date
})

var prices = new mongoose.Schema({
    symbol: String,
    currentPrice: Number,
    lastUpdated: Date
})

var stampRatio = new mongoose.Schema({
    symbol: String,
    currentRatio: Number,
    lastUpdated: Date
})

var Blocks = mongoose.model('Blocks', blocks, 'blocks');
var BlocksProcessed = mongoose.model('BlocksProcessed', blocksProcessed, 'blocksProcessed');
var Stamps = mongoose.model('Stamps', stamps, 'stamps');
var PixelFrame = mongoose.model('PixelFrame', pixelFrame, 'pixelFrame');
var Likes = mongoose.model('Likes', likes, 'likes');
var LikedByUser = mongoose.model('LikedByUser', likedByUser, 'likedByUser');
var SalesHistory = mongoose.model('SalesHistory', salesHistory, 'salesHistory');
var CurrentAuctions = mongoose.model('CurrentAuctions', currentAuctions, 'currentAuctions');
var AuctionHistory = mongoose.model('AuctionHistory', auctionHistory, 'auctionHistory');
var ShareLinks = mongoose.model('ShareLinks', shareLinks, 'shareLinks');
var AuthCodes = mongoose.model('AuthCodes', authCodes, 'authCodes');
var Prices = mongoose.model('Prices', prices, 'prices');
var StampRatio = mongoose.model('StampRatio', stampRatio, 'stampRatio');

export default {
    Blocks,
    Stamps,
    PixelFrame,
    Likes, LikedByUser,
    SalesHistory,
    ShareLinks, AuthCodes,
    Prices,
    StampRatio,
    CurrentAuctions,
    AuctionHistory,
    BlocksProcessed
};