#tests/test_contract.py
import unittest
import base64
from contracting.client import ContractingClient
client = ContractingClient()

frames_good_1 = ("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnjjjPPPnnnnnnnnnnnnnUUjjUjjPPjjjPPPPnnnnnnnnjjjnyyyPyyyPjjPjPPPnnnnnnjjjyPPPPPPPPyjPjPPPPnnnnnnjjPPPPPPPPPPPjyPPPPnnnnUUUjjPPPPPyyyyjjyyPPPnnnUUUUyjjjPyPUUUjyjyyPPPnnnUUUUjPjjyyPUjjUUjyPPPPnnnUUUjjjjjjjPnjnyynjnnnnnnnnnnjPyyPjPjPPynnnnjnnnnnnnnnjnPPyjjjPyPPPPPjnnnnnnnnjnnPPjjyyjjPPPPPjnnnnnnnnjnUPjjjPyyjjPPPPjPnnnnnnnjUUjjPPPPPjjjPPjPPnnnnnnUjjUjjjPPPPPjyPjjPPnnnnUUUUjUjjPPPPPPPjjjPPPnnnnUUUUjUjjPPPPPPPPyjPPPnnnnUUUUjjPjyyPPPPPPyPjjPnnnnUUUUjUUjjPyyPPPyPPPnnnnnnUUUUUjUnjPPPyyyyPPPnnnjnnnnnnnnnnjjPPPPPPPPnnjjnnnnnnnnnnnnjjjjjjjjjjjnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
                 "nnnnnnnnnnnnnnnnnnnnnnnnnnnZZZZZZnZZjZZZZZnnnnnnnnnnnZZZZZZjZZZjjjPZZZZnnnnnnnjZZZZyyPyyZPZZZZZZZnnnnnnjjjyZZPPPPPPyjZZPPZPnnnnnnjjPPZZPPPPZZZjyPZPPnnnnUUUjjPPZZPZZyyjjyyZPPnnnUUUUyjjZZZZUUUjyjyyZPPnnnUUZUjZZjyyZUjjUUjyPZPPnnnUUZZZZjjjjZnjnyynjZnnnnnnnnnZZyyPjPjZPynnnnjnnnnnnnnnZnZPyjjjZyPPPPPZnnnnnnnnjZZZZZZyZZZZZZZZZZnnnnnnnjnUPjZjPyZjjPPPPZZnnnnnnnjUUjjZZPPZjjjPZZZZZnnnnnUjjUjjjZZZZZZZZZjPPZnnnUUUUjUZZZZZZPPPjjjPPPZZnnUUUUjZZZZPPPZZPPyjPPPnZnnUUUUZZZZyyPPPPZPZPjjPZZnnUUUUZZUjjPyyPPPyZZZZZZnnnUUUZZZZZZZZZZZZZZZZnZnjnnnnnZZnnZZZZZPPPPPPZZjjnnnnnnnnnnnnjjjjZZZjjjZZnnnnnnnnnnnnnnnnnnnnZZZnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
frames_good_1_name_hash = "a4e624d686e03ed2767c0abd85c14426b0b1157d2ce81d27bb4fe4f6f01d688a"
frames_good_1_uid = "20e2c4baf4fce1cc17e386ead27d62342ea3cf261ccae029b7d2307d43940a28"

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

frames_invalid_char = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB*BBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBzzYBBBBBBBzzzzYBzzzzBzzzzzzBBBBBBBzzBYzzzzzzzYYBBzBYBBBBBBBzYBBzzzYYYYYYYzBYYBBBBBBBzYYzzYYBBBBBzBYYBYBBBBBBBYzYzBBYBBBBBBBYYBYYBBBBBBYzzzBBBYBBBzBBYYBBYBBBBBBYzzzzYBBYBzzBBYYBzYBBBBBBBzYBYBBBBYBBzzYBzzBYBBBBBBzYYBzzBBBBBYYYBBBzzBBBBBBBYYBYBzBBBYYBBzBBBYBzBBBBzzYBBYBBzzYYzBBBBBYBBzBBBBYzYBYYBBYzzBBBBBBYBBzBBBzYBzzYzzYzzYBBBBBBYBBzBBBzYYBBYYYYBzBYBBBBBYBzBBBBBYBBBBBBBBzYBYBBBBYzBBBBBzzYYBBBBBzBBYYYYYzzBBBBBBBzBYYYYBzBBBYYBYBzBBBBBBBBBzzzzzYYYBYBBBYBzBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiizzYiiiiiiizzzzYizzzzizzzzzzBiiiiiizzBYzzzzzzzYYBBzBYBiiiiiizYBBzzzYYYYYYYzBYYBiiiiiizYYzzYYBBBBBzBYYBYBiiiiiiYzYzBBYBBBBBBBYYBYYiiiiiiYzzzBBBYBBBzBBYYBBYiiiiiiYzzzzYBBYBzzBBYYBzYiiiiiiizYBYBBBBYBBzzYBzzBYiiiiiizYYBzzBBBBBYYYBBBzziiiiiiBYYBYBzBBBYYBBzBBBYiziiiizzYBBYBBzzYYzBBBBBYiBziiiBYzYBYYBBYzzBBBBBBYiBziiizYBzzYzzYzzYBBBBBBYiBziiizYYBBYYYYBzBYBBBBBYiziiiiBYBBBBBBBBzYBYBBBBYziiiiizzYYBBBBBziBYYYYYzziiiiiiizBYYYYBziiBYYBYiziiiiiiiiizzzzzYYYiYBBBYiziiiiiiiiiiiiiiiiiiYYYYYiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOzzYOOOOOOOzzzzYOzzzzOzzzzzzBOOOOOOzzBYzzzzzzzYYBBzBYBOOOOOOzYBBzzzYYYYYYYzBYYBOOOOOOzYYzzYYOOOOOzBYYBYBOOOOOOYzYzBBYOOOOOBBYYBYYOOOOOOYzzzBBBYOOOzBBYYBBYOOOOOOYzzzzYBBYOzzBBYYBzYOOOOOOOzYBYBBBBYBBzzYBzzBYOOOOOOzYYBzzBBBBBYYYBOOzzOOOOOOBYYBYBzBBBYYBOzOOOYOzOOOOzzYBBYBBzzYYzOOOOOYOBzOOOBYzYBYYBBYzzOOOOOOYOBzOOOzYBzzYzzYzzYOOOOOOYOBzOOOzYYOOYYYYOzBYOOOOOYOzOOOOBYOOOOOOOOzYBYOOOOYzOOOOOzzYYOOOOOzOBYYYYYzzOOOOOOOzBYYYYOzOOBYYBYOzOOOOOOOOOzzzzzYYYOYBBBYOzOOOOOOOOOOOOOOOOOOYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
)

