import piecash

book = piecash.create_book(
    uri_conn="mysql+pymysql://cohirer:Letsgo!@localhost/cohirer_dev?charset=utf8&use_unicode=0", overwrite=True)
book.save()
