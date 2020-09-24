from Group import load as loadGroups, save as saveGroups, Partition, Group
from Ledger import loadLedger, loadFormats, saveFormats, saveLedger, importLedger, Ledger
from Table import tableFromDf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from Scrollable import Scrollable
from ImportLedger import importLedgerCb
from EditGroup import editGroupCb

import pdb

pd.plotting.register_matplotlib_converters()

# import all the data
formats = loadFormats()
ledger = loadLedger()
groups = loadGroups()

# set up managers
expensePart = Partition( [ g for g in groups if g.negate ], sum( [
   g.whitelist + g.blacklist for g in groups if not g.negate
], [] ), negate=True )
generalPart = Partition()

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot( 111 )
        self.build()
    
    def redraw( self, df, part=generalPart ):
        self.ax.cla()
        part.plotDelta( df, self.ax )
        self.chartWidget.draw()

    def build( self ):
        self.chartWidget = FigureCanvasTkAgg( self.fig, self )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )

        self.ledgerManager = Ledger( ledger, updateCb=self.redraw )
        self.ledgerManager.updateCb( self.ledgerManager.df )

        controlFrame = tk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        importLedgerButton = tk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( self, self.ledgerManager ) )
        importLedgerButton.pack( side=tk.TOP, fill=tk.X )

        addGroupButton = tk.Button( controlFrame, text="New Group", command=editGroupCb( self, Group(), self.ledgerManager, 20 ) )
        addGroupButton.pack( side=tk.BOTTOM, fill=tk.X )

# make the window
top = MainWindow()
top.mainloop()

# save current settings
if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
saveFormats( formats )
saveLedger( top.ledgerManager.df )
saveGroups( groups )