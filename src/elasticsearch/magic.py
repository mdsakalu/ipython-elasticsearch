"""Elasticearch IPython magic."""
from __future__ import absolute_import, print_function

import json
import os
import urllib.parse

from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import requests

from . import notebook as nb


@magics_class
class ElasticsearchMagics(Magics):
    def __init__(self, **kwargs):
        self._base_url = 'http://localhost:9200/'
        nb.output_notebook()
        super().__init__(**kwargs)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value
        print('Using: {}'.format(self.base_url))

    @needs_local_scope
    @line_cell_magic
    @magic_arguments()
    @argument('base_url', type=str, nargs='?', default=None, help='Elasticsearch URL.')
    @argument("-o", "--output", type=str, default={}, help="save result to variable of this name")
    def elasticsearch(self, line, cell=None, local_ns=None):
        "elasticsearch line magic"
        args = parse_argstring(self.elasticsearch, line)
        cell_base_url = args.base_url if args.base_url else self.base_url

        if not cell:
            self.base_url = cell_base_url
        else:
            line1 = (cell + os.linesep).find(os.linesep)
            method, path = cell[:line1].split(None, 1)
            body = cell[line1:].strip()
            if method in ("POST", "PUT") and path.rsplit("/", 1)[-1].startswith("_bulk"):
                body += "\n"
            request_args = {}
            if body:
                request_args['data'] = body
                # maybe not always?
                request_args['headers'] = {'Content-Type': 'application/json'}

            session = requests.Session()
            rsp = session.send(requests.Request(method=method,
                                                url=urllib.parse.urljoin(cell_base_url, path),
                                                **request_args).prepare())
            try:
                if args.output:
                    local_ns[args.output] = rsp.json()
                    nb.output_cell(local_ns[args.output])
                else:
                    nb.output_cell(rsp.json())
            except json.JSONDecodeError:
                # TODO: parse charset out of response eg: 'application/json; charset=UTF-8'
                # >>> requests.get("http://localhost:9200/_search").headers['Content-Type']
                # 'application/json; charset=UTF-8'
                # >>> requests.get("http://localhost:9200/_cat").headers['Content-Type']
                # 'text/plain; charset=UTF-8'
                if args.output:
                    local_ns[args.output] = rsp.content.decode('UTF-8')
                    print(local_ns[args.output])
                else:
                    print(rsp.content.decode('UTF-8'))  # ES [probably] always returns utf-8
            return rsp


def load_ipython_extension(ipy):
    ipy.register_magics(ElasticsearchMagics)
