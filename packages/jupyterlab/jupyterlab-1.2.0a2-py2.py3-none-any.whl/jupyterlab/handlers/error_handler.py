# coding: utf-8
"""An error handler for JupyterLab."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from tornado import web
from jupyterlab_server.server import JupyterHandler


TEMPLATE = """
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8">
    <title>JupyterLab Error</title>
</head>
<body>
<h1>JupyterLab Error<h1>
%s
</body>
"""

class ErrorHandler(JupyterHandler):

    def initialize(self, messages):
        self.messages = messages

    @web.authenticated
    @web.removeslash
    def get(self):
        msgs = ['<h2>%s</h2>' % msg for msg in self.messages]
        self.write(TEMPLATE % '\n'.join(msgs))
