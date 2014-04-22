document_history
================

Adds history and versioning for MongoDB documents using mongoengine


Installation:
-------------


Usage:
------

Assuming you're connected to mongoengine:

```python
from mongoengine import Document, StringField
from document_history import save_history

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
```
