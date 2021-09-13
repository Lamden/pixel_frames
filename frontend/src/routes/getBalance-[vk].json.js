export async function get(req, res, next) {
	const { vk } = req.params;

    let results = await global.blockservice.getCurrentKeyValue('currency', 'balances', vk)

    let { value } = results

    if (!value) value = "0"
    if (value.__fixed__) value = value.__fixed__

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({value}));
}