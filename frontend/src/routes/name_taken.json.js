export async function get(req, res, next) {
	const { name_uid } = req.query;
	let thing = await global.db.models.PixelFrame.findOne({name_uid})

    res.setHeader('Content-Type', 'application/json');
	if (!thing) {
		res.end(JSON.stringify(false));
	}else{
		res.end(JSON.stringify(true));
	}
}