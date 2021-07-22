export async function get(req, res, next) {
	const { contractName, variableName, key } = req.params;
	let result = await global.blockservice.getCurrentKeyValue(contractName, variableName, key)
    res.end(JSON.stringify(result));
}