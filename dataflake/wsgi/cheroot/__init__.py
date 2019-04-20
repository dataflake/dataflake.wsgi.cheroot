##############################################################################
#
# Copyright (c) 2019 Jens Vagelpohl and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import logging

from cheroot import wsgi


CHEROOT_ERROR_LOGGER = logging.getLogger('cheroot.error')


class LoggingWSGIServer(wsgi.Server):
    """ Fix up how cheroot does logging """

    def error_log(self, msg='', level=logging.INFO, traceback=False):
        """ Log error messages

        Overridden to use the Python logging module instead of sys.stderr

        Args:
            msg (str): error message
            level (int): logging level
            traceback (bool): add traceback to output or not
        """
        CHEROOT_ERROR_LOGGER.log(level, msg, exc_info=traceback)


def serve_paste(app, global_conf, **kw):
    """ A handler for PasteDeploy-compatible runners.

    Sample .ini configuration:

      [server:main]
      use = egg:dataflake.wsgi.cheroot#main
      host = 127.0.0.1
      port = 8080

    If you don't provide a host value, the server will listen on all IPv4
    interfaces.
    If you don't provide a port value, the server will listen on port 8080.
    """
    host = kw.get('host', '0.0.0.0')
    port = kw.get('port', '8080')
    address = (host, int(port))

    server = LoggingWSGIServer(address, app)
    try:
        server.start()
    except KeyboardInterrupt:
        # Without this explicit exception handler, the server cannot be stopped
        # with <CTRL-C> when it runs in the foreground.
        server.stop()
    return 0
