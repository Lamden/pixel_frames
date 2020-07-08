S = Hash(default_value='')

@export
def thing_exists(thing_string: str):
    uid = hashlib.sha256(thing_string)
    return S[uid]

@export
def add_thing(thing_string: str, description: str, owner: str, creator: str):
    uid = hashlib.sha256(thing_string)
    if not S[uid]:
        S[uid] = True
        S[uid, 'thing'] = thing_string
        S[uid, 'type'] = 'pixel information'
        S[uid, 'description'] = description
        S[uid, 'owner'] = owner
        S[uid, 'creator'] = creator
        S[uid, 'likes'] = 0
        S[uid, 'price', 'amount'] = 0

    return uid

@export
def get_owner(uid: str):
    return S[uid, 'owner']

@export
def set_price(uid: str, amount: int, hold: str):
    assert amount >= 0, 'Cannot set a negative price'
    S[uid, 'price', 'amount'] = amount

    if not hold == None:
        S[uid, 'price', 'hold'] = hold

@export
def get_price_amount(uid: str):
    return S[uid, 'price', 'amount']

@export
def get_price_hold(uid: str):
    return S[uid, 'price', 'hold']

@export
def set_owner(uid: str, owner: str):
    S[uid, 'owner'] = owner

@export
def like_thing(uid: str):
    likes = S[uid, 'likes']
    S[uid, 'likes'] = likes + 1