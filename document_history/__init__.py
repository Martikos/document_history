from mongoengine import *
from mongoengine import signals
from datetime import datetime


def save_history(cls):
    """ Class decorator that adds the 'history' field to the MongoDB model document.
    """

    cls._fields['history'] = ListField(DictField, default=[])
    cls._fields['last_updated'] = DateTimeField()
    cls._fields['history_index'] = IntField()

    def __init__(instance, *args, **kwargs):
        """ Initializes empty list of history records, then calls original __init__.
        """
        instance.history = []
        instance.history_index = 0
        super(cls, instance).__init__(*args, **kwargs)
    cls.__init__ = __init__

    def save(instance, *args, **kwargs):

        super(cls, instance).save(*args, **kwargs)


    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """ Saves timestamp and modified fields in history.
        """
        now = datetime.now()

        delta = dict(document._delta()[0])

        if document.history_index < len(document.history):
            document.history = document.history[:document.history_index]
            document.last_updated = now
        else:
            if any(delta):
                document.history.append({
                    'timestamp': now, 
                    'changes': delta
                })
                document.history_index += 1
    cls.pre_save = pre_save

    def revert_to(instance, commit_index):
        """ Reverts your document back to index specified by commit_index.
        """
        history = instance.history
        changes = dict()

        if commit_index > len(history):
            return instance

        for index in range(commit_index):
            record = history[index]
            for key, value in record['changes'].iteritems():
                changes[key] = value

        new_instance = instance.__class__(**changes)

        new_instance['history'] = instance.history
        new_instance['last_updated'] = instance.last_updated 
        new_instance['history_index'] = commit_index

        print new_instance.history_index, new_instance.title, new_instance.caption

        instance = new_instance
        return instance

    cls.revert_to = revert_to




    signals.pre_save.connect(cls.pre_save, sender=cls)

    return cls

