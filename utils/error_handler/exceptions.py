from nextcord.ext.commands import CommandError

class NotAdmin(CommandError):
    def __init__(self, *args):
        super().__init__(message="You are not an admin!", *args)

class NotOwner(CommandError):
    def __init__(self, *args):
        super().__init__(message="You are not the owner of RelaxCraft!", *args)
    
class NoProfile(CommandError):
    def __init__(self, *args):
        super().__init__(message="You do not yet have a profile!", *args)