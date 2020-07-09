import con_pixel_frames
import currency

S = Hash(default_value='')

@construct
def seed(name: str, description: str, icon_svg_base64: str):
    # Enforce the Thing Requirements for submitting a thing contract
    assert len(name) > 0, "A thing contracts needs a name value."
    assert len(description) > 0, "A thing contracts needs a description value."

    # Icons are svg files that have been encoded to a base64 string.
    # See https://base64.guru/converter/encode/image/svg for details.
    # NOTE: the value xmlns="http://www.w3.org/2000/svg" is a REQUIRED property in your <svg> tag.
    assert len(icon_svg_base64) > 0, "A thing contracts needs a an icon value (base64 encoded svg)."

    S['name'] = name
    S['description'] = description
    S['icon_svg'] = icon_svg_base64

@export
def create_thing(thing_string: str, name: str, description: str, meta: dict = {}):
    sender = ctx.caller
    thing_uid = con_pixel_frames.add_thing(thing_string, name, description, meta, sender)
    return thing_uid

@export
def buy_thing(uid: str):
    owner = con_pixel_frames.get_owner(uid)
    sender = ctx.caller
    assert_already_owned(uid, sender)

    price_amount = con_pixel_frames.get_price_amount(uid)
    assert price_amount, uid + ' is not for sale'
    assert price_amount > 0, uid + ' is not for sale'

    price_hold = con_pixel_frames.get_price_hold(uid)
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
    con_pixel_frames.set_price(uid, amount, '')

@export
def sell_thing_to(uid: str, amount: int, hold: str):
    # make sure the caller owns the item
    assert_ownership(uid, ctx.caller)
    con_pixel_frames.set_price(uid, amount, hold)

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
    con_pixel_frames.like_thing(uid)
    S['liked', uid, sender] = True

@export
def prove_ownership(uid: str, code: str):
    sender = ctx.caller
    assert_ownership(uid, sender)
    con_pixel_frames.set_proof(uid, code)

def assert_ownership(uid: str, sender):
    owner = con_pixel_frames.get_owner(uid)
    assert owner == sender, uid + ' not owned by ' + sender

def assert_already_owned(uid: str, sender):
    owner = con_pixel_frames.get_owner(uid)
    assert owner != sender, uid + ' already owned by ' + sender

def transfer_ownership(uid:str, new_owner: str):
    #change ownership to new owner
    con_pixel_frames.set_owner(uid, new_owner)

    # if item was for sale make it no longer for sale
    if con_pixel_frames.get_price_amount(uid) > 0:
        con_pixel_frames.set_price(uid, 0, '')