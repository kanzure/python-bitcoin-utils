# Copyright (C) 2018 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, P2wshAddress, P2wpkhAddress
from bitcoinutils.script import Script


def main():
    # always remember to setup the network
    setup('testnet')

    priv = PrivateKey("cVdte9ei2xsVjmZSPtyucG43YZgNkmKTqhwiUA8M4Fc3LdPJxPmZ")

    pub = priv.get_public_key()

    fromAddress = pub.get_segwit_address()
    print(fromAddress.to_string())

    # amount is needed to sign the segwit input
    fromAddressAmount = 0.01

    # UTXO of fromAddress
    txid = '13d2d30eca974e8fa5da11b9608fa36905a22215e8df895e767fc903889367ff'
    vout = 0

    toAddress = P2pkhAddress('mrrKUpJnAjvQntPgz2Z4kkyr1gbtHmQv28')

    # create transaction input from tx id of UTXO
    txin = TxInput(txid, vout)
    # the redeem script for p2wpkh is the same as p2pkh
    redeem_script = Script(['OP_DUP', 'OP_HASH160',
                            priv.get_public_key().to_hash160(),
                            'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    # create transaction output
    txOut = TxOutput(0.009, toAddress.to_script_pub_key())

    # create transaction without change output
    tx = Transaction([txin], [txOut], has_segwit=True)

    print("\nRaw transaction:\n" + tx.serialize())

    sig = priv.sign_segwit_input(tx, 0, redeem_script, fromAddressAmount)
    tx.witnesses.append( Script([sig, pub.to_hex()]) )

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())


if __name__ == "__main__":
    main()
