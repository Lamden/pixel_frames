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
    lastUpdate: Date
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
    gift: Boolean
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

var Blocks = mongoose.model('Blocks', blocks, 'blocks');
var Stamps = mongoose.model('Stamps', stamps, 'stamps');
var PixelFrame = mongoose.model('PixelFrame', pixelFrame, 'pixelFrame');
var Likes = mongoose.model('Likes', likes, 'likes');
var LikedByUser = mongoose.model('LikedByUser', likedByUser, 'likedByUser');
var SalesHistory = mongoose.model('SalesHistory', salesHistory, 'salesHistory');
var ShareLinks = mongoose.model('ShareLinks', shareLinks, 'shareLinks');
var AuthCodes = mongoose.model('AuthCodes', authCodes, 'authCodes');
var Prices = mongoose.model('Prices', prices, 'prices');

export default {
    Blocks,
    Stamps,
    PixelFrame,
    Likes, LikedByUser,
    SalesHistory,
    ShareLinks, AuthCodes,
    Prices
};