#tests/test_auction.py
import unittest
from datetime import datetime, timedelta
import time
from contracting.stdlib.bridge.time import Datetime
from contracting.client import ContractingClient

frames_good_1 = ("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjjjPPPnnnnnnnnnnnnnUUjjUjjPPjjjPPPPnnnnnnnnjjjnyyyPyyyPjjPjPPPnnnnnnjjjyPPPPPPPPyjPjPPPPnnnnnnjjPPPPPPPPPPPjyPPPPnnnnUUUjjPPPPPyyyyjjyyPPPnnnUUUUyjjjPyPUUUjyjyyPPPnnnUUUUjPjjyyPUjjUUjyPPPPnnnUUUjjjjjjjPnjnyynjnnnnnnnnnnjPyyPjPjPPynnnnjnnnnnnnnnjnPPyjjjPyPPPPPjnnnnnnnnjnnPPjjyyjjPPPPPjnnnnnnnnjnUPjjjPyyjjPPPPjPnnnnnnnjUUjjPPPPPjjjPPjPPnnnnnnUjjUjjjPPPPPjyPjjPPnnnnUUUUjUjjPPPPPPPjjjPPPnnnnUUUUjUjjPPPPPPPPyjPPPnnnnUUUUjjPjyyPPPPPPyPjjPnnnnUUUUjUUjjPyyPPPyPPPnnnnnnUUUUUjUnjPPPyyyyPPPnnnjnnnnnnnnnnjjPPPPPPPPnnjjnnnnnnnnnnnnjjjjjjjjjjjnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
                 "nnnnnnnnnnnnnnnnnnnnnnnnnnnZZZZZZnZZjZZZZZnnnnnnnnnnnZZZZZZjZZZjjjPZZZZnnnnnnnjZZZZyyPyyZPZZZZZZZnnnnnnjjjyZZPPPPPPyjZZPPZPnnnnnnjjPPZZPPPPZZZjyPZPPnnnnUUUjjPPZZPZZyyjjyyZPPnnnUUUUyjjZZZZUUUjyjyyZPPnnnUUZUjZZjyyZUjjUUjyPZPPnnnUUZZZZjjjjZnjnyynjZnnnnnnnnnZZyyPjPjZPynnnnjnnnnnnnnnZnZPyjjjZyPPPPPZnnnnnnnnjZZZZZZyZZZZZZZZZZnnnnnnnjnUPjZjPyZjjPPPPZZnnnnnnnjUUjjZZPPZjjjPZZZZZnnnnnUjjUjjjZZZZZZZZZjPPZnnnUUUUjUZZZZZZPPPjjjPPPZZnnUUUUjZZZZPPPZZPPyjPPPnZnnUUUUZZZZyyPPPPZPZPjjPZZnnUUUUZZUjjPyyPPPyZZZZZZnnnUUUZZZZZZZZZZZZZZZZnZnjnnnnnZZnnZZZZZPPPPPPZZjjnnnnnnnnnnnnjjjjZZZjjjZZnnnnnnnnnnnnnnnnnnnnZZZnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")

