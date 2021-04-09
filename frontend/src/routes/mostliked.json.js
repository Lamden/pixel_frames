export async function get(req, res, next) {
	let { limit } = req.query;
	limit = parseInt(limit) || 25

	let things = await global.models.PixelFrame.find({})
		.sort({likes: -1})
		.limit(limit)

	//console.log({liked: things})
	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify(things));

}