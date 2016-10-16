import xmlrpclib

#pripojeni k xmlrpc serveru
server = xmlrpclib.ServerProxy("http://172.16.34.157:8870")

#nasledne se s nim da pracovat jako se tridou svetelnypanel na panelu
server.test()