frames_good_2 = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBzzYBBBBBBBzzzzYBzzzzBzzzzzzBBBBBBBzzBYzzzzzzzYYBBzBYBBBBBBBzYBBzzzYYYYYYYzBYYBBBBBBBzYYzzYYBBBBBzBYYBYBBBBBBBYzYzBBYBBBBBBBYYBYYBBBBBBYzzzBBBYBBBzBBYYBBYBBBBBBYzzzzYBBYBzzBBYYBzYBBBBBBBzYBYBBBBYBBzzYBzzBYBBBBBBzYYBzzBBBBBYYYBBBzzBBBBBBBYYBYBzBBBYYBBzBBBYBzBBBBzzYBBYBBzzYYzBBBBBYBBzBBBBYzYBYYBBYzzBBBBBBYBBzBBBzYBzzYzzYzzYBBBBBBYBBzBBBzYYBBYYYYBzBYBBBBBYBzBBBBBYBBBBBBBBzYBYBBBBYzBBBBBzzYYBBBBBzBBYYYYYzzBBBBBBBzBYYYYBzBBBYYBYBzBBBBBBBBBzzzzzYYYBYBBBYBzBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiizzYiiiiiiizzzzYizzzzizzzzzzBiiiiiizzBYzzzzzzzYYBBzBYBiiiiiizYBBzzzYYYYYYYzBYYBiiiiiizYYzzYYBBBBBzBYYBYBiiiiiiYzYzBBYBBBBBBBYYBYYiiiiiiYzzzBBBYBBBzBBYYBBYiiiiiiYzzzzYBBYBzzBBYYBzYiiiiiiizYBYBBBBYBBzzYBzzBYiiiiiizYYBzzBBBBBYYYBBBzziiiiiiBYYBYBzBBBYYBBzBBBYiziiiizzYBBYBBzzYYzBBBBBYiBziiiBYzYBYYBBYzzBBBBBBYiBziiizYBzzYzzYzzYBBBBBBYiBziiizYYBBYYYYBzBYBBBBBYiziiiiBYBBBBBBBBzYBYBBBBYziiiiizzYYBBBBBziBYYYYYzziiiiiiizBYYYYBziiBYYBYiziiiiiiiiizzzzzYYYiYBBBYiziiiiiiiiiiiiiiiiiiYYYYYiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOzzYOOOOOOOzzzzYOzzzzOzzzzzzBOOOOOOzzBYzzzzzzzYYBBzBYBOOOOOOzYBBzzzYYYYYYYzBYYBOOOOOOzYYzzYYOOOOOzBYYBYBOOOOOOYzYzBBYOOOOOBBYYBYYOOOOOOYzzzBBBYOOOzBBYYBBYOOOOOOYzzzzYBBYOzzBBYYBzYOOOOOOOzYBYBBBBYBBzzYBzzBYOOOOOOzYYBzzBBBBBYYYBOOzzOOOOOOBYYBYBzBBBYYBOzOOOYOzOOOOzzYBBYBBzzYYzOOOOOYOBzOOOBYzYBYYBBYzzOOOOOOYOBzOOOzYBzzYzzYzzYOOOOOOYOBzOOOzYYOOYYYYOzBYOOOOOYOzOOOOBYOOOOOOOOzYBYOOOOYzOOOOOzzYYOOOOOzOBYYYYYzzOOOOOOOzBYYYYOzOOBYYBYOzOOOOOOOOOzzzzzYYYOYBBBYOzOOOOOOOOOOOOOOOOOOYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOiiiiiiiiOOOOOOOOOOOOOOOOiiiiiiiiiizzYOOOOOOOzOOOYiiiiiiiiiizzOOOOOOOzOBYziiiiiiiiiiiBOBOOOOOOzOiiiiiiiiiiiiiiYYBOiiOOOOiiiiiiiiiiiiiiiiYBOiOOOOiiiiiiiiiiiiiiiiiYiOOOOOiiiiiiiiiiiiiiiiiiBYOOOOiiiiiiiiiiiiiiiiiiiiYOOOOiiiiiiiiiiiiOBiiiiiiBYOOOiiiiiiiiiBBBOBiiiiiizzOOOiiiiiiiiiOBBBYiiiiiiOYOzOiiiiiiiiOiBzzOiiiiiiOYOBziiiiiiiiiiBBiziiiiiOOYOBziiiiiiiiiiiYzzOOOiOOOYOBziiiiiiiiiiiiizBOOOOOOiOzOiiiiiiiiiiiiizYBOOOiOizOOOiiiiiiiiiiiiiiYYYYYiiiOOOiiiiiiiiiiiiiiYYBYOzOOOOOOOiiiiiiiiiiiiBBBYOzOOOOOOOOOiiiiiiiiiiYYYYOOOOOOOOOOOOOiiiiiiiiOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    "ZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZiiiiZZZZZZZZZZZZZZZZZZZZZiiiiiiiiZZZZZZZZZZZZZZZZZiiiiiiiiZZZZZZZZZZZZZZZZZZiiiiiiiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZZiiiBBBZZZZZZZZZZZZZZZZZZZiiiOBBBZZZZZZZZZZZZZZZZZZZiOiZZZZZZZZZZZZZZZiZZZZZZZZZZZZZZZZZiZZZZZZiZZZZZZZZZZZZZZZZZOZZZZZZiiZZZZZZZZZZZZZOOOOZZZZZZiZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOOOOZZZZZZZZZZZZZZZZZZZOO"
    "YYYYYYYYYYYYYYGGGGGZZYYYOYYYYYYYYYYYGGGGGGGGGZYYYOYYGGGGGYYYGGGGGGGGGGZYYYYYYGGGGGYYYGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGZZYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGiZGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUUYYYGGGGGGGGGGGGGGGGGGGUUUYYYiYYYGGGGGGGGGGGGGGGUUUYYYiYYYGGGGGGGGGYGGGGGUUUUYYiiYYYGGGGGGGGYGGGGGUUUUYYiYYYYGGGGGGGGYGGGGGUUUUYYOYYYYGGGGGGGGYGGGGGUUUUYYOYYYYGGGGGGGGYYYYYGUUUUYYOYYYYYYYGGGGGYYYYYYYYYYYYOYYYYYYYGGGGGYYYYYYYYYYYYOYYYYYYYYYYYYYYYYYYYYYYYYOYYYYYYYYYYYYYYYYYYYYYYYYOOOOYYYYYYYYYYYYYYYYYYYOO"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
)

