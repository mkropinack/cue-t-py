class NULL_TARGET():

    def __init__( self, targetInfo ):
        self.data = targetInfo

    def setParam( self, param):
        result = ""
        match param["param"]:
            case _: result = "NULL_TARGET - Invalid Target / Parameter [{}|{}]".format( self.data["type"], param["param"] )
        print(result)
        return result
        
