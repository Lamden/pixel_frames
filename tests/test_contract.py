#tests/test_contract.py
import unittest
import base64
from contracting.client import ContractingClient
client = ContractingClient()

frames_good_1 = ("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAABBBBBBBBABBBBBBAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBA" +
                     "BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBAAABBBBBAABBBBBBBBBA" +
                     "AAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBAAAAAABBBBBBBBBBBBBBBAAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBAABBB" +
                     "BBBBBBBBBBBBABBBBBAABBBBBBBBABBBBBBBABBBBBBBABBBBBBBBABBBBBBABBBBBBBBBAABBBAABBBBBBBBBBAAAAA" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBBBAABBBBBBBBBBBAAABBBBBBBBBBBBAABBBBBBBBBBBBAABBBBBBBBBBBBBAABBBBBBBBBBBBBBAB" +
                     "BBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBAAAAABBBBBB" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBB" +
                     "BBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBB" +
                     "BBBBBBBABBBBBBBBBBBBBBAABBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBB" +
                     "AAAAAAAAAAAB")

frames_good_2 = ("ABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAABBBBBBBBABBBBBBAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBA" +
                     "BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBAAABBBBBAABBBBBBBBBA" +
                     "AAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBAAAAAABBBBBBBBBBBBBBBAAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBAABBB" +
                     "BBBBBBBBBBBBABBBBBAABBBBBBBBABBBBBBBABBBBBBBABBBBBBBBABBBBBBABBBBBBBBBAABBBAABBBBBBBBBBAAAAA" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBBBAABBBBBBBBBBBAAABBBBBBBBBBBBAABBBBBBBBBBBBAABBBBBBBBBBBBBAABBBBBBBBBBBBBBAB" +
                     "BBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBAAAAABBBBBB" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBB" +
                     "BBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBB" +
                     "BBBBBBBABBBBBBBBBBBBBBAABBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBB" +
                     "AAAAAAAAAAAB")

frames_invalid_char = ("BBB1BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAABBBBBBBBABBBBBBAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBA" +
                     "BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBAAABBBBBAABBBBBBBBBA" +
                     "AAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBAAAAAABBBBBBBBBBBBBBBAAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBAABBB" +
                     "BBBBBBBBBBBBABBBBBAABBBBBBBBABBBBBBBABBBBBBBABBBBBBBBABBBBBBABBBBBBBBBAABBBAABBBBBBBBBBAAAAA" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBBBAABBBBBBBBBBBAAABBBBBBBBBBBBAABBBBBBBBBBBBAABBBBBBBBBBBBBAABBBBBBBBBBBBBBAB" +
                     "BBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBAAAAABBBBBB" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBB" +
                     "BBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBB" +
                     "BBBBBBBABBBBBBBBBBBBBBAABBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBB" +
                     "AAAAAAAAAAAB")

frames_invalid_len = ("BBB1BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAABBBBBBBBABBBBBBAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBA" +
                     "BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBAAABBBBBAABBBBBBBBBA" +
                     "AAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBAAAAAABBBBBBBBBBBBBBBAAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBAABBB" +
                     "BBBBBBBBBBBBABBBBBAABBBBBBBBABBBBBBBABBBBBBBABBBBBBBBABBBBBBABBBBBBBBBAABBBAABBBBBBBBBBAAAAA" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBBBAABBBBBBBBBBBAAABBBBBBBBBBBBAABBBBBBBBBBBBAABBBBBBBBBBBBBAABBBBBBBBBBBBBBAB" +
                     "BBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBAAAAABBBBBB" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBB" +
                     "BBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBB" +
                     "BBBBBBBABBBBBBBBBBBBBBAABBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBB" +
                     "AAAAAAAAAAABAAAA")

frames_invalid_data_len = ("BBB1BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAABBBBBBBBABBBBBBAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBA" +
                     "BBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBAAABBBBBAABBBBBBBBBA" +
                     "AAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBAAAAAABBBBBBBBBBBBBBBAAABBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBAABBB" +
                     "BBBBBBBBBBBBABBBBBAABBBBBBBBABBBBBBBABBBBBBBABBBBBBBBABBBBBBABBBBBBBBBAABBBAABBBBBBBBBBAAAAA" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" +
                     "BBBBBBBBBBBBBBBBBAABBBBBBBBBBBAAABBBBBBBBBBBBAABBBBBBBBBBBBAABBBBBBBBBBBBBAABBBBBBBBBBBBBBAB" +
                     "BBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBBAABBBBBBBBBBBBBBBAAAAABBBBBB" +
                     "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBB" +
                     "BBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBBBBBBBBBABBBBBBBB" +
                     "BBBBBBBABBBBBB")