frames_good_3 = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
)

new_thing_1_uid = "20e2c4baf4fce1cc17e386ead27d62342ea3cf261ccae029b7d2307d43940a28"
new_thing_2_uid = "58ab8c72c2238a874baaa9d9faa988605df738d348932f054ce0d0adf1e7dab3"


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.current_date = datetime.now()
        self.environment_current_date = {'now': Datetime(
            self.current_date.year,
            self.current_date.month,
            self.current_date.day,
            self.current_date.hour,
            self.current_date.minute,
            self.current_date.second
        )}

        self.c = ContractingClient(signer='jeff', environment=self.environment_current_date)
        self.c.flush()

        start_date = self.current_date + timedelta(seconds=-10)
        self.start_date = Datetime(
            start_date.year,
            start_date.month,
            start_date.day,
            start_date.hour,
            start_date.minute,
            start_date.second
        )

        end_date = self.current_date + timedelta(days=1)
        self.end_date = Datetime(
            end_date.year,
            end_date.month,
            end_date.day,
            end_date.hour,
            end_date.minute,
            end_date.second
        )

        with open('./currency.py') as f:
            code = f.read()
            self.c.submit(code, name='currency')
        with open('../contracts/con_pixel_frames.py') as f:
            code = f.read()
            self.c.submit(code, name='con_pixel_frames', owner="con_pixel_frames_master")
        with open('../contracts/con_pixel_frames_master.py') as f:
            code = f.read()
            self.c.submit(
                code,
                name='con_pixel_frames_master'
            )
        with open('../contracts/con_pixel_frames_auction.py') as f:
            code = f.read()
            self.c.submit(
                code,
                name='con_pixel_frames_auction'
            )

        self.con_pixel_frames_auction = self.c.get_contract('con_pixel_frames_auction')
        self.con_pixel_frames_master = self.c.get_contract('con_pixel_frames_master')
        self.con_pixel_frames = self.c.get_contract('con_pixel_frames')
        self.currency_contract = self.c.get_contract('currency')

        self.new_thing_1_uid = self.con_pixel_frames_master.create_thing(
            thing_string=frames_good_1,
            name="Test1",
            description="Test1 Pixel Frame",
            meta={
                'speed': 256,
                'num_of_frames': 2,
                'royalty_percent': 20
            }
        )

        self.new_thing_2_uid = self.con_pixel_frames_master.create_thing(
            thing_string=frames_good_2,
            name="Test2",
            description="Test2 Pixel Frame",
            meta={
                'speed': 256,
                'num_of_frames': 8,
                'royalty_percent': 0
            }
        )

        self.new_thing_3_uid = self.con_pixel_frames_master.create_thing(
            thing_string=frames_good_3,
            name="Test3",
            description="Test3 Pixel Frame",
            meta={
                'speed': 256,
                'num_of_frames': 2,
                'royalty_percent': 15
            },
            signer='stu'
        )

    def tearDown(self):
        self.c.flush()

    def approve_auction(self, uid, signer='jeff'):
        self.con_pixel_frames_master.approve(
            uid=uid,
            to=self.con_pixel_frames_auction.name,
            signer=signer
        )

    def approve_currency(self, to, amount, signer):
        self.currency_contract.approve(
            amount=amount,
            to=to,
            signer=signer
        )

    def get_currency_balance(self, who):
        return self.currency_contract.quick_read('balances', who)

    def get_royalty_percent(self, uid):
        return self.con_pixel_frames.quick_read('S', f'{uid}:meta:royalty_percent')

    def start_auction(self, uid, reserve_price, end_date=None, start_date=None, signer='jeff'):
        if start_date is None:
            start_date = self.start_date
        else:
            start_date = Datetime(
                    start_date.year,
                    start_date.month,
                    start_date.day,
                    start_date.hour,
                    start_date.minute,
                    start_date.second
                )

        if end_date is None:
            end_date = self.end_date
        else:
            end_date = Datetime(
                    end_date.year,
                    end_date.month,
                    end_date.day,
                    end_date.hour,
                    end_date.minute,
                    end_date.second
                )

        self.approve_auction(uid, signer)
        self.con_pixel_frames_auction.auction_thing(
            uid=uid,
            reserve_price=reserve_price,
            start_date=start_date,
            end_date=end_date,
            signer=signer
        )

    def make_bid(self, uid, bid_amount, bid_datetime=None, signer='jeff'):
        if bid_datetime is not None:
            self.con_pixel_frames_auction.environment = {
                'now': Datetime(
                    bid_datetime.year,
                    bid_datetime.month,
                    bid_datetime.day,
                    bid_datetime.hour,
                    bid_datetime.minute,
                    bid_datetime.second
                )
            }

        self.approve_currency(
            to=self.con_pixel_frames_auction.name,
            amount=bid_amount,
            signer=signer
        )

        self.con_pixel_frames_auction.bid(
            uid=uid,
            bid_amount=bid_amount,
            signer=signer
        )

    def end_auction(self, uid, end_early=False, end_auction_datetime=None, signer='jeff'):
        if end_auction_datetime is not None:
            self.con_pixel_frames_auction.environment = {
                'now': Datetime(
                        end_auction_datetime.year,
                        end_auction_datetime.month,
                        end_auction_datetime.day,
                        end_auction_datetime.hour,
                        end_auction_datetime.minute,
                        end_auction_datetime.second
                )
            }

        self.con_pixel_frames_auction.end_auction(
            uid=uid,
            end_early=end_early,
            signer=signer
        )

    def test_auction_thing(self):
        print("TEST AUCTION A THING")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=50.5

        )

        self.assertEqual(
            self.con_pixel_frames_auction.name,
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_owner'),
            'jeff'
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:end_date'),
            self.end_date
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:uid'),
            self.new_thing_1_uid
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            None
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_winner'),
            ""
        )

    def test_auction_thing_neg_no_approval(self):
        print("TEST NO APPROVAL GIVEN")

        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_auction.auction_thing(
                uid=self.new_thing_1_uid,
                reserve_price=50.5,
            )
        self.assertEqual(
            'You have not been given approval to transfer this user\'s item.',
            str(cm.exception)
        )
        self.assertEqual(
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
            'jeff'
        )

    def test_auction_thing_neg_not_owner_no_approval(self):
        print("TEST NOT OWNER OF THING AND NO APPROVAL BY OWNER")

        with self.assertRaises(AssertionError) as cm:
            self.start_auction(
                uid=self.new_thing_1_uid,
                reserve_price=50.5,
                signer='stu'
            )

        self.assertEqual(
            f'{self.new_thing_1_uid} not owned by stu',
            str(cm.exception)
        )

    def test_auction_thing_neg_not_owner_has_approval(self):
        print("TEST NOT OWNER OF THING AND OWNER SENT APPROVAL FOR CONTRACT")
        self.approve_auction(self.new_thing_1_uid)


        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_auction.auction_thing(
                uid=self.new_thing_1_uid,
                reserve_price=50.5,
                signer='stu'
            )

        self.assertEqual(
            f'You have not been given approval to transfer this user\'s item.',
            str(cm.exception)
        )

    def test_auction_thing_neg_end_date_past(self):
        print("TEST END DATE IS IN THE PAST")

        with self.assertRaises(AssertionError) as cm:
            self.start_auction(
                uid=self.new_thing_1_uid,
                reserve_price=50.5,
                end_date=Datetime(2021, 1, 1, 1, 1, 1)
            )

        self.assertEqual(
            'end_date is in the past',
            str(cm.exception)
        )

    def test_auction_reserve_date_less_than_zero(self):
        print("TEST RESERVE DATE LESS THAN ZERO")

        with self.assertRaises(AssertionError) as cm:
            self.start_auction(
                uid=self.new_thing_1_uid,
                reserve_price=-0.1
            )

        self.assertEqual(
            'reserve_price cannot be less than 0',
            str(cm.exception)
        )

    def test_bid(self):
        print("TEST BID ON THING")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            10
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_winner'),
            'stu'
        )

    def test_bid_accept_higher_bid(self):
        print("TEST BID ON THING AND ACCEPTS HIGHER BID")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        stu_currency_bal_before = self.get_currency_balance('stu')
        ben_currency_bal_before = self.get_currency_balance('ben')

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10.1,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        stu_currency_bal_after = self.get_currency_balance('stu')
        ben_currency_bal_after = self.get_currency_balance('ben')

        self.assertEqual(
            stu_currency_bal_before,
            stu_currency_bal_after
        )
        self.assertEqual(
            ben_currency_bal_after,
            ben_currency_bal_before - 10.1
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            10.1
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_winner'),
            'ben'
        )
    def test_bid_neg_auction_not_started(self):
        print("TEST BID ON THING NEG AUCTION HAS ENDED")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            start_date=self.current_date + timedelta(seconds=2)
        )

        # Equal To
        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=10,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            'Auction has not stared.',
            str(cm.exception)
        )

        # GreaterThan
        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=10,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=5.1)
            )

        self.assertEqual(
            'Auction has ended.',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            None
        )

    def test_bid_neg_auction_ended(self):
        print("TEST BID ON THING NEG AUCTION HAS ENDED")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5)
        )

        # Equal To
        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=10,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=5)
            )

        self.assertEqual(
            'Auction has ended.',
            str(cm.exception)
        )

        # GreaterThan
        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=10,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=5.1)
            )

        self.assertEqual(
            'Auction has ended.',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            None
        )

    def test_bid_neg_higher_bid(self):
        print("TEST BID ON THING NEG HIGHER BID")

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        high_bid = 10

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=high_bid,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=9.9,
                signer='ben',
                bid_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            f'Current bid of {high_bid} is higher!',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            high_bid
        )
    def test_bid_neg_bid_of_zero(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=0,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            f'Bid must be greater than zero.',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            None
        )

    def test_bid_neg_bid_of_less_than_zero(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=-1,
                signer='stu',
                bid_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            f'Bid must be greater than zero.',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            None
        )

    def test_bid_neg_equal_bid(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5
        )

        high_bid = 10

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=high_bid,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        with self.assertRaises(AssertionError) as cm:
            self.make_bid(
                uid=self.new_thing_1_uid,
                bid_amount=high_bid,
                signer='ben',
                bid_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            f'Current bid of {high_bid} is higher!',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', f'{self.new_thing_1_uid}:current_bid'),
            high_bid
        )

    def test_end_auction_owner_as_creator(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2)
        )

        stu_currency_bal_before = self.get_currency_balance('stu')
        jeff_currency_bal_before = self.get_currency_balance('jeff')

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.end_auction(
            uid=self.new_thing_1_uid,
            signer='jeff',
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        stu_currency_bal_after = self.get_currency_balance('stu')
        jeff_currency_bal_after = self.get_currency_balance('jeff')

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            stu_currency_bal_before - 10,
            stu_currency_bal_after,
        )
        self.assertEqual(
            jeff_currency_bal_before + 10,
            jeff_currency_bal_after
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            False
        )

    def test_end_auction_owner_as_creator_no_royalty_percent(self):
        self.start_auction(
            uid=self.new_thing_2_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2)
        )

        stu_currency_bal_before = self.get_currency_balance('stu')
        jeff_currency_bal_before = self.get_currency_balance('jeff')

        self.make_bid(
            uid=self.new_thing_2_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.end_auction(
            uid=self.new_thing_2_uid,
            signer='jeff',
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        stu_currency_bal_after = self.get_currency_balance('stu')
        jeff_currency_bal_after = self.get_currency_balance('jeff')

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_2_uid}:owner'),
        )

        self.assertEqual(
            stu_currency_bal_before - 10,
            stu_currency_bal_after,
        )
        self.assertEqual(
            jeff_currency_bal_before + 10,
            jeff_currency_bal_after
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_2_uid),
            False
        )

    def test_end_auction_owner_not_creator(self):
        self.con_pixel_frames_master.transfer(
            uid=self.new_thing_1_uid,
            new_owner='ben'
        )

        self.assertEqual(
            'ben',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2),
            signer='ben'
        )

        stu_currency_bal_before = self.get_currency_balance('stu')
        ben_currency_bal_before = self.get_currency_balance('ben')
        jeff_currency_bal_before = self.get_currency_balance('jeff')

        bid_amount = 10

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=bid_amount,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.end_auction(
            uid=self.new_thing_1_uid,
            signer='ben',
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        stu_currency_bal_after = self.get_currency_balance('stu')
        ben_currency_bal_after = self.get_currency_balance('ben')
        jeff_currency_bal_after = self.get_currency_balance('jeff')

        royalty_percent = self.get_royalty_percent(uid=self.new_thing_1_uid)
        expected_royalty_amount = bid_amount * (royalty_percent / 100)
        expected_net_amount = bid_amount - expected_royalty_amount

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        # Buyers currency amount is less than the bid
        self.assertEqual(
            stu_currency_bal_before - bid_amount,
            stu_currency_bal_after,
        )

        # Creator's currency amount is plus the royalty percent amount
        self.assertEqual(
            jeff_currency_bal_before + expected_royalty_amount,
            jeff_currency_bal_after
        )

        # Sellers's currency amount is plus the bis amount minues royalty amount
        self.assertEqual(
            ben_currency_bal_before + expected_net_amount,
            ben_currency_bal_after
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            False
        )

    def test_end_auction_reserve_not_met(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2)
        )

        stu_currency_bal_before = self.get_currency_balance('stu')
        jeff_currency_bal_before = self.get_currency_balance('jeff')

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=2,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.end_auction(
            uid=self.new_thing_1_uid,
            signer='jeff',
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        stu_currency_bal_after = self.get_currency_balance('stu')
        jeff_currency_bal_after = self.get_currency_balance('jeff')

        self.assertEqual(
            'jeff',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            stu_currency_bal_before,
            stu_currency_bal_after,
        )
        self.assertEqual(
            jeff_currency_bal_before,
            jeff_currency_bal_after
        )
        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            False
        )

    def test_end_auction_no_bids(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2)
        )

        jeff_currency_bal_before = self.get_currency_balance('jeff')

        self.end_auction(
            uid=self.new_thing_1_uid,
            signer='jeff',
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        jeff_currency_bal_after = self.get_currency_balance('jeff')

        self.assertEqual(
            'jeff',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            jeff_currency_bal_before,
            jeff_currency_bal_after
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            False
        )

    def test_end_auction_early_neg_no_flag(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=2)
        )

        with self.assertRaises(AssertionError) as cm:
            self.end_auction(
                uid=self.new_thing_1_uid,
                signer='jeff',
                end_auction_datetime=self.current_date + timedelta(seconds=1)
            )

        self.assertEqual(
            f'Auction is still pending!',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.name,
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            True
        )

    def test_end_auction_cannot_end_early_with_winning_bid_as_owner(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5)
        )

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        with self.assertRaises(AssertionError) as cm:
            self.end_auction(
                uid=self.new_thing_1_uid,
                signer='jeff',
                end_early=True,
                end_auction_datetime=self.current_date + timedelta(seconds=3)
            )

        self.assertEqual(
            'Cannot end early. Auction started or reserve has been met.',
            str(cm.exception)
        )


        self.assertEqual(
            'con_pixel_frames_auction',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            True
        )

    def test_end_auction_early_with_flag_as_operator_started_but_no_bids(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='jeff',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )

    def test_end_auction_early_with_flag_as_owner_started_but_no_bids(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='stu',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )

    def test_end_auction_early_with_flag_as_owner_started_has_bids_but_reserve_not_met(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=2,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=1,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=2)
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='stu',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )

    def test_end_auction_early_with_flag_as_operator_started_has_bids_but_reserve_not_met(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=2,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=1,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=2)
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='jeff',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=3)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )

    def test_end_auction_early_with_flag_as_owner_auction_not_started(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            start_date=self.current_date + timedelta(seconds=2),
            signer='stu'
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='stu',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=1)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )


    def test_end_auction_early_with_flag_as_operator_auction_not_started(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            start_date=self.current_date + timedelta(seconds=2),
            signer='stu'
        )

        self.end_auction(
            uid=self.new_thing_3_uid,
            signer='jeff',
            end_early=True,
            end_auction_datetime=self.current_date + timedelta(seconds=1)
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            False
        )

    def test_end_auction_early_with_flag_as_operator_neg_auction_has_started_reserve_met(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=0,
            end_date=self.current_date + timedelta(seconds=5),
            start_date=self.current_date + timedelta(seconds=-5),
            signer='stu'
        )

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=1,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=2)
        )

        with self.assertRaises(AssertionError) as cm:
            self.end_auction(
                uid=self.new_thing_3_uid,
                signer='jeff',
                end_early=True,
                end_auction_datetime=self.current_date + timedelta(seconds=3)
            )

        self.assertEqual(
            'Cannot end early. Auction started or reserve has been met.',
            str(cm.exception)
        )

        self.assertEqual(
            'con_pixel_frames_auction',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            True
        )

    def test_end_auction_early_with_flag_as_owner_neg_auction_has_started_reserve_met(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=0,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=1,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=2)
        )

        with self.assertRaises(AssertionError) as cm:
            self.end_auction(
                uid=self.new_thing_3_uid,
                signer='stu',
                end_early=True,
                end_auction_datetime=self.current_date + timedelta(seconds=3)
            )

        self.assertEqual(
            'Cannot end early. Auction started or reserve has been met.',
            str(cm.exception)
        )

        self.assertEqual(
            'con_pixel_frames_auction',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid),
            True
        )

    def test_end_auction_early_neg_with_flag_not_owner(self):
        self.start_auction(
            uid=self.new_thing_1_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5)
        )

        self.make_bid(
            uid=self.new_thing_1_uid,
            bid_amount=10,
            signer='stu',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        with self.assertRaises(AssertionError) as cm:
            self.end_auction(
                uid=self.new_thing_1_uid,
                signer='stu',
                end_auction_datetime=self.current_date + timedelta(seconds=3),
                end_early=True
            )

        self.assertEqual(
            'Only thing owner or auction operator can end the auction early!',
            str(cm.exception)
        )

        self.assertEqual(
            self.con_pixel_frames_auction.name,
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_1_uid}:owner'),
        )

        self.assertEqual(
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_1_uid),
            True
        )

    def test_operator_thing_transfer(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        self.con_pixel_frames_auction.operator_transfer_thing(
            uid=self.new_thing_3_uid,
            new_owner='jeff',
            signer='jeff'
        )

        self.assertEqual(
            'jeff',
            self.con_pixel_frames.quick_read('S', f'{self.new_thing_3_uid}:owner'),
        )

        self.assertEqual(
            False,
            self.con_pixel_frames_auction.quick_read('S', self.new_thing_3_uid)
        )

    def test_operator_thing_transfer_neg_not_owner(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_auction.operator_transfer_thing(
                uid=self.new_thing_3_uid,
                new_owner='ben',
                signer='ben'
            )

        self.assertEqual(
            'Only auction operator can transfer things from contract.',
            str(cm.exception)
        )

    def test_operator_currency_transfer(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        ben_currency_bal_before = self.get_currency_balance('ben')
        jeff_currency_bal_before = self.get_currency_balance('jeff')
        auction_contract_currency_bal_before = self.get_currency_balance(self.con_pixel_frames_auction.name)

        if not auction_contract_currency_bal_before:
            auction_contract_currency_bal_before = 0

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=10,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.con_pixel_frames_auction.operator_transfer_currency(
            amount=10,
            to='jeff',
            signer='jeff'
        )

        ben_currency_bal_after = self.get_currency_balance('ben')
        jeff_currency_bal_after = self.get_currency_balance('jeff')
        auction_contract_currency_bal_after = self.get_currency_balance(self.con_pixel_frames_auction.name)

        self.assertEqual(
            ben_currency_bal_before - 10,
            ben_currency_bal_after
        )

        self.assertEqual(
            jeff_currency_bal_before + 10,
            jeff_currency_bal_after
        )

        self.assertEqual(
            auction_contract_currency_bal_before,
            auction_contract_currency_bal_after
        )

    def test_operator_currency_transfer_neg_not_owner(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_auction.operator_transfer_currency(
                amount=10,
                to='jeff',
                signer='ben'
            )

        self.assertEqual(
            'Only auction operator can transfer currency from contract.',
            str(cm.exception)
        )

    def test_change_operator(self):
        self.start_auction(
            uid=self.new_thing_3_uid,
            reserve_price=5,
            end_date=self.current_date + timedelta(seconds=5),
            signer='stu'
        )

        ben_currency_bal_before = self.get_currency_balance('ben')
        jeff_currency_bal_before = self.get_currency_balance('jeff')
        stu_currency_bal_before = self.get_currency_balance('stu')
        auction_contract_currency_bal_before = self.get_currency_balance(self.con_pixel_frames_auction.name)

        if not auction_contract_currency_bal_before:
            auction_contract_currency_bal_before = 0

        self.make_bid(
            uid=self.new_thing_3_uid,
            bid_amount=10,
            signer='ben',
            bid_datetime=self.current_date + timedelta(seconds=1)
        )

        self.con_pixel_frames_auction.operator_transfer_currency(
            amount=4,
            to='jeff',
            signer='jeff'
        )

        self.con_pixel_frames_auction.change_metadata(
            key='operator',
            value='stu',
            signer='jeff'
        )

        self.con_pixel_frames_auction.operator_transfer_currency(
            amount=4,
            to='stu',
            signer='stu'
        )

        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_auction.operator_transfer_currency(
                amount=2,
                to='jeff',
                signer='jeff'
            )

        self.assertEqual(
            'Only auction operator can transfer currency from contract.',
            str(cm.exception)
        )

        ben_currency_bal_after = self.get_currency_balance('ben')
        jeff_currency_bal_after = self.get_currency_balance('jeff')
        stu_currency_bal_after = self.get_currency_balance('stu')
        auction_contract_currency_bal_after = self.get_currency_balance(self.con_pixel_frames_auction.name)

        self.assertEqual(
            ben_currency_bal_before - 10,
            ben_currency_bal_after
        )

        self.assertEqual(
            jeff_currency_bal_before + 4,
            jeff_currency_bal_after
        )

        self.assertEqual(
            stu_currency_bal_before + 4,
            stu_currency_bal_after
        )

        self.assertEqual(
            auction_contract_currency_bal_before + 2,
            auction_contract_currency_bal_after
        )

        self.assertEqual(
            'stu',
            self.con_pixel_frames_auction.quick_read('metadata', 'operator')
        )

if __name__ == '__main__':
    unittest.main()