
from pythonosc import udp_client

class OSC_M32():

    CH_CONFIG_NAME_MAXLEN = 12
    CH_CONFIG_COLORS = ["OFF", "RD", "GN", "YE", "BL", "MG", "CY", "WH", "OFFi", "RDi", "GNi", "YEi", "BLi", "MGi", "CYi", "WHi"]

    def __init__( self, configVal ):
        self.data = configVal
        self.OSCclient = udp_client.SimpleUDPClient(configVal["ip"], int(configVal["port"]))


    # setParam - setParam issues individual configuration and parameter changes to the Audio console.
    # These commands are not conditional, and are issued regardless of the state of the console.
    # No information is returned from the console, and the previous state of the parameter is not saved.
    # These are intended to be used as building blocks for more complicated cues.

    def setParam( self, param):
        result = ""
        match param["param"]:
            case "channel_config_name": result = self.setChannelConfigName( param )
            case "channel_config_color": result = self.setChannelConfigColor( param )
            case "channel_config_icon": result = self.setChannelConfigIcon( param )
            case "channel_group_dca": result = self.setChannelGroupDCA( param )
            case "channel_on_off": result = self.setChannelOnOff( param )
            case "channel_fader": result = self.setChannelFader( param )
            case _: result = "Invalid Parameter [{}]".format( param["param"] )
        return result
    
    def setChannelConfigName( self, param ):
        channel_number = param["index"]
        channel_name = param["value"]
        self.OSCclient.send_message("/ch/{}/config/name".format(channel_number), channel_name)

    def setChannelConfigColor( self, param ):
        channel_number = param["index"]
        channel_color = param["value"]
        self.OSCclient.send_message("/ch/{}/config/color".format(channel_number), channel_color)
    
    def setChannelConfigColor( self, param ):
        channel_number = param["index"]
        channel_icon = param["value"]
        self.OSCclient.send_message("/ch/{}/config/icon".format(channel_number), channel_icon)

    def setChannelOnOff( self, param):
        channel = param["index"]
        on_off_state = param["value"]
        print("setChannelOnOff [{} - {}]".format( channel, on_off_state ))
        # TODO - set the state of channel mute based on "state" = on|off
        self.OSCclient.send_message("/ch/{}/mix/on".format(channel), on_off_state)

    def setChannelFader(self, param):
        channel = param["index"]
        fader_value = param["value"]
        print("setChannelFader [{} - {}]".format( channel, fader_value ))
        self.OSCclient.send_message("/ch/{}/mix/fader".format(channel), fader_value)

    def setChannelGroupDCA( self, param ):
        # action["index"] is the channel number ["01" through "32"]
        # action["value"] is an integer representing an 8 bit bitmap for assigning the 8 DCA's
        channel = param["index"]
        dca_groups = param["value"]
        print("setChannelGroupDCA [{} - {}]".format( channel, dca_groups ))
        self.OSCclient.send_message("/ch/{}/grp/dca".format(channel) , dca_groups)
