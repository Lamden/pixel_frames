export async function get(req, res, next) {
	const { creator } = req.params;
	let things = await global.models.PixelFrame.find({creator})

	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify(things));

}