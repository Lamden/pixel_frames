import currency
I = importlib

# Import the Thing Info contract storage
Thing_Info = ForeignHash(foreign_contract='con_pixel_frames', foreign_name='S')

S = Hash(default_value=None)
metadata = Hash(default_value=0)


@construct
def seed():
    S['thing_master_contract'] = 'con_pixel_frames_master'
    # LST002
    metadata['operator'] = ctx.caller

# LST002
@export
def change_metadata(key: str, value: Any):
    assert ctx.caller == metadata['operator'], 'Only auction operator can set metadata!'
    metadata[key] = value

@export
def operator_transfer_thing(uid: str, new_owner: str):
    assert ctx.caller == metadata['operator'], 'Only auction operator can transfer things from contract.'
    thing_master_contract = I.import_module(S['thing_master_contract'])
    thing_master_contract.transfer(uid=uid, new_owner=new_owner)
    S[uid] = False

@export
def operator_transfer_currency(amount: str, to: float):
    assert ctx.caller == metadata['operator'], 'Only auction operator can transfer currency from contract.'
    currency.transfer(amount=amount, to=to)

def get_listing_info(uid: str):
    # Get listing info
    listing_info = S[uid]
    assert listing_info is not None, "Listing doesn't exist!"
    return {
        'start_date': S[uid, 'start_date'],
        'end_date': S[uid, 'end_date'],
        'current_owner': S[uid, 'current_owner'],
        'uid': S[uid, 'uid'],
        'reserve_price': S[uid, 'reserve_price'],
        'current_bid': S[uid, 'current_bid'],
        'current_winner': S[uid, 'current_winner'],
        'royalty_percent': S[uid, 'royalty_percent'],
        'creator': S[uid, 'creator']
    }

@export
def auction_thing(uid: str, reserve_price: float, start_date: datetime.datetime, end_date: datetime.datetime):
    # transfer thing to this auction contract
    # This will throw an Assertion error if caller does not own the thing and revert the tx
    thing_master_contract = I.import_module(S['thing_master_contract'])
    thing_master_contract.transfer_from(
        uid=uid,
        to=ctx.this,
        main_account=ctx.caller
    )

    assert not S[uid], 'Auction has already started!'
    assert end_date > now, "end_date is in the past"
    assert reserve_price >= 0, "reserve_price cannot be less than 0"

    S[uid, 'start_date'] = start_date
    S[uid, 'end_date'] = end_date
    S[uid, 'current_owner'] = ctx.caller
    S[uid, 'uid'] = uid
    S[uid, 'reserve_price'] = reserve_price
    S[uid, 'current_bid'] = None
    S[uid, 'current_winner'] = ""
    S[uid, "royalty_percent"] = Thing_Info[uid, 'meta', 'royalty_percent']
    S[uid, "creator"] = Thing_Info[uid, 'creator']
    
    # Mark as auction started
    S[uid] = True

@export
def end_auction(uid: str, end_early: bool):
    # Get listing info
    listing_info = get_listing_info(uid=uid)

    if end_early:
        # Only the owner or the operator can end an auction early
        assert listing_info['current_owner'] == ctx.caller or metadata['operator'] == ctx.caller, \
               'Only thing owner or auction operator can end the auction early!'

        if now < listing_info['start_date']:
            process_auction_result_no_winner(listing_info)
        else:
            if (listing_info['current_bid'] or -1) < listing_info['reserve_price']:
                process_auction_result_no_winner(listing_info)
            else:
                assert False, "Cannot end early. Auction started or reserve has been met."
    else:
        # Else, anyone can call this to complete the auction, assuming the auction is over
        assert now > listing_info['end_date'], 'Auction is still pending!'
        if listing_info['current_bid'] == None or listing_info['current_bid'] < listing_info['reserve_price']:
            process_auction_result_no_winner(listing_info)
        else:
            process_auction_result(listing_info)

def process_auction_result_no_winner(listing_info):
    thing_master_contract = I.import_module(S['thing_master_contract'])

    # Send thing back to owner
    thing_master_contract.transfer(
        uid=listing_info['uid'],
        new_owner=listing_info['current_owner']
    )

    # Send money back to last bidder (if there was one)
    if listing_info['current_winner'] != "":
        currency.transfer(
            to=listing_info['current_winner'],
            amount=listing_info['current_bid']
        )

    S[listing_info['uid']] = False

def process_auction_result(listing_info):
    thing_master_contract = I.import_module(S['thing_master_contract'])

    # transfer thing to new owner
    thing_master_contract.transfer(
        uid=listing_info['uid'],
        new_owner=listing_info['current_winner']
    )

    royalty_percent = listing_info['royalty_percent']

    if royalty_percent > 0:
        # calculate the royalty
        royalty_amount = listing_info['current_bid'] * (royalty_percent / 100)

        # calculate the amount that goes to the seller
        net_amount = listing_info['current_bid'] - royalty_amount

        # send royalty to creator
        currency.transfer(
            to=listing_info['creator'],
            amount=royalty_amount
        )
    else:
        net_amount = listing_info['current_bid']

    currency.transfer(
        to=listing_info['current_owner'],
        amount=net_amount
    )

    S[listing_info['uid']] = False

@export
def bid(uid: str, bid_amount: float):
    listing_info = get_listing_info(uid=uid)

    current_bid = listing_info['current_bid'] or 0

    assert now < listing_info['end_date'], "Auction has ended."
    assert now > listing_info['start_date'], "Auction has not stared."
    assert bid_amount > 0 , "Bid must be greater than zero."
    assert bid_amount > current_bid, f"Current bid of {current_bid} is higher!"

    # Take the currency bid from the bidder
    currency.transfer_from(
        main_account=ctx.caller,
        to=ctx.this,
        amount=bid_amount,
    )

    # Send the previous bidder's bid back to them
    if listing_info['current_winner'] != "":
        currency.transfer(
            to=listing_info['current_winner'],
            amount=listing_info['current_bid']
        )

    # Set the new bid info
    S[uid, 'current_bid'] = bid_amount
    S[uid, 'current_winner'] = ctx.caller
