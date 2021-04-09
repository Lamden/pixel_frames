export async function get(req, res, next) {
	const { uid } = req.query;

    let authCodeInfo = await global.models.AuthCodes.findOne({uid})
    if (!authCodeInfo) {
        authCodeInfo = await new global.models.AuthCodes({
            uid,
            code: global.randomHash(),
            challenge: global.randomHash(),
            validated: false,
            dateCreated: new Date()
        }).save()
    }

    //console.log({authCodeInfo_getCode: authCodeInfo, date: new Date()})

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(authCodeInfo));
}