frames_invalid_char_92 = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\BBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBzzYBBBBBBBzzzzYBzzzzBzzzzzzBBBBBBBzzBYzzzzzzzYYBBzBYBBBBBBBzYBBzzzYYYYYYYzBYYBBBBBBBzYYzzYYBBBBBzBYYBYBBBBBBBYzYzBBYBBBBBBBYYBYYBBBBBBYzzzBBBYBBBzBBYYBBYBBBBBBYzzzzYBBYBzzBBYYBzYBBBBBBBzYBYBBBBYBBzzYBzzBYBBBBBBzYYBzzBBBBBYYYBBBzzBBBBBBBYYBYBzBBBYYBBzBBBYBzBBBBzzYBBYBBzzYYzBBBBBYBBzBBBBYzYBYYBBYzzBBBBBBYBBzBBBzYBzzYzzYzzYBBBBBBYBBzBBBzYYBBYYYYBzBYBBBBBYBzBBBBBYBBBBBBBBzYBYBBBBYzBBBBBzzYYBBBBBzBBYYYYYzzBBBBBBBzBYYYYBzBBBYYBYBzBBBBBBBBBzzzzzYYYBYBBBYBzBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiizzYiiiiiiizzzzYizzzzizzzzzzBiiiiiizzBYzzzzzzzYYBBzBYBiiiiiizYBBzzzYYYYYYYzBYYBiiiiiizYYzzYYBBBBBzBYYBYBiiiiiiYzYzBBYBBBBBBBYYBYYiiiiiiYzzzBBBYBBBzBBYYBBYiiiiiiYzzzzYBBYBzzBBYYBzYiiiiiiizYBYBBBBYBBzzYBzzBYiiiiiizYYBzzBBBBBYYYBBBzziiiiiiBYYBYBzBBBYYBBzBBBYiziiiizzYBBYBBzzYYzBBBBBYiBziiiBYzYBYYBBYzzBBBBBBYiBziiizYBzzYzzYzzYBBBBBBYiBziiizYYBBYYYYBzBYBBBBBYiziiiiBYBBBBBBBBzYBYBBBBYziiiiizzYYBBBBBziBYYYYYzziiiiiiizBYYYYBziiBYYBYiziiiiiiiiizzzzzYYYiYBBBYiziiiiiiiiiiiiiiiiiiYYYYYiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOzzYOOOOOOOzzzzYOzzzzOzzzzzzBOOOOOOzzBYzzzzzzzYYBBzBYBOOOOOOzYBBzzzYYYYYYYzBYYBOOOOOOzYYzzYYOOOOOzBYYBYBOOOOOOYzYzBBYOOOOOBBYYBYYOOOOOOYzzzBBBYOOOzBBYYBBYOOOOOOYzzzzYBBYOzzBBYYBzYOOOOOOOzYBYBBBBYBBzzYBzzBYOOOOOOzYYBzzBBBBBYYYBOOzzOOOOOOBYYBYBzBBBYYBOzOOOYOzOOOOzzYBBYBBzzYYzOOOOOYOBzOOOBYzYBYYBBYzzOOOOOOYOBzOOOzYBzzYzzYzzYOOOOOOYOBzOOOzYYOOYYYYOzBYOOOOOYOzOOOOBYOOOOOOOOzYBYOOOOYzOOOOOzzYYOOOOOzOBYYYYYzzOOOOOOOzBYYYYOzOOBYYBYOzOOOOOOOOOzzzzzYYYOYBBBYOzOOOOOOOOOOOOOOOOOOYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
)

