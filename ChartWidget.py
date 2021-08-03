from tkinter import ttk
import tkinter as tk

class ChartWidget( ttk.Frame ):
    def __init__( self, parent, *args, **kwargs ):
        ttk.Frame.__init__( self, parent, *args, **kwargs )
        self.build()
    
    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )