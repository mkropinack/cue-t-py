from pythonosc import udp_client

class OSC_PILOT():

    def __init__( self, targetInfo ):
        self.data = targetInfo
        self.OSCclient = udp_client.SimpleUDPClient(targetInfo["ip"], int(targetInfo["port"]))

    def setParam( self, param):
        result = ""
        match param["param"]:
            case "text_data": result = self.setTextData( param )
            case _: result = "Invalid Parameter [{}]".format( param["param"] )
        return result
    
    def setTextData( self, param):
        obj_addr_str = "/text/{}/data".format(param["index"])
        print("DEBUG : address = {} | value = {} ".format(obj_addr_str, param["value"]))
        self.OSCclient.send_message(obj_addr_str, param["value"])
        
