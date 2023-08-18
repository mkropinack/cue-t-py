from pythonosc import udp_client

class OSC_M32():

    CONFIG_NAME_MAXLEN = 12
    CONFIG_COLORS = ["OFF", "RD", "GN", "YE", "BL", "MG", "CY", "WH", "OFFi", "RDi", "GNi", "YEi", "BLi", "MGi", "CYi", "WHi"]

    CHN_VALID_IDS = [ "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16",
                      "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32" ]
    MTX_VALID_IDS = [ "01", "02", "03", "04", "05", "06", "07", "08" ]
    DCA_VALID_IDS = [ "01", "02", "03", "04", "05", "06", "07", "08" ]

    def __init__( self, targetInfo ):
        self.data = targetInfo
        self.OSCclient = udp_client.SimpleUDPClient(targetInfo["ip"], int(targetInfo["port"]))

    def _debug( self ):
        pass

    # setParam - setParam issues individual configuration and parameter changes to the Audio console.
    # These commands are not conditional, and are issued regardless of the state of the console.
    # No information is returned from the console, and the previous state of the parameter is not saved.
    # These are intended to be used as building blocks for more complicated cues.

    def setParam( self, param):
        result = ""
        match param["param"]:
            case "channel_config_name": result = self.setConfigName( param )
            case "channel_config_color": result = self.setConfigColor( param )
            case "channel_config_icon": result = self.setConfigIcon( param )
            case "channel_config_source": result = self.setChannelConfigSource( param )
            case "channel_group_dca": result = self.setChannelGroupDCA( param )
            case "channel_on_off": result = self.setChannelOnOff( param )
            case "channel_fader": result = self.setChannelFader( param )
            case "matrix_config_name": result = self.setConfigName( param )
            case "matrix_config_color": result = self.setConfigColor( param )
            case "matrix_config_icon": result = self.setConfigIcon( param )
            case "dca_config_name": result = self.setConfigName( param )
            case "dca_config_color": result = self.setConfigColor( param )
            case "dca_config_icon": result = self.setConfigIcon( param )
            case _: result = "Invalid Parameter [{}]".format( param["param"] )
        return result
    
    def setConfigName( self, param):
        match param["param"]:
            case "channel_config_name": obj_type_str = "ch"
            case "matrix_config_name": obj_type_str = "mtx"
            case "dca_config_name": obj_type_str = "dca"
        obj_addr_str = "/{}/{}/config/name".format(obj_type_str, param["index"])
        print("DEBUG : address = {} | value = {} ".format(obj_addr_str, param["value"]))
        self.OSCclient.send_message(obj_addr_str, param["value"])
        
    def setConfigColor( self, param):
        match param["param"]:
            case "channel_config_color": obj_type_str = "ch"
            case "matrix_config_color": obj_type_str = "mtx"
            case "dca_config_color": obj_type_str = "dca"
        obj_addr_str = "/{}/{}/config/color".format(obj_type_str, param["index"])
        print("DEBUG : address = {} | value = {} ".format(obj_addr_str, param["value"]))
        self.OSCclient.send_message(obj_addr_str, param["value"])
    
    def setConfigIcon( self, param):
        match param["param"]:
            case "channel_config_icon": obj_type_str = "ch"
            case "matrix_config_icon": obj_type_str = "mtx"
            case "dca_config_icon": obj_type_str = "dca"
        obj_addr_str = "/{}/{}/config/icon".format(obj_type_str, param["index"])
        print("DEBUG : address = {} | value = {} ".format(obj_addr_str, param["value"]))
        self.OSCclient.send_message(obj_addr_str, param["value"])

    def setChannelConfigSource( self, param ):
        channel_number = param["index"]
        channel_source = param["value"]
        self.OSCclient.send_message("/ch/{}/config/source".format(channel_number), channel_source)

    def setChannelOnOff( self, param):
        channel = param["index"]
        on_off_state = param["value"]
        #print("setChannelOnOff [{} - {}]".format( channel, on_off_state ))
        self.OSCclient.send_message("/ch/{}/mix/on".format(channel), on_off_state)

    def setChannelFader(self, param):
        channel = param["index"]
        fader_value = param["value"]
        # print("setChannelFader [{} - {}]".format( channel, fader_value ))
        self.OSCclient.send_message("/ch/{}/mix/fader".format(channel), fader_value)

    def setChannelGroupDCA( self, param ):
        # action["index"] is the channel number ["01" through "32"]
        # action["value"] is an integer representing an 8 bit bitmap for assigning the 8 DCA's
        channel = param["index"]
        dca_groups = param["value"]
        # print("setChannelGroupDCA [{} - {}]".format( channel, dca_groups ))
        self.OSCclient.send_message("/ch/{}/grp/dca".format(channel) , dca_groups)
