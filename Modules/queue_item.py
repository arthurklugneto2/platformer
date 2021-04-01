class QueueItem:

    def __init__(self,command,parameters,message = None, isDialog = False):
        self.command = command
        self.parameters = parameters
        self.message = message
        self.isDialog = isDialog