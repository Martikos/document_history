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
        super(cls, instance).__init__(args, kwargs)
    cls.__init__ = __init__

    def history_changes(self):
        """ Returns a list of history changes sorted by date.
        """
        return sorted(history, key=lambda record: record['timestamp'])
    cls.history_changes = history_changes

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """ Saves timestamp and modified fields in history.
        """
        document.updated_on = datetime.now()
        delta = dict(document._delta()[0])
        delta['timestamp'] = datetime.now()
        document.history.append(delta)
    cls.pre_save = pre_save

    signals.pre_save.connect(cls.pre_save, sender=cls)

    return cls

