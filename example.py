import os

import mongoengine
from mongoengine import Document, StringField
from document_history import save_history


def establish_mongo_connection():
    mongo_name = os.environ.get('DH_MONGO_DB_NAME', 'test_document_history')
    mongo_port = int(os.environ.get('DH_MONGO_DB_PORT', 27017))
    mongoengine.connect(mongo_name, port=mongo_port)


establish_mongo_connection()


@save_history
class Book(Document):
    title = StringField()
    caption = StringField()


book = Book(
    title="Mother Night",
    caption="We must be careful about what we pretend to be."
).save()


history = book.history
print history
# [
#         {
#             'timestamp': datetime.datetime(2014, 4, 22, 16, 27, 40, 715871), 
#             'changes': {
#                 'caption': u'We must be careful about what we pretend to be.', 
#                 'title': u'Mother Night'
#             }
#         }
# ]

book.title = "Cat's Cradle"
book.save()

history = book.history
print history
# [
#         {
#             'timestamp': datetime.datetime(2014, 4, 22, 16, 29, 29, 873231), 
#             'changes': {
#                 'caption': u'We must be careful about what we pretend to be.', 
#                 'title': u'Mother Night'
#             }
#         }, 
#         {
#             'timestamp': datetime.datetime(2014, 4, 22, 16, 29, 29, 874008), 
#             'changes': {
#                 'title': u"Cat's Cradle"
#             }
#         }
# ]

