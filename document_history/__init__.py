from mongoengine import *
from mongoengine import signals
from datetime import datetime


def save_history(cls):
    """ Class decorator that adds the 'history' field to the MongoDB model document.
    """

    cls._fields['history'] = ListField(DictField, default=[])


    def __init__(instance, *args, **kwargs):
        """ Initializes empty list of history records, then calls original __init__.
        """
        instance.history = []
        super(cls, instance).__init__(*args, **kwargs)
    cls.__init__ = __init__


    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """ Saves timestamp and modified fields in history.
        """
        document.updated_on = datetime.now()
        delta = dict(document._delta()[0])
        record = dict()
        record['timestamp'] = datetime.now()
        record['changes'] = delta
        document.history.append(record)
    cls.pre_save = pre_save


    signals.pre_save.connect(cls.pre_save, sender=cls)

    return cls

