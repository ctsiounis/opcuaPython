'''
Created on Aug 22, 2018

@author: ktsiouni
'''

import sys
sys.path.insert(0, "..")
import time

from opcua import ua, uamethod, Server

@uamethod
def multiply(parent, x, y):
    print("multiply method call with parameters: ", x, y)
    return x * y

if __name__ == '__main__':
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "urn:ca:uwo:test-module"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "TestFolder")
    for i in range(5):
        myvar = myobj.add_variable(idx, "TestVariable_1_"+str(i), 6.7)
        myvar.set_writable()    # Set MyVariable to be writable by clients

    # creating a method node
    inargx = ua.Argument()
    inargx.Name = "x"
    inargx.DataType = ua.NodeId(ua.ObjectIds.Int64)
    inargx.ValueRank = -1
    inargx.ArrayDimensions = []
    inargx.Description = ua.LocalizedText("First number x")
    inargy = ua.Argument()
    inargy.Name = "y"
    inargy.DataType = ua.NodeId(ua.ObjectIds.Int64)
    inargy.ValueRank = -1
    inargy.ArrayDimensions = []
    inargy.Description = ua.LocalizedText("Second number y")
    outarg = ua.Argument()
    outarg.Name = "Result"
    outarg.DataType = ua.NodeId(ua.ObjectIds.Int64)
    outarg.ValueRank = -1
    outarg.ArrayDimensions = []
    outarg.Description = ua.LocalizedText("Multiplication result")

    multiply_node = myobj.add_method(idx, "multiply", multiply, [inargx, inargy], [outarg])
    # starting!
    server.start()
    
    try:
        while True:
            time.sleep(1)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()