from Group import Partition
from Viewer import Viewer

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
import tkinter as tk

class ChartWidget( ttk.Frame, Viewer ):
    def __init__( self, parent, group, ledger, setting, *args, **kwargs ):
        Viewer.__init__( self, backer=[ group, ledger, setting ] ) # TODO: fill out
        ttk.Frame.__init__( self, parent, *args, **kwargs )

        self.group = group
        self.ledger = ledger
        self.setting = setting
        
        self.fig = plt.Figure()
        self.chart = None
        
        self.build()
    
    def onUpdate( self ):
        self.draw()
    
    def draw( self ):
        self.fig.clf()

        active = self.group.active
        if not active:
            self.chart.draw()
            return

        df = self.ledger.df
        if self.setting.dateRange[ 0 ]:
            df = df.loc[ df[ 'date' ] >= self.setting.dateRange[ 0 ] ]
        if self.setting.dateRange[ 1 ]:
            df = df.loc[ df[ 'date' ] < self.setting.dateRange[ 1 ] ]
        self.ax = self.fig.add_subplot( 111 )
        if self.setting.exclusive:
            groups = [ self.group.groups[ a ] for a in active ]
            blacklist = sum( ( g.whitelist for k, g in self.group.groups.items() if k not in active ), [] )
            part = Partition( groups=groups, blacklist=blacklist, otherColor=self.group.newColor() )
            getattr( part, self.setting.plotType )( df, self.ax )
        else:
            for a in active:
                getattr( self.group.groups[ a ], self.setting.plotType )( df, self.ax )
        if self.setting.plotType != 'plotPie':
            self.ax.legend( handles=self.ax.lines )
        self.chart.draw()
    
    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        self.chart = FigureCanvasTkAgg( self.fig, self )
        self.chart.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )