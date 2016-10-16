import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
import svetelny_panel as sp


XmlRpcServer = SimpleXMLRPCServer(("172.16.34.157",8870),allow_none=True)
XmlRpcServer.register_instance(sp)


try:
    print "jede to "
    try:
        sp.showtext("Startuji...")
    except:
        pass
    sp.showtext("Svetelny panel XMLRPC bezi na portu 8870","00ff00")
    sp.showtext("XMLRPC na portu 8870","00ff00")
    XmlRpcServer.serve_forever()
except KeyboardInterrupt:
    XmlRpcServer.server_close()
    sp.showtext("Tak uz to spadlo. XMLRPC nejede!","ff0000")

print "ukonceno"
