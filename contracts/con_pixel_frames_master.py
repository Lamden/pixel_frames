import currency
I = importlib

S = Hash(default_value='')
balances = Hash(default_value=0)
metadata = Hash(default_value=0)


@construct
def seed():
    S['thing_info_contract'] = 'con_pixel_frames'

    # LST002
    metadata['operator'] = ctx.caller
    metadata['things_name'] = 'Pixel Frames Test 2'
    metadata['things_description'] = 'Create, Own and Sell unique pixel animations on the Lamden Blockchain!'

# LST002
@export
def change_metadata(key: str, value: Any):
    assert ctx.caller == metadata['operator'], 'Only operator can set metadata!'
    metadata[key] = value

@export
def create_thing(thing_string: str, name: str, description: str, meta: dict = {}):
    thing_info = I.import_module(S['thing_info_contract'])
    sender = ctx.caller
    thing_uid = thing_info.add_thing(thing_string, name, description, meta, sender)
    add_to_balance(sender)
    return thing_uid

@export
def buy_thing(uid: str):
    thing_info = I.import_module(S['thing_info_contract'])
    sender = ctx.caller

    owner = thing_info.get_owner(uid)
    creator = thing_info.get_creator(uid)

    assert_already_owned(uid, sender)

    price_amount = thing_info.get_price_amount(uid)
    royalty_percent = thing_info.get_royalty_amount(uid)
    assert price_amount, uid + ' is not for sale'
    assert price_amount > 0, uid + ' is not for sale'

    price_hold = thing_info.get_price_hold(uid)
    if price_hold != '':
        assert sender == price_hold, uid + ' is being held for ' + price_hold

    if royalty_percent > 0:
        # calculate the royalty
        royalty_amount = price_amount * (royalty_percent / 100)
        # calculate the amount that goes to the seller
        net_amount = price_amount - royalty_amount
        # send royalty to creator
        currency.transfer_from(royalty_amount, creator, sender)
    else:
        net_amount = price_amount

    # send currency to current owner
    currency.transfer_from(net_amount, owner, sender)

    # if the TAU transfers did not take place then this part will not execute as the whole method will fail
    transfer_ownership(uid, sender)

@export
def sell_thing(uid: str, amount: int):
    # make sure the caller owns the item
    assert_ownership(uid, ctx.caller)
    thing_info = I.import_module(S['thing_info_contract'])
    thing_info.set_price(uid, amount, '')

@export
def sell_thing_to(uid: str, amount: int, hold: str):
    # make sure the caller owns the item
    assert_ownership(uid, ctx.caller)

    thing_info = I.import_module(S['thing_info_contract'])
    thing_info.set_price(uid, amount, hold)

@export
def give_thing(uid: str, new_owner: str):
    sender = ctx.caller
    # make sure the caller owns the item
    assert_ownership(uid, sender)
    assert_already_owned(uid, new_owner)
    transfer_ownership(uid, new_owner)

@export
def like_thing(uid: str):
    sender = ctx.caller
    assert S['liked', uid, sender] == '', sender + " already liked " + uid

    thing_info = I.import_module(S['thing_info_contract'])
    thing_info.like_thing(uid)

    S['liked', uid, sender] = True

@export
def prove_ownership(uid: str, code: str):
    sender = ctx.caller
    assert_ownership(uid, sender)

    thing_info = I.import_module(S['thing_info_contract'])
    thing_info.set_proof(uid, code)

def assert_ownership(uid: str, sender):
    thing_info = I.import_module(S['thing_info_contract'])
    owner = thing_info.get_owner(uid)
    assert owner == sender, uid + ' not owned by ' + sender

def assert_already_owned(uid: str, sender):
    thing_info = I.import_module(S['thing_info_contract'])
    owner = thing_info.get_owner(uid)
    assert owner != sender, uid + ' already owned by ' + sender

def transfer_ownership(uid:str, new_owner: str):
    thing_info = I.import_module(S['thing_info_contract'])
    old_owner = thing_info.get_owner(uid)
    #change ownership to new owner
    thing_info.set_owner(uid, new_owner)

    # if item was for sale make it no longer for sale
    if thing_info.get_price_amount(uid) > 0:
        thing_info.set_price(uid, 0, '')

    #adjust balances
    add_to_balance(new_owner)
    subtract_from_balance(old_owner)

def add_to_balance(holder: str):
    if balances[holder] is None:
        balances[holder] = 1
    else:
        balances[holder] = balances[holder] + 1

def subtract_from_balance(holder: str):
    if balances[holder] is None:
        balances[holder] = 0
    else:
        balances[holder] = balances[holder] - 1