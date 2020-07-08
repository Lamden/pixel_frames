import con_pixel_frames
import currency

S = Hash(default_value='')

@construct
def seed(name: str, description: str, icon_small: str, icon_large: str):
    print(icon_small)
    print(icon_large)
    S['name'] = name
    S['description'] = description
    S['icon_small'] = icon_small
    S['icon_large'] = icon_large

@export
def create_thing(thing_string: str, description: str):
    sender = ctx.caller
    assert not con_thing_info.thing_exists(thing_string),  thing_string + ' already exists'
    thing_uid = con_thing_info.add_thing(thing_string, description, sender, sender)
    return thing_uid

@export
def buy_thing(uid: str):
    owner = con_thing_info.get_owner(uid)
    sender = ctx.caller
    assert_already_owned(uid, sender)

    price_amount = con_thing_info.get_price_amount(uid)
    assert price_amount, uid + ' is not for sale'
    assert price_amount > 0, uid + ' is not for sale'

    price_hold = con_thing_info.get_price_hold(uid)
    if price_hold != '':
        assert sender == price_hold, 'this item is being held for ' + price_hold

    # currency.transfer_from(amount: float, to: str, main_account: str)
    currency.transfer_from(price_amount, owner, sender)

    # if the TAU transfer did not take place then this part will not execute as the whole method will fail
    transfer_ownership(uid, sender)

@export
def sell_thing(uid: str, amount: int):
    # make sure the caller owns the item
    assert_ownership(uid, ctx.caller)
    con_thing_info.set_price(uid, amount, '')

@export
def sell_thing_to(uid: str, amount: int, hold: str):
    # make sure the caller owns the item
    assert_ownership(uid, ctx.caller)
    con_thing_info.set_price(uid, amount, hold)

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
    con_thing_info.like_thing(uid)
    S['liked', uid, sender] = True

def assert_ownership(uid: str, sender):
    owner = con_thing_info.get_owner(uid)
    assert owner == sender, uid + ' not owned by ' + sender

def assert_already_owned(uid: str, sender):
    owner = con_thing_info.get_owner(uid)
    assert owner != sender, uid + ' already owned by ' + sender

def transfer_ownership(uid:str, new_owner: str):
    #change ownership to new owner
    con_thing_info.set_owner(uid, new_owner)

    # if item was for sale make it no longer for sale
    if con_thing_info.get_price_amount(uid) > 0:
        con_thing_info.set_price(uid, 0, '')