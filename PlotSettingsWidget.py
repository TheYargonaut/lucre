from tkinter import ttk

class PlotSettingsWidget( ttk.Frame ):
    def __init__( self, master, settingsContainer, *args, **kwargs ):
        ttk.Frame.__init__( self, master, *args, **kwargs )
        self.settings = settingsContainer
    
    def build( self ):
        pass