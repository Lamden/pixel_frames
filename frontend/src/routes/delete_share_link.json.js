import fs from 'fs'
import path from 'path';

export async function get(req, res, next) {
    res.setHeader('Content-Type', 'application/json');
    console.log({query_deleteLink: req.query})
	const { uid, challenge } = req.query;

    let authCodeInfo = await global.models.AuthCodes.findOne({uid})
    console.log({authCodeInfo_deleteLink: authCodeInfo, uid, challenge, date: new Date()})
    if (!authCodeInfo || !authCodeInfo.validated) {
        res.end(JSON.stringify({error: "Auth Code not valid."}));
        return
    }

    if (authCodeInfo.challenge === challenge){
        let shareLinkInfo = await global.models.ShareLinks.findOne({uid})
        const shareLink = shareLinkInfo.link

        if (!shareLinkInfo) res.end(JSON.stringify({deleted: true, shareLink: null}));

        await shareLinkInfo.remove()
        await authCodeInfo.remove()

        shareLinkInfo = await global.models.ShareLinks.findOne({uid})

        if (shareLinkInfo) {
            res.end(JSON.stringify({error: "Code was not deleted!"}));
        }else{
            if(fs.existsSync(`./GIFS/${shareLink}.gif`)) fs.unlinkSync(`./GIFS/${shareLink}.gif`)
            res.end(JSON.stringify({deleted: true, shareLink: null}));
        }
    }else{
        res.end(JSON.stringify({error: "Challenge not accepted."}));
    }
}