frames_invalid_len = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBzzYBBBBBBBzzzzYBzzzzBzzzzzzBBBBBBBzzBYzzzzzzzYYBBzBYBBBBBBBzYBBzzzYYYYYYYzBYYBBBBBBBzYYzzYYBBBBBzBYYBYBBBBBBBYzYzBBYBBBBBBBYYBYYBBBBBBYzzzBBBYBBBzBBYYBBYBBBBBBYzzzzYBBYBzzBBYYBzYBBBBBBBzYBYBBBBYBBzzYBzzBYBBBBBBzYYBzzBBBBBYYYBBBzzBBBBBBBYYBYBzBBBYYBBzBBBYBzBBBBzzYBBYBBzzYYzBBBBBYBBzBBBBYzYBYYBBYzzBBBBBBYBBzBBBzYBzzYzzYzzYBBBBBBYBBzBBBzYYBBYYYYBzBYBBBBBYBzBBBBBYBBBBBBBBzYBYBBBBYzBBBBBzzYYBBBBBzBBYYYYYzzBBBBBBBzBYYYYBzBBBYYBYBzBBBBBBBBBzzzzzYYYBYBBBYBzBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiizzYiiiiiiizzzzYizzzzizzzzzzBiiiiiizzBYzzzzzzzYYBBzBYBiiiiiizYBBzzzYYYYYYYzBYYBiiiiiizYYzzYYBBBBBzBYYBYBiiiiiiYzYzBBYBBBBBBBYYBYYiiiiiiYzzzBBBYBBBzBBYYBBYiiiiiiYzzzzYBBYBzzBBYYBzYiiiiiiizYBYBBBBYBBzzYBzzBYiiiiiizYYBzzBBBBBYYYBBBzziiiiiiBYYBYBzBBBYYBBzBBBYiziiiizzYBBYBBzzYYzBBBBBYiBziiiBYzYBYYBBYzzBBBBBBYiBziiizYBzzYzzYzzYBBBBBBYiBziiizYYBBYYYYBzBYBBBBBYiziiiiBYBBBBBBBBzYBYBBBBYziiiiizzYYBBBBBziBYYYYYzziiiiiiizBYYYYBziiBYYBYiziiiiiiiiizzzzzYYYiYBBBYiziiiiiiiiiiiiiiiiiiYYYYYiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOzzYOOOOOOOzzzzYOzzzzOzzzzzzBOOOOOOzzBYzzzzzzzYYBBzBYBOOOOOOzYBBzzzYYYYYYYzBYYBOOOOOOzYYzzYYOOOOOzBYYBYBOOOOOOYzYzBBYOOOOOBBYYBYYOOOOOOYzzzBBBYOOOzBBYYBBYOOOOOOYzzzzYBBYOzzBBYYBzYOOOOOOOzYBYBBBBYBBzzYBzzBYOOOOOOzYYBzzBBBBBYYYBOOzzOOOOOOBYYBYBzBBBYYBOzOOOYOzOOOOzzYBBYBBzzYYzOOOOOYOBzOOOBYzYBYYBBYzzOOOOOOYOBzOOOzYBzzYzzYzzYOOOOOOYOBzOOOzYYOOYYYYOzBYOOOOOYOzOOOOBYOOOOOOOOzYBYOOOOYzOOOOOzzYYOOOOOzOBYYYYYzzOOOOOOOzBYYYYOzOOBYYBYOzOOOOOOOOOzzzzzYYYOYBBBYOzOOOOOOOOOOOOOOOOOOYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO00"
)

