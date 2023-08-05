from ingaia.commons.exceptions import GenericException


class ProjectReferenceNotDefinedException(GenericException):
    message = 'Define the google cloud project using the "ProjectReference" class.'


class SchemaNotDefinedException(GenericException):
    message = 'Define the bigquery schema.'


class QueryIsNoneException(GenericException):
    message = 'Query is None'


class NoBlobSetException(GenericException):
    message = 'Blob must be set. Use "set_blob([file_name])" method.'


class BigQueryCheckingException(GenericException):
    message = 'There is something wrong with the schema definition or with existing bigquery table.'


class DifferentTableSchemaException(GenericException):
    message = 'The existing table schema is different than the definition schema. ' \
              'To recreate the table, delete that from database.'


class BigQueryException(Exception):
    def __init__(self, message=None):
        super(BigQueryException, self).__init__(message)
