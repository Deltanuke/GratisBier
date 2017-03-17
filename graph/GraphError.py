class GraphError(Exception):
    """
    An error that occurs while manipulating a `Graph`
    """

    def __init__(self, message: str):
        """
        Constructor
        :param message: The error message
        :type message: str
        """
        super(GraphError, self).__init__(message)