#!/usr/bin/python3

# Copyright (c) 2017 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""Reference tests for segwit adresses"""

import unittest
import riemann
from ...encoding import bech32


def segwit_scriptpubkey(witver, witprog):
    """Construct a Segwit scriptPubKey for a given witness program."""
    return bytes([witver + 0x50 if witver else 0, len(witprog)] + witprog)


VALID_CHECKSUM = [
    "A12UEL5L",
    "an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1tt5tgs",  # noqa: E501
    "abcdef1qpzry9x8gf2tvdw0s3jn54khce6mua7lmqqqxw",
    "11qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqc8247j",  # noqa: E501
    "split1checkupstagehandshakeupstreamerranterredcaperred2y9e3w",
]


INVALID_CHECKSUM = [
    " 1nwldj5",
    "\x7F" + "1axkwrx",
    "an84characterslonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1569pvx",  # noqa: E501
    "pzry9x0s0muk",
    "1pzry9x0s0muk",
    "x1b4n0q5v",
    "li1dgmt3",
    "de1lg7wt\xff",
]


VALID_ADDRESS = [
    ["BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4", "0014751e76e8199196d454941c45d1b3a323f1433bd6"],  # noqa: E501
    ["tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7",
     "00201863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262"],
    ["bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7k7grplx",  # noqa: E501
     "5128751e76e8199196d454941c45d1b3a323f1433bd6751e76e8199196d454941c45d1b3a323f1433bd6"],  # noqa: E501
    ["BC1SW50QA3JX3S", "6002751e"],
    ["bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj", "5210751e76e8199196d454941c45d1b3a323"],  # noqa: E501
    ["tb1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesrxh6hy",
     "0020000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433"],
]

INVALID_ADDRESS = [
    "tc1qw508d6qejxtdg4y5r3zarvary0c5xw7kg3g4ty",
    "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5",
    "BC13W508D6QEJXTDG4Y5R3ZARVARY0C5XW7KN40WF2",
    "bc1rw5uspcuh",
    "bc10w508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kw5rljs90",  # noqa: E501
    "BC1QR508D6QEJXTDG4Y5R3ZARVARYV98GJ9P",
    "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sL5k7",
    "bc1zw508d6qejxtdg4y5r3zarvaryvqyzf3du",
    "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3pjxtptv",
    "bc1gmk9yu",

]

INVALID_ADDRESS_ENC = [
    ("BC", 0, 20),
    ("bc", 0, 21),
    ("bc", 17, 32),
    ("bc", 1, 1),
    ("bc", 16, 41),
]


class TestBech32(unittest.TestCase):
    """Unit test class for segwit addressess."""

    def tearDown(self):
        riemann.select_network('bitcoin_main')

    def test_valid_checksum(self):
        """Test checksum creation and validation."""
        for t in VALID_CHECKSUM:
            hrp, _ = bech32.bech32_decode(t)
            self.assertIsNotNone(hrp)
            pos = t.rfind('1')
            t = t[:pos + 1] + chr(ord(t[pos + 1]) ^ 1) + t[pos + 2:]
            hrp, _ = bech32.bech32_decode(t)
            self.assertIsNone(hrp)

    def test_invalid_checksum(self):
        """Test validation of invalid checksums."""
        for test in INVALID_CHECKSUM:
            hrp, _ = bech32.bech32_decode(test)
            self.assertIsNone(hrp)

    def test_valid_address(self):
        """Test whether valid addresses decode to the correct output."""
        for (address, hexscript) in VALID_ADDRESS:
            hrp = "bc"
            witver, witprog = bech32.segwit_decode(hrp, address)
            if witver is None:
                hrp = "tb"
                witver, witprog = bech32.segwit_decode(hrp, address)
            self.assertIsNotNone(witver)
            scriptpubkey = segwit_scriptpubkey(witver, witprog)
            self.assertEqual(scriptpubkey, bytearray.fromhex(hexscript))
            addr = bech32.segwit_encode(hrp, witver, witprog)
            self.assertEqual(address.lower(), addr)

    def test_invalid_address(self):
        """Test whether invalid addresses fail to segwit_decode."""
        for test in INVALID_ADDRESS:
            witver, _ = bech32.segwit_decode("bc", test)
            self.assertIsNone(witver)
            witver, _ = bech32.segwit_decode("tb", test)
            self.assertIsNone(witver)

    def test_invalid_address_enc(self):
        """Test whether address encoding fails on invalid input."""
        for hrp, version, length in INVALID_ADDRESS_ENC:
            code = bech32.segwit_encode(hrp, version, [0] * length)
            self.assertIsNone(code)

    def test_encode_error(self):
        riemann.select_network('zcash_sprout_main')
        with self.assertRaises(ValueError) as context:
            bech32.encode(bytearray([0] * 32))

        self.assertIn(
            'Network (zcash_sprout_main) does not support bech32 encoding.',
            str(context.exception))

    def test_decode_error(self):
        riemann.select_network('zcash_sprout_main')
        with self.assertRaises(ValueError) as context:
            bech32.decode(bytearray([0] * 32))

        self.assertIn(
            'Network (zcash_sprout_main) does not support bech32 encoding.',
            str(context.exception))

    def test_convert_bits_error(self):
        self.assertIsNone(bech32.convertbits([2 ** 5 + 1], 5, 8))
