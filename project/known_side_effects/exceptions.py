class UnmatchedArguments(Exception):

    ERROR_MSG = 'Unexpected call to mock with args=({args}) kwargs=({kwargs})'

    def __init__(self, *args, **kwargs):
        super().__init__(
            UnmatchedArguments.ERROR_MSG.format(
                args=args,
                kwargs=kwargs,
            )
        )
