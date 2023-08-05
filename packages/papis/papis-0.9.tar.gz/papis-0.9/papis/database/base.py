"""
Here the database abstraction for the libraries is defined.
"""

import papis.utils
import papis.config
import papis.library


class Database(object):
    """Abstract class for the database backends
    """

    def __init__(self, library=None):
        self.lib = library or papis.config.get_lib()
        assert(isinstance(self.lib, papis.library.Library))

    def initialize(self):
        raise NotImplementedError('Initialize not implemented')

    def get_backend_name(self):
        raise NotImplementedError('Get backend name not implemented')

    def get_lib(self):
        """Get library name
        """
        return self.lib.name

    def get_dirs(self):
        """Get directories of the library
        """
        return self.lib.paths

    def match(self, document, query_string):
        """Wether or not document matches query_string

        :param document: Document to be matched
        :type  document: papis.document.Document
        :param query_string: Query string
        :type  query_string: str
        """
        raise NotImplementedError('Match not implemented')

    def clear(self):
        raise NotImplementedError('Clear not implemented')

    def add(self, document):
        raise NotImplementedError('Add not implemented')

    def update(self, document):
        raise NotImplementedError('Update not implemented')

    def delete(self, document):
        raise NotImplementedError('Delete not implemented')

    def query(self, query_string):
        raise NotImplementedError('Query not implemented')

    def query_dict(self, query_string):
        raise NotImplementedError('Query dict not implemented')

    def get_all_documents(self):
        raise NotImplementedError('Get all docs not implemented')

    def get_all_query_string(self):
        raise NotImplementedError('Get all query string not implemented')
