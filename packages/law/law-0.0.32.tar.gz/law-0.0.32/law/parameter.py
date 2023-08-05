# coding: utf-8

"""
Custom luigi parameters.
"""


__all__ = [
    "NO_STR", "NO_INT", "NO_FLOAT", "is_no_param", "get_param", "TaskInstanceParameter",
    "CSVParameter", "NotifyParameter", "NotifyMultiParameter", "NotifyMailParameter",
]


import luigi

from law.notification import notify_mail


# make luigi's BoolParameter parsing explicit globally, https://github.com/spotify/luigi/pull/2427
luigi.BoolParameter.parsing = getattr(luigi.BoolParameter, "EXPLICIT_PARSING", "explicit")

# also update existing BoolParameter instances in luigi's config classes to have explicit parsing
for cls in luigi.task.Config.__subclasses__():
    for attr in dir(cls):
        member = getattr(cls, attr)
        if isinstance(member, luigi.BoolParameter):
            member.parsing = luigi.BoolParameter.parsing

#: String value denoting an empty parameter.
NO_STR = "NO_STR"

#: Integer value denoting an empty parameter.
NO_INT = -1

#: Float value denoting an empty parameter.
NO_FLOAT = -1.


def is_no_param(value):
    """
    Checks whether a parameter *value* denotes an empty parameter, i.e., if the value is either
    :py:attr:`NO_STR`, :py:attr:`NO_INT`, or :py:attr:`NO_FLOAT`.
    """
    return value in (NO_STR, NO_INT, NO_FLOAT)


def get_param(value, default=None):
    """
    Returns the passed *value* when it does not refer to an empty parameter value, checked with
    :py:func:`is_no_param`. Otherwise, *default* is returned, which defaults to *None*.
    """
    return default if is_no_param(value) else value


class TaskInstanceParameter(luigi.Parameter):
    """
    Parameter that can be used pass the instance of a task. This class does not implement parameter
    value parsing.
    """

    def serialize(self, x):
        """"""
        return str(x)


class CSVParameter(luigi.Parameter):
    """
    Parameter that can be parsed from a comma-separated value (CSV). *cls* can refer to an other
    luigi parameter class that will be used to parse and serialize the particular items. Example:

    .. code-block:: python

        p = CSVParameter(cls=luigi.IntParameter, default=[1, 2, 3])

        p.parse("4,5,6")
        # => [4, 5, 6]

        p.serialize([7, 8, 9])
        # => "7,8,9"

    .. py:attribute:: _inst
       type: cls

        Instance of the luigi parameter class *cls* that is used internally for parameter parsing
        and serialization.
    """

    def __init__(self, *args, **kwargs):
        """ __init__(cls=luigi.Parameter, *args, **kwargs) """
        cls = kwargs.pop("cls", luigi.Parameter)

        super(CSVParameter, self).__init__(*args, **kwargs)

        self._inst = cls()

    def parse(self, inp):
        """"""
        if not inp:
            return []
        else:
            return [self._inst.parse(elem) for elem in inp.split(",")]

    def serialize(self, value):
        """"""
        if not value:
            return ""
        else:
            return ",".join(str(self._inst.serialize(elem)) for elem in value)


class NotifyParameter(luigi.BoolParameter):
    """
    Base class for notification parameters. A notification parameter must provide a notification
    transport in :py:meth:`get_transport`, e.g.

    .. code-block:: python

        def get_transport(self):
            return {
                "func": notification_func,
                "raw": True,  # or False
            }

    When a task has a specific notification parameter set to *True* and its run method is decorated
    with the :py:func:`law.notify` function, *notification_func* is called with at least three
    arguments: *success*, *title* and *message*. *success* is a boolean which is *True* when the
    decorated function did not raise an exception. *title* is always a string. When *raw* is *False*
    (the default), *message* is also a string. Otherwise, it is an ordered dictionary containing key
    value pairs describing the message content. All options passed to
    :py:func:`law.decorator.notify` are forwarded to *notification_func* as optional arguments.
    """

    def get_transport(self):
        """
        Method to configure the transport that is toggled by this parameter. Should return a
        dictionary with ``"func"`` and ``"raw"`` (optional) fields.
        """
        return None


class NotifyMultiParameter(NotifyParameter):
    """
    Parameter that takes multiple other :py:class:`NotifyParameter`'s to join their notification
    functionality in a single parameter. Example:

    .. code-block:: python

        class MyTask(law.Task):

            notify = law.NotifyMultiParameter(parameters=[
                law.NotifyMailParameter(significant=False),
                ...  # further NotifyParameters
            ])
    """

    def __init__(self, *args, **kwargs):
        """ __init__(parameters=[], *args, **kwargs) """
        self.parameters = kwargs.pop("parameters", [])

        super(NotifyMultiParameter, self).__init__(*args, **kwargs)

    def get_transport(self):
        """"""
        return [param.get_transport() for param in self.parameters]


class NotifyMailParameter(NotifyParameter):
    """
    Notification parameter defining a basic email transport. Uses
    :py:meth:`law.notification.notify_mail` internally.
    """

    def __init__(self, *args, **kwargs):
        super(NotifyMailParameter, self).__init__(*args, **kwargs)

        if not self.description:
            self.description = "when true, and the task's run method is decorated with " \
                "law.decorator.notify, an email notification is sent once the task finishes"

    @classmethod
    def notify(success, *args, **kwargs):
        """"""
        return notify_mail(*args, **kwargs)

    def get_transport(self):
        """"""
        return {
            "func": self.notify,
            "raw": False,
        }
