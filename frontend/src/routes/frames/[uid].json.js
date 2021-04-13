export async function get(req, res, next) {
	const { uid } = req.params;
	let thing = await global.models.PixelFrame.findOne({uid})
	console.log(thing)
	if (!thing) thing = null
	else {
		if (thing.blacklist) thing = null
	}
	console.log(thing)
	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify(thing));

}