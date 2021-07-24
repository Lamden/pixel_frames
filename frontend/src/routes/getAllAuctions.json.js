export async function get(req, res) {
	console.log("HERE")
	let auctions = await global.db.queries.getAllAuctions()
	console.log({auctions})

	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify({auctions}));
}
