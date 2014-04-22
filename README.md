document_history
================

Adds history and versionning for MongoDB documents with mongoengine.
Saves all document changes in 'history' field inside the document, along 
with the timestamp of when the change was made, and all the fields that were updated.
It will save a record everytime a document is saved or updated.

Supports: MongoEngine

Installation:
-------------
`pip install document_history`


Usage:
------

Assuming you're connected to mongoengine:

```python
from mongoengine import Document, StringField
from document_history import save_history


@save_history
class Book(Document):
    title = StringField()
    caption = StringField()


document = Book(
    title="Mother Night",
    caption="We must be careful about what we pretend to be."
).save()

print document.history
# [
#         {
#             'timestamp': datetime.datetime(2014, 4, 22, 16, 27, 40, 715871), 
#             'changes': {
#                 'caption': u'We must be careful about what we pretend to be.', 
#                 'title': u'Mother Night'
#             }
#         }
# ]

document.title = "Cat's Cradle"

print document.history
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
```
