from Viewer import Viewer

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk

class ChartWidget( ttk.Frame, Viewer ):
    def __init__( self, parent, groupMan, ledgerMan, dateMan, settingsContainer, *args, **kwargs ):
        Viewer.__init__( self, backer=[ settingsContainer ] ) # TODO: fill out
        ttk.Frame.__init__( self, parent, *args, **kwargs )

        self.group = groupMan
        self.ledger = ledgerMan
        self.setting = settingsContainer
        
        self.fig = plt.Figure()
        self.chart = None
        
        self.build()
    
    def draw( self ):
      if self.chart:
        self.chart.draw()
    
    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        self.chart = FigureCanvasTkAgg( self.fig, self )
        self.chart.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )