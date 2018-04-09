import piecash

book = piecash.create_book(
    keep_foreign_keys=True,
    uri_conn="mysql+pymysql://cohirer:Letsgo!@localhost/pieledger?charset=utf8&use_unicode=0",
    overwrite=True
)

acc = piecash.Account(
    name="My account",
    type="ASSET",
    parent=book.root_account,
    commodity=book.commodities.get(mnemonic="EUR"),
    placeholder=True)

book.save()
