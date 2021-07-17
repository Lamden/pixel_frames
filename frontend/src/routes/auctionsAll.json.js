export async function get(req, res) {
	let { limit, offset } = req.query;
	limit = parseInt(limit) || 25

	let auctionsRes = await global.db.queries.getAllActiveAuctions(limit, offset)
	let auctions = auctionsRes[0]
	auctions.data = await global.db.queries.populateThingInfo(auctions.data)

	console.log({data: auctions.data})

	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify({data: auctions.data, count: auctions.count.length}));
}
