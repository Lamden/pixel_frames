export async function get(req, res) {
	let auctions = await global.db.models.AuctionHistory.find()

	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify({auctions}));
}
