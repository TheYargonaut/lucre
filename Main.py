from Group import Group, Partition, GroupMan
from Ledger import loadFormats, saveFormats, LedgerMan
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import tkinter as tk
from ImportLedger import importLedgerCb
from EditGroup import editGroupCb

import pdb

pd.plotting.register_matplotlib_converters()

# set up managers
# expensePart = Partition( [ g for g in groups if g.negate ], sum( [
#    g.whitelist + g.blacklist for g in groups if not g.negate
# ], [] ), negate=True )
generalPart = Partition()

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )
        self.group = GroupMan()
        self.ledger = LedgerMan( updateCb=self.redraw )
        self.build()
        self.loadData()
    
    def loadData( self ):
        self.formats = loadFormats()
        self.ledger.load()
        self.group.load()
    
    def redraw( self, df, part=generalPart ):
        self.ax.cla()
        part.plotDelta( df, self.ax )
        self.chartWidget.draw()
    
    def makeChart( self ):
        fig = plt.Figure()
        self.ax = fig.add_subplot( 111 )
        self.chartWidget = FigureCanvasTkAgg( fig, self )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )

    def build( self ):
        self.makeChart()

        controlFrame = tk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        importLedgerButton = tk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( self, self.ledger ) )
        importLedgerButton.pack( side=tk.TOP, fill=tk.X )

        addGroupButton = tk.Button( controlFrame, text="New Group", command=editGroupCb( self, Group(), self.ledger, 20 ) )
        addGroupButton.pack( side=tk.BOTTOM, fill=tk.X )

# make the window
top = MainWindow()
top.mainloop()

# save current settings
if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
saveFormats( top.formats )
top.ledger.save()
top.group.save()