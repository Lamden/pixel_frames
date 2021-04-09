export async function get(req, res, next) {
	let { account } = req.params;
	let { limit, offset } = req.query;

	limit = parseInt(limit) || 25

	var match = { $match : {owner: account}}
	var sort = { $sort : {"lastUpdate" : -1.0}}
	var skip = { $skip: parseInt(offset) }
	var reclimit = { $limit: limit}
	let dataPipeline = []
	let countPipeline = [match]
	if (offset) {
		dataPipeline = [match, sort, skip, reclimit]
	}
	else dataPipeline = [match, sort, reclimit]
	let facet = { $facet: {data: dataPipeline, "count": countPipeline}}
	let collation = { locale : "en_US", numericOrdering : true }

	let things = await global.models.PixelFrame
		.aggregate([facet])
		.collation(collation)

	res.setHeader('Content-Type', 'application/json');
	res.end(JSON.stringify({data: things[0].data, count: things[0].count.length}));
}