frames_invalid_data_len = (
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBYYBBBBBBBBBBYYBYYYBBBBBBBYBBBBBBBBBBYBBBBBBBYYBBBBYBBBBBBBBYBBBBBBBBBBBYBBYBBBBBBBBBYYYYYBBBBBBBBYYBBBBBBBBBYBYBBBYBBBBBBBBYBBBBBBBBBYBYBBBBYBBBBBBBYBBBBBBBBBYBYBYYBBYBBBBBYYBBBBBBBBBBYYBYBBBBYBBBYYBBBBBBBBBBBBYYBBBBBBBBYBBBBBBBBBBBBBBYYBYBBBBBYBBBBBBBBBBBBBBBYYBBYBBYBYBBBBBBBBBBBBBBBYBYBYYBBYYBBBBBBBBBBBBBBBYBYYYBBYYBYBBBBBBBBBBBBBBYYBBYYYYBBBYBBBBBBBBBBBBBYBBBBBBBBBBBYBBBBBBBBBBBBYYYBBBBBBBBBYYBBBBBBBBBBBBBYYYYBBBBBYYBYBBBBBBBBBBBBBBBYYYYBYBBBYBBBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBzzYBBBBBBBzzzzYBzzzzBzzzzzzBBBBBBBzzBYzzzzzzzYYBBzBYBBBBBBBzYBBzzzYYYYYYYzBYYBBBBBBBzYYzzYYBBBBBzBYYBYBBBBBBBYzYzBBYBBBBBBBYYBYYBBBBBBYzzzBBBYBBBzBBYYBBYBBBBBBYzzzzYBBYBzzBBYYBzYBBBBBBBzYBYBBBBYBBzzYBzzBYBBBBBBzYYBzzBBBBBYYYBBBzzBBBBBBBYYBYBzBBBYYBBzBBBYBzBBBBzzYBBYBBzzYYzBBBBBYBBzBBBBYzYBYYBBYzzBBBBBBYBBzBBBzYBzzYzzYzzYBBBBBBYBBzBBBzYYBBYYYYBzBYBBBBBYBzBBBBBYBBBBBBBBzYBYBBBBYzBBBBBzzYYBBBBBzBBYYYYYzzBBBBBBBzBYYYYBzBBBYYBYBzBBBBBBBBBzzzzzYYYBYBBBYBzBBBBBBBBBBBBBBBBBBYYYYYBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
    "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiizzYiiiiiiizzzzYizzzzizzzzzzBiiiiiizzBYzzzzzzzYYBBzBYBiiiiiizYBBzzzYYYYYYYzBYYBiiiiiizYYzzYYBBBBBzBYYBYBiiiiiiYzYzBBYBBBBBBBYYBYYiiiiiiYzzzBBBYBBBzBBYYBBYiiiiiiYzzzzYBBYBzzBBYYBzYiiiiiiizYBYBBBBYBBzzYBzzBYiiiiiizYYBzzBBBBBYYYBBBzziiiiiiBYYBYBzBBBYYBBzBBBYiziiiizzYBBYBBzzYYzBBBBBYiBziiiBYzYBYYBBYzzBBBBBBYiBziiizYBzzYzzYzzYBBBBBBYiBziiizYYBBYYYYBzBYBBBBBYiziiiiBYBBBBBBBBzYBYBBBBYziiiiizzYYBBBBBziBYYYYYzziiiiiiizBYYYYBziiBYYBYiziiiiiiiiizzzzzYYYiYBBBYiziiiiiiiiiiiiiiiiiiYYYYYiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOzzYOOOOOOOzzzzYOzzzzOzzzzzzBOOOOOOzzBYzzzzzzzYYBBzBYBOOOOOOzYBBzzzYYYYYYYzBYYBOOOOOOzYYzzYYOOOOOzBYYBYBOOOOOOYzYzBBYOOOOOBBYYBYYOOOOOOYzzzBBBYOOOzBBYYBBYOOOOOOYzzzzYBBYOzzBBYYBzYOOOOOOOzYBYBBBBYBBzzYBzzBYOOOOOOzYYBzzBBBBBYYYBOOzzOOOOOOBYYBYBzBBBYYBOzOOOYOzOOOOzzYBBYBBzzYYzOOOOOYOBzOOOBYzYBYYBBYzzOOOOOOYOBzOOOzYBzzYzzYzzYOOOOOOYOBzOOOzYYOOYYYYOzBYOOOOOYOzOOOOBYOOOOOOOOzYBYOOOOYzOOOOOzzYYOOOOOzOBYYYYYzzOOOOOOOzBYYYYOzOOBYYBYOzOOOOOOOOOzzzzzYYYOYBBBYOzOOOOOOOOOOOOOOOOOOYYYYYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOiiiiiiiiOOOOOOOOOOOOOOOOiiiiiiiiiizzYOOOOOOOzOOOYiiiiiiiiiizzOOOOOOOzOBYziiiiiiiiiiiBOBOOOOOOzOiiiiiiiiiiiiiiYYBOiiOOOOiiiiiiiiiiiiiiiiYBOiOOOOiiiiiiiiiiiiiiiiiYiOOOOOiiiiiiiiiiiiiiiiiiBYOOOOiiiiiiiiiiiiiiiiiiiiYOOOOiiiiiiiiiiiiOBiiiiiiBYOOOiiiiiiiiiBBBOBiiiiiizzOOOiiiiiiiiiOBBBYiiiiiiOYOzOiiiiiiiiOiBzzOiiiiiiOYOBziiiiiiiiiiBBiziiiiiOOYOBziiiiiiiiiiiYzzOOOiOOOYOBziiiiiiiiiiiiizBOOOOOOiOzOiiiiiiiiiiiiizYBOOOiOizOOOiiiiiiiiiiiiiiYYYYYiiiOOOiiiiiiiiiiiiiiYYBYOzOOOOOOOiiiiiiiiiiiiBBBYOzOOOOOOOOOiiiiiiiiiiYYYYOOOOOOOOOOOOOiiiiiiiiOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    "ZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZiiiiZZZZZZZZZZZZZZZZZZZZZiiiiiiiiZZZZZZZZZZZZZZZZZiiiiiiiiZZZZZZZZZZZZZZZZZZiiiiiiiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZiZZZZZiZZZZZZZZZZZZZZZZZZZiiiBBBZZZZZZZZZZZZZZZZZZZiiiOBBBZZZZZZZZZZZZZZZZZZZiOiZZZZZZZZZZZZZZZiZZZZZZZZZZZZZZZZZiZZZZZZiZZZZZZZZZZZZZZZZZOZZZZZZiiZZZZZZZZZZZZZOOOOZZZZZZiZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOZZZZZZZZZZZZZZZZZZZZZZZZOOOOZZZZZZZZZZZZZZZZZZZOO"
    "YYYYYYYYYYYYYYGGGGGZZYYYOYYYYYYYYYYYGGGGGGGGGZYYYOYYGGGGGYYYGGGGGGGGGGZYYYYYYGGGGGYYYGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGGZYYYYYGGGGGGGGGGGGGGGGGGZZYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGiZGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUYYYYGGGGGGGGGGGGGGGGGGGUUUYYYGGGGGGGGGGGGGGGGGGGUUUYYYiYYYGGGGGGGGGGGGGGGUUUYYYiYYYGGGGGGGGGYGGGGGUUUUYYiiYYYGGGGGGGGYGGGGGUUUUYYiYYYYGGGGGGGGYGGGGGUUUUYYOYYYYGGGGGGGGYGGGGGUUUUYYOYYYYGGGGGGGGYYYYYGUUUUYYOYYYYYYYGGGGGYYYYYYYYYYYYOYYYYYYYGGGGGYYYYYYYYYYYYOYYYYYYYYYYYYYYYYYYYYYYYYOYYYYYYYYYYYYYYYYYYYYYYYYOOOOYYYYYYYYYYYYYYYYYYYOO"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
)


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
            name="Test4",
            description="Test Case 1a Pixel Frame",
            meta={
                'speed': 256,
                'num_of_frames': 2,
                'royalty_percent': 20
            }
        )

        assert len(new_thing) is 64, "UID not returned"

        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join(['names', frames_good_1_name_hash])), new_thing)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'thing'])), frames_good_1)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 0)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'hold'])), None)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'type'])), "text/plain")
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'name'])), "Test4")
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'description'])), "Test Case 1a Pixel Frame")
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'jeff')
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'creator'])), 'jeff')
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'likes'])), 0)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid])),
                         ['thing', 'type', 'name', 'description', 'owner', 'creator', 'likes', 'price:amount', 'price:hold', 'meta_items'])
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'meta_items'])),
                         ['speed', 'num_of_frames', 'royalty_percent'])
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'meta', 'num_of_frames'])), 2)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'meta', 'speed'])), 256)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'meta', 'royalty_percent'])), 20)
        # balance updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01b_create_thing_assert_invalid_char_1(self):
        print("TEST CREATE A THING - NEG - INVALID PIXEL CHAR *")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_char,
                name="New Pixel Frame 1b_1!",
                description="Test Case 1b Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Frames Data contains invalid pixel *.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)
    def test_01b_create_thing_assert_invalid_char_2(self):
        print("TEST CREATE A THING - NEG - INVALID PIXEL CHAR \\")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_char_92,
                name="New Pixel Frame 1b_2!",
                description="Test Case 1b Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Frames Data contains invalid pixel \.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01c_create_thing_assert_invalid_frame_length(self):
        print("TEST CREATE A THING - NEG - INVALID FRAME LENGTH")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_len,
                name="New Pixel Frame 1c!",
                description="Test Case 1c Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Frames Data is Invalid, must be 625 pixels/frame.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01d_create_thing_assert_invalid_frame_data_length(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES DATA LENGTH")
        self.change_signer('jeff')

        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_invalid_data_len,
                name="New Pixel Frame 1d!",
                description="Test Case 1d Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 7,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'num_of_frames value is invalid.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)


    def test_01e_create_thing_assert_invalid_frame_value_1(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES VALUE HIGH")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1e!",
                description="Test Case 1e Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 9,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'num_of_frames value 9 is out of range (1-4).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01f_create_thing_assert_invalid_frame_value_2(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES VALUE LOW")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1f!",
                description="Test Case 1f Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': -1,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'num_of_frames value -1 is out of range (1-4).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01g_create_thing_assert_invalid_frame_value_3(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES IS INT (str)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1g!",
                description="Test Case 1g Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': "4",
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'num_of_frames value is not an integer.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01g_create_thing_assert_invalid_frame_value_3_5(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES IS INT (float)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1g!",
                description="Test Case 1g Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4.5,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'num_of_frames value is not an integer.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01h_create_thing_assert_invalid_frame_value_4(self):
        print("TEST CREATE A THING - NEG - INVALID FRAMES MISSING")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1h!",
                description="Test Case 1h Pixel Frame",
                meta={
                    'speed': 256,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            "Missing meta value 'num_of_frames' (int).",
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01i_create_thing_assert_invalid_speed_value_1(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED MISSING")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1i!",
                description="Test Case 1i Pixel Frame",
                meta={
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            "Missing meta value 'speed' (int).",
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01j_create_thing_assert_invalid_speed_value_2(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED IS INT (str)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1j!",
                description="Test Case 1j Pixel Frame",
                meta={
                    'speed': '256',
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Speed value is not an integer.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01j_create_thing_assert_invalid_speed_value_2_5(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED IS INT (float)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1j!",
                description="Test Case 1j Pixel Frame",
                meta={
                    'speed': 256.5,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Speed value is not an integer.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01k_create_thing_assert_invalid_speed_value_3(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED VALUE HIGH")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1k!",
                description="Test Case 1k Pixel Frame",
                meta={
                    'speed': 2001,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Speed value 2001 is out of range (100ms-2000ms).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01l_create_thing_assert_invalid_speed_value_4(self):
        print("TEST CREATE A THING - NEG - INVALID SPEED VALUE LOW")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1l!",
                description="Test Case 1l Pixel Frame",
                meta={
                    'speed': 99,
                    'num_of_frames': 4,
                    'royalty_percent': 20
                }
            )
        self.assertEqual(
            'Speed value 99 is out of range (100ms-2000ms).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01m_create_thing_assert_invalid_royalty_value_1(self):
        print("TEST CREATE A THING - NEG - INVALID ROYALTY MISSING")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1m!",
                description="Test Case 1m Pixel Frame",
                meta={
                    'speed': 100,
                    'num_of_frames': 4
                }
            )
        self.assertEqual(
            "Missing meta value 'royalty_percent' (int).",
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01n_create_thing_assert_invalid_royalty_value_2(self):
        print("TEST CREATE A THING - NEG - INVALID ROYALTY IS INT (str)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1n!",
                description="Test Case 1n Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': '20'
                }
            )
        self.assertEqual(
            'royalty_percent value is not an integer.',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01n_create_thing_assert_invalid_royalty_value_2_5(self):
        print("TEST CREATE A THING - NEG - INVALID ROYALTY IS INT (float)")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1n!",
                description="Test Case 1n Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': 20.5
                }
            )
        self.assertEqual(
            'royalty_percent value is not an integer.',
            str(cm.exception)
            )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01o_create_thing_assert_invalid_royalty_value_3(self):
        print("TEST CREATE A THING - NEG - INVALID ROYALTY VALUE HIGH")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1o!",
                description="Test Case 1o Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': 101
                }
            )
        self.assertEqual(
            'royalty_percent value 101 is out of range (0-100).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_01p_create_thing_assert_invalid_royalty_value_4(self):
        print("TEST CREATE A THING - NEG - INVALID ROYALTY VALUE LOW")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.create_thing(
                thing_string=frames_good_2,
                name="New Pixel Frame 1p!",
                description="Test Case 1p Pixel Frame",
                meta={
                    'speed': 256,
                    'num_of_frames': 4,
                    'royalty_percent': -1
                }
            )
        self.assertEqual(
            'royalty_percent value -1 is out of range (0-100).',
            str(cm.exception)
        )

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_02a_sell_thing(self):
        print("TEST SELL THING")
        self.change_signer('jeff')
        self.con_pixel_frames_master.sell_thing(
            uid=frames_good_1_uid,
            amount=100
        )
        # Price is set
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 100)

    def test_02b_sell_thing_neg_negative_value(self):
        print("TEST SELL THING - NEG - AMOUNT IS NEGATIVE")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.sell_thing(
                uid=frames_good_1_uid,
                amount=-1
            )
        self.assertEqual(
            'Cannot set a negative price',
            str(cm.exception)
        )
        # price did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 100)

    def test_02c_sell_thing_neg_not_owner(self):
        print("TEST SELL THING - NEG - NOT OWNED")
        self.change_signer('stu')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.sell_thing(
                uid=frames_good_1_uid,
                amount=1
            )
        self.assertEqual(
            frames_good_1_uid + ' not owned by stu',
            str(cm.exception)
        )
        # price did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 100)

    def test_03a_buy_thing_already_owner(self):
        print("TEST BUY THING - NEG - ALREADY OWNED")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.buy_thing(
                uid=frames_good_1_uid
            )
        self.assertEqual(
            frames_good_1_uid + ' already owned by jeff',
            str(cm.exception)
        )
        # price did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 100)

        # balance not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 1)

    def test_03b_buy_thing(self):
        print("TEST BUY THING")
        self.change_signer('stu')
        stu_prev_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_prev_currency_bal = self.currency_contract.quick_read('balances', 'jeff')

        # print('stu_prev_currency_bal: ', stu_prev_currency_bal)
        # print('jeff_prev_currency_bal: ', jeff_prev_currency_bal)

        self.con_pixel_frames_master.buy_thing(
            uid=frames_good_1_uid
        )
        stu_curr_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_curr_currency_bal = self.currency_contract.quick_read('balances', 'jeff')

        # print('stu_curr_currency_bal: ', stu_curr_currency_bal)
        # print('jeff_curr_currency_bal: ', jeff_curr_currency_bal)

        #price set back to zero (becomes un-buyable)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 0)
        # owner changes
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')
        # creator doesn't change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'creator'])), 'jeff')
        # correct amount taken from stu for sale
        self.assertEqual(stu_prev_currency_bal - stu_curr_currency_bal, 100)
        # correct amount given to jeff (amount + royalty) because he is the seller and the creator
        self.assertEqual(jeff_curr_currency_bal - jeff_prev_currency_bal, 100)

        # balances updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 0)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)

    def test_03c_buy_thing_neg_not_for_sale(self):
        print("TEST BUY THING - NEG - NOT FOR SALE")
        self.change_signer('jeff')
        jeff_prev_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.buy_thing(
                uid=frames_good_1_uid
            )
        self.assertEqual(
            frames_good_1_uid + ' is not for sale',
            str(cm.exception)
        )
        jeff_curr_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        # owner didn't change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')
        # buyer wasn't charged
        self.assertEqual(jeff_prev_currency_bal, jeff_curr_currency_bal)

        # balances not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 0)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)

    def test_04a_sell_thing_to(self):
        print("TEST SELL THING TO")
        self.change_signer('stu')


        self.con_pixel_frames_master.sell_thing_to(
            uid=frames_good_1_uid,
            amount=50,
            hold="ben"
        )

        # correct price set
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 50)
        # correct hold amount set
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'hold'])), 'ben')

    def test_04b_sell_thing_to_neg_negative_value(self):
        print("TEST SELL THING TO - NEG - AMOUNT IS NEGATIVE")
        self.change_signer('stu')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.sell_thing_to(
            uid=frames_good_1_uid,
            amount=-1,
            hold="ben"
        )
        self.assertEqual(
            'Cannot set a negative price',
            str(cm.exception)
        )
        # price did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 50)

    def test_04c_sell_thing_to_neg_not_owner(self):
        print("TEST SELL THING TO - NEG - NOT OWNER")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.sell_thing_to(
                uid=frames_good_1_uid,
                amount=1,
                hold='jeff'
            )
        self.assertEqual(
            frames_good_1_uid + ' not owned by jeff',
            str(cm.exception)
        )
        # price did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 50)

    def test_05a_buy_thing_on_hold_neg_on_hold_for_someone_else(self):
        print("TEST BUY THING ON HOLD - NEG - ON HOLD FOR SOMEONE ELSE")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.buy_thing(
                uid=frames_good_1_uid
            )
        self.assertEqual(
            frames_good_1_uid + ' is being held for ben',
            str(cm.exception)
        )
        # owner did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')

        # balances not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 0)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)

    def test_05b_buy_thing_on_hold(self):
        print("TEST BUY THING ON HOLD")
        self.change_signer('ben')
        stu_prev_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_prev_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        ben_prev_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        # print('stu_prev_currency_bal: ', stu_prev_currency_bal)
        # print('ben_prev_currency_bal: ', jeff_prev_currency_bal)

        self.con_pixel_frames_master.buy_thing(
            uid=frames_good_1_uid
        )
        stu_curr_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_curr_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        ben_curr_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        # print('stu_curr_currency_bal: ', stu_curr_currency_bal)
        # print('ben_curr_currency_bal: ', ben_curr_currency_bal)

        # price set back to zero (becomes un-buyable)
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 0)
        # hold sent to nothing
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'hold'])), "")
        # owner changes
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'ben')
        # creator doesn't change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'creator'])), 'jeff')
        # correct amount taken from ben for sale
        self.assertEqual(ben_prev_currency_bal - ben_curr_currency_bal, 50)
        # correct amount given to the creator jeff (20%)
        self.assertEqual(jeff_curr_currency_bal - jeff_prev_currency_bal, 10)
        # correct amount given to the owner stu (80%)
        self.assertEqual(stu_curr_currency_bal - stu_prev_currency_bal, 40)

        # balances updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 0)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['ben'])), 1)

    def test_06a_transfer(self):
        print("TEST TRANSFER")
        self.change_signer('ben')
        stu_prev_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        ben_prev_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        self.con_pixel_frames_master.transfer(
            uid=frames_good_1_uid,
            new_owner='stu'
        )
        stu_curr_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        ben_curr_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        # price still zero
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 0)
        # owner changes
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')
        # creator doesn't change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'creator'])), 'jeff')
        # giver's balance doesn't change
        self.assertEqual(ben_prev_currency_bal, ben_curr_currency_bal)
        # receiver's balance doesn't change
        self.assertEqual(stu_curr_currency_bal, stu_prev_currency_bal)

        # balances updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['ben'])), 0)

    def test_06b_transfer_neg_not_owner(self):
        print("TEST TRANSFER THING - NEG - NOT OWNER")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.transfer(
            uid=frames_good_1_uid,
            new_owner='jeff'
        )
        self.assertEqual(
            frames_good_1_uid + ' not owned by jeff',
            str(cm.exception)
        )
        # owner did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')

        # balances not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 0)

    def test_06c_transfer_neg_already_owned(self):
        print("TEST TRANSFER THING - NEG - ALREADY OWNED")
        self.change_signer('stu')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.transfer(
            uid=frames_good_1_uid,
            new_owner='stu'
        )
        self.assertEqual(
            frames_good_1_uid  + ' already owned by stu',
            str(cm.exception)
        )
        # owner did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')

        # balances not updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 1)


    def test_07a_like_thing(self):
        print("TEST LIKE THING")
        self.change_signer('jeff')
        self.con_pixel_frames_master.like_thing(
            uid=frames_good_1_uid
        )
        # added 1 like
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'likes'])), 1)
        # logged that jeff liked this specific thing
        self.assertEqual(self.con_pixel_frames_master.quick_read('S', (':').join(['liked', frames_good_1_uid, 'jeff'])), True)

    def test_07b_like_thing_neg_already_liked(self):
        print("TEST LIKE THING - NEG - ALREADY LIKED")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.like_thing(
                uid=frames_good_1_uid
            )
        self.assertEqual(
            'jeff already liked ' + frames_good_1_uid,
            str(cm.exception)
        )

        # no like added
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'likes'])), 1)

    def test_08a_prove_ownership(self):
        print("TEST PROVE OWNERSHIP")
        self.change_signer('stu')
        self.con_pixel_frames_master.prove_ownership(
                uid=frames_good_1_uid,
                code="testing"
            )
        # code added
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'proof'])), 'testing')

    def test_08b_prove_ownership_neg_not_owner(self):
        print("TEST PROVE OWNERSHIP - NEG - NOT OWNER")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.prove_ownership(
                uid=frames_good_1_uid,
                code="jeff-proof"
            )
        self.assertEqual(
            frames_good_1_uid  + ' not owned by jeff',
            str(cm.exception)
        )

        # code did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'proof'])), 'testing')


    def test_09a_transfer_from_neg_not_approved(self):
        print("TEST TRANSFER FROM - NEG - NOT APPROVED")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.transfer_from(
                uid=frames_good_1_uid,
                to="ben",
                main_account="stu"
            )
        self.assertEqual(
            "You have not been given approval to transfer this user's item.",
            str(cm.exception)
        )

        # owner did not change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'stu')

    def test_09b_transfer_from_neg_approve_not_owned(self):
        print("TEST APPROVAL - NEG - NOT OWNED")
        self.change_signer('jeff')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.approve(
                uid=frames_good_1_uid,
                to="ben"
            )
        self.assertEqual(
            frames_good_1_uid + ' not owned by jeff',
            str(cm.exception)
        )

        # approval did not change
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff', frames_good_1_uid, 'ben'])), None)

    def test_09c_approve(self):
        print("TEST APPROVAL")
        self.change_signer('stu')
        self.con_pixel_frames_master.approve(
            uid=frames_good_1_uid,
            to="jeff"
        )

        # approval added
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu', frames_good_1_uid, 'jeff'])), True)

    def test_09d_transfer_from(self):
        print("TEST TRANSFER FROM")
        self.change_signer('jeff')

        stu_prev_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_prev_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        ben_prev_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        # Approval exists
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu', frames_good_1_uid, 'jeff'])), True)

        # Transfer Stu's art to Ben on Stu's Behalf
        self.con_pixel_frames_master.transfer_from(
            uid=frames_good_1_uid,
            to="ben",
            main_account="stu"
        )

        stu_curr_currency_bal = self.currency_contract.quick_read('balances', 'stu')
        jeff_curr_currency_bal = self.currency_contract.quick_read('balances', 'jeff')
        ben_curr_currency_bal = self.currency_contract.quick_read('balances', 'ben')

        # approval revoked after the fact
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu', frames_good_1_uid, 'jeff'])), None)

        # price still zero
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'price', 'amount'])), 0)
        # owner changes
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'owner'])), 'ben')
        # creator doesn't change
        self.assertEqual(self.con_pixel_frames.quick_read('S', (':').join([frames_good_1_uid, 'creator'])), 'jeff')
        # giver's currency balance doesn't change
        self.assertEqual(ben_prev_currency_bal, ben_curr_currency_bal)
        # receiver's currency balance doesn't change
        self.assertEqual(stu_curr_currency_bal, stu_prev_currency_bal)
        # receiver's currency balance doesn't change
        self.assertEqual(jeff_curr_currency_bal, jeff_prev_currency_bal)

        # balances updated
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['stu'])), 0)
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['ben'])), 1)

        # balance didn't change
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['jeff'])), 0)

    def test_10a_revoke_approval(self):
        print("TEST APPROVAL")
        self.change_signer('ben')
        self.con_pixel_frames_master.approve(
            uid=frames_good_1_uid,
            to="stu"
        )

        # Approval is set
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['ben', frames_good_1_uid, 'stu'])), True)

        # Revoke approval
        self.con_pixel_frames_master.revoke(
            uid=frames_good_1_uid,
            to="stu"
        )

        # Approval is removed
        self.assertEqual(self.con_pixel_frames_master.quick_read('balances', (':').join(['ben', frames_good_1_uid, 'stu'])), None)

        # Attempt by Stu to transfer art does not work
        self.change_signer('stu')
        with self.assertRaises(AssertionError) as cm:
            self.con_pixel_frames_master.transfer_from(
                uid=frames_good_1_uid,
                to="stu",
                main_account="ben"
            )
        self.assertEqual(
            "You have not been given approval to transfer this user's item.",
            str(cm.exception)
        )


if __name__ == '__main__':
    unittest.main()