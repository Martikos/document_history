import os

import nose
from nose.tools import *
from nose.tools import assert_raises

from mongoengine import Document, StringField


try:
    import mongoengine
except ImportError:
    mongoengine = None


def establish_mongo_connection():
    mongo_name = os.environ.get('DH_MONGO_DB_NAME', 'test_document_history')
    mongo_port = int(os.environ.get('DH_MONGO_DB_PORT', 27017))
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
    class VeryImportantDocument(Document):
        title = StringField()
        comment = StringField()

    establish_mongo_connection()

    vid = VeryImportantDocument()
    title_string = "Mother Night"
    vid.title = title_string
    vid.save()

    history = vid.history
    eq_(len(history), 1)
    eq_(history[0]['changes']['title'], title_string)


    comment_string = "We must be careful about what we pretend to be."

    vid.comment = comment_string
    vid.save()

    history = vid.history
    eq_(len(history), 2)
    eq_(history[1]['changes']['comment'], comment_string)



