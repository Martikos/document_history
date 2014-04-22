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

@save_history
class ImportantDocument(Document):
    title = StringField()
    
    
my_doc = ImportantDocument()
my_doc.title = "Life Is Good"
my_doc.save()

```
