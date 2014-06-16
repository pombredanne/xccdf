# -*- coding: utf-8 -*-


class InvalidValueException(Exception):

    """
    This exception is raised when an Element has an invalid value

    :param str value: Exception message
    """

    #: Default message value
    value = 'The value of the element is not valid'

    def __init__(self, value=None):

        if value is not None:
            self.value = value

    def __str__(self):
        """
        String representation of the exception

        :returns: Exception message as string
        :rtype: str
        """

        return self.value


class RequiredAttributeException(Exception):

    """
    This exception is raised when an Element has a missing attribute

    :param str value: Exception message
    """

    #: Default message value
    value = 'The required attribute is missing'

    def __init__(self, value=None):

        if value is not None:
            self.value = value

    def __str__(self):
        """
        String representation of the exception

        :returns: Exception message as string
        :rtype: str
        """

        return self.value


class CardinalityException(Exception):

    """
    This exception is raised when a children doesn't comply
    to the parent cardinality rules

    :param str value: Exception message
    """

    #: Default message value
    value = 'This element is invalid based on '\
            'the cardinality rules of the parent'

    def __init__(self, value=None):

        if value is not None:
            self.value = value

    def __str__(self):
        """
        String representation of the exception

        :returns: Exception message as string
        :rtype: str
        """

        return self.value
