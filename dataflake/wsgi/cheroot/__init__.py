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
from cheroot import wsgi


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

    server = wsgi.Server(address, app)
    server.start()
    return 0
