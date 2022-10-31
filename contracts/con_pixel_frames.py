S = Hash(default_value='')

@export
def add_thing(thing_string: str, name: str, description: str, meta: dict, creator: str):

    #Enforce the thing requirements on the standard arguments
    enforce_thing_standards(thing_string, name, description, meta)

    # Create unique hash of the thing_string
    # Append any meta items required to make the string more unique, if necessary.
    uid = hashlib.sha256(thing_string)

    # Validate the string is unique
    assert not S[uid],  thing_string + ' already exists'

    # Create unique hash of the name,
    # to weed out similar names first convert to lowercase, then remove spaces
    names_uid = hashlib.sha256(name.lower().replace(" ", ""))

    # Validate the name is unique
    assert not S['names', names_uid],  'A form of this name already belongs to ' + S['names', names_uid]

    # Store the uid of the name
    S['names', names_uid] = uid

    # Run Custom formatting validations on your thing_string (length, content, etc.)
    custom_string_validations(thing_string, meta['num_of_frames'])

    # Required Values for Thing Compatibility
    S[uid] = ['thing', 'type', 'name', 'description', 'owner', 'creator', 'likes', 'price:amount', 'price:hold', 'meta_items']
    S[uid, 'thing'] = thing_string
    S[uid, 'type'] = 'text/plain'  # A mime/type or custom value that helps a 3rd party decode the thing_string.
    S[uid, 'name'] = name
    S[uid, 'description'] = description
    S[uid, 'owner'] = creator
    S[uid, 'creator'] = creator
    S[uid, 'likes'] = 0
    S[uid, 'price', 'amount'] = 0

    # Store some meta information about your Thing.
    # Meta Items defined here will be attached to your thing when returned from the block explorer.
    # Meta Items can also be appended to your thing_string before hashing, if they add to it's uniqueness.
    # Then they can be stored separately here for easy lookup later

    S[uid, 'meta_items'] = ['speed', 'num_of_frames', 'royalty_percent']
    S[uid, 'meta', 'speed'] = meta['speed']
    S[uid, 'meta', 'num_of_frames'] = meta['num_of_frames']
    S[uid, 'meta', 'royalty_percent'] = meta['royalty_percent']

    return uid

def enforce_thing_standards(thing_string: str, name: str, description: str, meta: dict):
    assert len(thing_string) > 0, "Thing string cannot be empty."

    assert len(name) > 0, "No Name provided."
    assert len(name) <= 25, "Name too long (25 chars max)."

    assert len(description) > 0, "No description provided."
    assert len(description) <= 128, "Description too long (128 chars max)."

    custom_meta_validations(meta)

def custom_string_validations(thing_string: str, num_of_frames: int):
    #Validate num_of_frames
    assert num_of_frames >= 1 and num_of_frames <= 8, "num_of_frames value " + str(num_of_frames) + " is out of range (1-8)."
    assert len(thing_string) % num_of_frames == 0, "num_of_frames value is invalid."

    #Validate Frames Data
    assert len(thing_string) / num_of_frames == 625, "Frames Data is Invalid, must be 625 pixels/frame."
    assertPixelValues(thing_string)

def assertPixelValues(thing_string):
    for pixel in thing_string:
        assert (ord(pixel) >= 65 and ord(pixel) <= 122) and ord(pixel) != 92, "Frames Data contains invalid pixel {}.".format(pixel)


def custom_meta_validations(meta):
    #Validate Speed
    assert 'speed' in meta, "Missing meta value 'speed' (int)."
    assert isinstance(meta['speed'], int), "Speed value is not an integer."
    assert meta['speed'] >= 100 and meta['speed'] <= 2000, "Speed value " + str(meta['speed']) + " is out of range (100ms-2000ms)."

    # Validate num_of_frames
    assert 'num_of_frames' in meta, "Missing meta value 'num_of_frames' (int)."
    assert isinstance(meta['num_of_frames'], int), "num_of_frames value is not an integer."

    # Validate royalty_ammount
    assert 'royalty_percent' in meta, "Missing meta value 'royalty_percent' (int)."
    assert isinstance(meta['royalty_percent'], int), "royalty_percent value is not an integer."
    assert meta['royalty_percent'] >= 0 and meta['royalty_percent'] <= 100, "royalty_percent value " + str(meta['royalty_percent']) + " is out of range (0-100)."

@export
def thing_exists(thing_string: str):
    uid = hashlib.sha256(thing_string)
    return S[uid]

@export
def get_owner(uid: str):
    return S[uid, 'owner']

@export
def get_creator(uid: str):
    return S[uid, 'creator']

@export
def set_price(uid: str, amount: float, hold: str):
    assert amount >= 0, 'Cannot set a negative price'
    S[uid, 'price', 'amount'] = amount

    if not hold == None:
        S[uid, 'price', 'hold'] = hold

@export
def get_price_amount(uid: str):
    return S[uid, 'price', 'amount']

@export
def get_royalty_amount(uid: str):
    return S[uid, 'meta', 'royalty_percent']

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

@export
def set_proof(uid: str, code: str):
    S[uid, 'proof'] = code
