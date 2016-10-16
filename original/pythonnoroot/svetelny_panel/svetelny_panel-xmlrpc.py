import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer

import svetelny_panel as sp


XmlRpcServer = SimpleXMLRPCServer(("172.16.34.157",8869))
XmlRpcServer.register_instance(sp)
XmlRpcServer.serve_forever()

