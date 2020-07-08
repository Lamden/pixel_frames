# server/contracting_server.py

from sanic import Sanic, response
from sanic_cors import CORS
import ast
import json

from contracting.db.encoder import encode
from contracting.client import ContractingClient
client = ContractingClient()

with open('tests/currency.py') as f:
    code = f.read()
    client.submit(code, name='currency')

with open('contracts/con_pixel_frames.py') as f:
    code = f.read()
    client.submit(code, name='con_pixel_frames', owner='con_pixel_frames_master')

with open('server/images.json') as json_file:
    base64_images = json.loads(json_file.read())
    with open('contracts/con_pixel_frames_master.py') as f:
        code = f.read()
        client.submit(
            code,
            name='con_pixel_frames_master',
            constructor_args={
                'name': "Pixel Frames",
                'description': 'Unique Pixel Animations you can make, sell and collect!',
                'icon_small': base64_images['small'],
                'icon_large': base64_images['large']
            }
        )

app = Sanic("contracting server")
CORS(app)

# Make sure the server is online
@app.route("/ping")
async def ping(request):
    return response.json({'status': 'online'})

# Get all Contracts in State (list of names)
@app.route("/contracts")
async def get_contracts(request):
    contracts = client.get_contracts()
    return response.json({'contracts': contracts})

@app.route("/contracts/<contract>")
# Get the source code of a specific contract
async def get_contract(request, contract):
    # Use the client raw_driver to get the contract code from the db
    contract_code = client.raw_driver.get_contract(contract)

    # Return an error response if the code does not exist
    if contract_code is None:
        return response.json({'error': '{} does not exist'.format(contract)}, status=404)

    funcs = []
    variables = []
    hashes = []

    # Parse the code into a walkable tree
    tree = ast.parse(contract_code)

    # Parse out all functions
    function_defs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    for definition in function_defs:
        func_name = definition.name
        kwargs = [arg.arg for arg in definition.args.args]

        funcs.append({'name': func_name, 'arguments': kwargs})

    # Parse out all defined state Variables and Hashes
    assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)]
    for assign in assigns:
        if type(assign.value) == ast.Call:
            if assign.value.func.id == 'Variable':
                variables.append(assign.targets[0].id.lstrip('__'))
            elif assign.value.func.id == 'Hash':
                hashes.append(assign.targets[0].id.lstrip('__'))

    #Return all Information
    return response.json({
        'name': contract,
        'code': contract_code,
        'methods': funcs,
        'variables': variables,
        'hashes': hashes
    }, status=200)

# Return the current state of a variable
@app.route("/contracts/<contract>/<variable>")
async def get_variable(request, contract, variable):
    # Check if contract exists. If not, return error
    contract_code = client.raw_driver.get_contract(contract)
    if contract_code is None:
        return response.json({'error': '{} does not exist'.format(contract)}, status=404)
    # Parse key from request object
    key = request.args.get('key')
    if key is not None:
        key = key.split(',')

    # Create the key contracting will use to get the value
    k = client.raw_driver.make_key(contract=contract, variable=variable, args=key)

    # Get value
    value = client.raw_driver.get(k)

    # If the variable or the value didn't exists return None
    if value is None:
        return response.json({'value': None}, status=404)

    # If there was a value, return it formatted
    return response.json({'value': value}, status=200, dumps=encode)

@app.route("/", methods=["POST",])
async def submit_transaction(request):
    # Get transaction details
    contract_name = request.json.get('contract')
    method_name = request.json.get('method')
    kwargs = request.json.get('args')
    sender = request.json.get('sender')

    # Set the sender
    client.signer = sender

    # Get reference to contract
    contract = client.get_contract(contract_name)

    # Return error of contract does not exist
    if contract_name is None:
        return response.json({'error': '{} does not exist'.format(contract)}, status=404)

    # Get reference to the contract method to be called
    method = getattr(contract, method_name)

    # Call method with supplied arguments and return status
    try:
        method(**kwargs)
        return response.json({'status': 0})
    except Exception as err:
        return response.json({'status': 1, 'error': str(err)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3737)