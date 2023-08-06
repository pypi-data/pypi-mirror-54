"""
make modules a little bit easier to use.
"""
from bs4 import BeautifulSoup as BSoup


class BeautifulSoup(BSoup):
    
    def __init__(self, ifile, ftype='file', parser='html.parser', **kwargs):
        if ftype == 'file':
            from . import read_and_write_basic
            html = read_and_write_basic.read_file(ifile)
        else:
            # ftype is 'str' or 'string'
            html = ifile
        
        super().__init__(html, parser, **kwargs)

    def insert_before(self, successor):
        pass

    def insert_after(self, successor):
        pass