with open('../frontend/static/img/logo.svg') as f:
    icon_svg = f.read()
    icon_svg_base64 = base64.b64encode(bytes(icon_svg, encoding='utf-8'))

with open('./currency.py') as f:
    code = f.read()
    client.submit(code, name='currency')
with open('../contracts/con_pixel_frames.py') as f:
    code = f.read()
    client.submit(code, name='con_pixel_frames', owner="con_pixel_frames_master")
with open('../contracts/con_pixel_frames_master.py') as f:
    code = f.read()
    client.submit(
        code,
        name='con_pixel_frames_master'
    )

class MyTestCase(unittest.TestCase):
    con_pixel_frames_master = None
    con_pixel_frames = None

    def change_signer(self, name):
        client.signer = name
        self.con_pixel_frames_master = client.get_contract('con_pixel_frames_master')
        self.con_pixel_frames = client.get_contract('con_pixel_frames')
        self.currency_contract = client.get_contract('currency')

    def test_01a_create_thing(self):
        print("TEST CREATE A THING")
        self.change_signer('jeff')
        new_thing = self.con_pixel_frames_master.create_thing(
            thing_string=frames_good_1,
            name="New Pixel Frame 1a!",
            description="Test Case 1a Pixel Frame",
            meta={
                'speed': 256,
                'num_of_frames': 4
            }
        )


    def test_01b_create_thing_assert_invalid_char(self):
        print("TEST CREATE A THING - NEG - INVALID PIXEL CHAR")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_char,
                name="New Pixel Frame 1b!",
                description="Test Case 1b Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4
                }
            )
        )

    def test_01c_create_thing_assert_invalid_frame_length(self):
        print("TEST CREATE A THING - NEG - INVALID FRAME LENGTH")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_len,
                name="New Pixel Frame 1c!",
                description="Test Case 1c Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4
                }
            )
        )

    def test_01d_create_thing_assert_invalid_frame_data_length(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES DATA LENGTH")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_data_len,
                name="New Pixel Frame 1d!",
                description="Test Case 1d Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4
                }
            )
        )

    def test_01e_create_thing_assert_invalid_frame_value_1(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES VALUE HIGH")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1e!",
                description="Test Case 1e Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 5
                }
            )
        )
    def test_01f_create_thing_assert_invalid_frame_value_2(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES VALUE LOW")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1f!",
                description="Test Case 1f Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': -1
                }
            )
        )
    def test_01g_create_thing_assert_invalid_frame_value_3(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES IS INT")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1g!",
                description="Test Case 1g Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': "4"
                }
            )
        )

    def test_01h_create_thing_assert_invalid_frame_value_4(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES MISSING")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1h!",
                description="Test Case 1h Pixel Frame",
                meta={
                    'speed': 256
                }
            )
        )

    def test_01i_create_thing_assert_invalid_speed_value_1(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED MISSING")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1i!",
                description="Test Case 1i Pixel Frame",
                meta={
                    'num_of_frames': 4
                }
            )
        )
    def test_01j_create_thing_assert_invalid_speed_value_2(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED IS INT")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1j!",
                description="Test Case 1j Pixel Frame",
                meta={
                    'speed': '256',
                    'num_of_frames': 4
                }
            )
        )
    def test_01k_create_thing_assert_invalid_speed_value_3(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED VALUE HIGH")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1k!",
                description="Test Case 1k Pixel Frame",
                meta={
                    'speed': 2001,
                    'num_of_frames': 4
                }
            )
        )
    def test_01l_create_thing_assert_invalid_speed_value_4(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED VALUE LOW")
        self.change_signer('jeff')
        self.assertRaises(
            AssertionError,
            lambda: self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1l!",
                description="Test Case 1l Pixel Frame",
                meta={
                    'speed': 99,
                    'num_of_frames': 4
                }
            )
        )
if __name__ == '__main__':
    unittest.main()