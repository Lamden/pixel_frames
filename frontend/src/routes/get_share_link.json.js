export async function get(req, res, next) {
    res.setHeader('Content-Type', 'application/json');
    //console.log({query_getShareLink: req.query})
	const { uid, challenge } = req.query;

    let authCodeInfo = await global.models.AuthCodes.findOne({uid})
    //console.log({authCodeInfo_getShareLink: authCodeInfo, uid, challenge, date: new Date()})
    if (!authCodeInfo || !authCodeInfo.validated) {
        res.end(JSON.stringify({error: "Auth Code not valid."}));
        return
    }

    if (authCodeInfo.challenge === challenge){
        let thingInfo = await global.models.PixelFrame.findOne({uid})
        if (!thingInfo) res.end(JSON.stringify({error: "Thing doesn't exists."}));

        let shareLinkInfo = await global.models.ShareLinks.findOne({uid})
        if (!shareLinkInfo) {
            shareLinkInfo = await new global.models.ShareLinks({
                uid,
                owner: thingInfo.owner
            }).save()
        }
        shareLinkInfo.link = `share_${thingInfo.uid}_${global.randomHash().substring(0,10)}`
        shareLinkInfo.dateCreated = new Date()
        //console.log({shareLinkInfo})
        await shareLinkInfo.save()
        await authCodeInfo.remove()
        authCodeInfo = await global.models.AuthCodes.findOne({uid})
        if (authCodeInfo) throw new Error("authcodeinfo NOT deleted!")


        res.end(JSON.stringify({shareLink: shareLinkInfo.link}));
    }else{
        res.end(JSON.stringify({error: "Challenge not accepted."}));
    }
}