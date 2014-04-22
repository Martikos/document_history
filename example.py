import mongoengine

mongoengine.connect(
        'mongo-history',
        host='localhost',
        port=27017,
        username=None,
        password=None)



@save_history
class ImportantDocument(Document):
    field_1 = StringField()
    field_2 = StringField()


oo = A()
oo.field_1 = 'new entry'
oo.save()

