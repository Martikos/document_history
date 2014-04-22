import os

import nose
from nose.tools import *
from nose.tools import assert_raises

from mongoengine import Document, StringField
from mongoengine.connection import _get_db


try:
    import mongoengine
except ImportError:
    mongoengine = None


def establish_mongo_connection():
    mongo_name = os.environ.get("DH_MONGO_DB_NAME", "test_document_history")
    mongo_port = int(os.environ.get("DH_MONGO_DB_PORT", 27017))
    mongoengine.connect(mongo_name, port=mongo_port)


from document_history import save_history

def requires_mongoengine(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if mongoengine is None:
            raise SkipTest("mongoengine is not installed")
        return func(*args, **kw)

    return wrapper


def test_document_history():

    @save_history
    class Book(Document):
        title = StringField()
        caption = StringField()

    establish_mongo_connection()

    book = Book()
    title_string = "Mother Night"
    book.title = title_string
    book.save()

    history = book.history
    eq_(len(history), 1)
    eq_(history[0]["changes"]["title"], title_string)


    caption_string = "We must be careful about what we pretend to be."

    book.caption = caption_string
    book.save()

    history = book.history

    eq_(len(history), 2)
    eq_(history[1]["changes"]["caption"], caption_string)


    # Clear database
    db = _get_db()
    collection_names = [c for c in db.collection_names() if not c.startswith("system.")]
    for collection in collection_names:
        db.drop_collection(collection)



