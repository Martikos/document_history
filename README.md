MongoDB Document Changes History
================================

This package offers you a class decorator (`@save_history`) that you can 
maintain the document field changes inside a `history` field inside the document.
`history` is saved as a list of dictionaries, each object inside the list has:
   * `timestamp`: specifies when the changes were made
   * `changes`: a dictionary that maintains the changes, the keys represent the 
        names of the fields changed, the values represent the values they were
        changed to.

The `history` list of records will update whenever a document is saved or is updated.

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
document.save()

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
