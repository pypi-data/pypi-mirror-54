


class DynamofException(Exception):
   def __init__(self, message):
       self.message = message
       super().__init__(message)
   def info(self, add_message):
       """ Adds details to the base error message"""
       self.message = f'{self.message}; {add_message}'
       return self

class PreexistingTableException(DynamofException):
    def __init__(self):
        message = "Attempted to create a table that already exists"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        key = 'Cannot create preexisting table'
        return err.response.get('Error', {}).get('Message') == key

class TableDoesNotExistException(DynamofException):
    def __init__(self):
        message = "Attempted to do operation on a table that does not exist"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        key = 'Cannot do operations on a non-existent table'
        return err.response.get('Error', {}).get('Message') == key

class ConditionNotMetException(DynamofException):
    def __init__(self):
        message = "Could not find an item that satisifed the given conditions"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        if err is not None and hasattr(err, 'response'):
          return err.response.get('Error', {}).get('Code', '') == 'ConditionalCheckFailedException'
        return False

class BadGatewayException(DynamofException):
    def __init__(self):
        message = "Issue communicating with dynamo"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        return err is not None and err.response.get('Error').get('Message') == 'Bad Gateway'

class UnknownDatabaseException(DynamofException):
    def __init__(self):
        message = "An unkonwn exception occured when executing request to dynamo"
        super().__init__(message)
