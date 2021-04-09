export async function get(req, res, next) {
	const { uid } = req.params;
	const { account } = req.query;

	let likes = await global.models.Likes.findOne({uid})
    res.setHeader('Content-Type', 'application/json');

	if (!likes) {
		res.end(JSON.stringify(false));
		return
	}
    if (likes.liked_by.includes(account)) res.end(JSON.stringify(true));
    else res.end(JSON.stringify(false));
}