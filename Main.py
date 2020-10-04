from Group import Group, Partition, GroupMan
from Ledger import LedgerMan
from Format import FormatMan
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import tkinter as tk
from ImportLedger import importLedgerCb
from EditGroup import editGroupCb
from List import ListView
from Scrollable import Scrollable

import pdb

pd.plotting.register_matplotlib_converters()

# set up managers
# expensePart = Partition( [ g for g in groups if g.negate ], sum( [
#    g.whitelist + g.blacklist for g in groups if not g.negate
# ], [] ), negate=True )
generalPart = Partition()

class GroupList( ListView ):
    def __init__( self, parent, back=[], addButton=None, addCb=lambda:None, activeCb=lambda idx:None, editCb=lambda idx, activator:None, **kwargs ):
        self.addCb = addCb
        self.activeCb = activeCb
        self.editCb = editCb
        ListView.__init__( self, parent, back, addButton, **kwargs )

    def makeCell( self, label, **kwargs ):
        groupCell = tk.Frame( self )
        def activate( *args, label=label ):
            self.activeCb( label )
        activator = tk.Button( groupCell, text=self.back[ label ].title, command=activate )
        activator.grid( row=0, column=0, rowspan=2, sticky=tk.NSEW )
        def remove( *args, groupCell=groupCell, label=label ):
            del self.back[ label ] # needs to actually link back to the "back" in the manager
            if self.back:
                self.activeCb( next( k for k in self.back.keys() ) )
            groupCell.destroy()
        remover = tk.Button( groupCell, text='X', command=remove )
        remover.grid( row=0, column=1, sticky=tk.NSEW )
        def edit( *args, label=label, activator=activator ):
            self.editCb( label, activator )
        editor = tk.Button( groupCell, text='E', command=edit )
        editor.grid( row=1, column=1, sticky=tk.NSEW )
        return groupCell
    
    def appendCell( self ):
        self.cells.append( self.initCell( self.addCb() ) )

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )
        self.makeChart()
        self.format = FormatMan()
        self.group = GroupMan()
        self.ledger = LedgerMan( updateCb=self.redraw )
        self.loadData()
        self.build()
    
    def loadData( self ):
        self.format.load()
        self.group.load()
        self.ledger.load()
    
    def redraw( self, df, part=generalPart ):
        self.ax.cla()
        part.plotDelta( df, self.ax )
        self.chartWidget.draw()
    
    def makeChart( self ):
        fig = plt.Figure()
        self.ax = fig.add_subplot( 111 )
        self.chartWidget = FigureCanvasTkAgg( fig, self )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )
    
    def editGroupCb( self, idx, activator ):
        editGroupCb( self, self.group.groups[ idx ], self.ledger, 20, activator )()

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        controlFrame = tk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        importLedgerButton = tk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( self, self.ledger, self.format ) )
        importLedgerButton.pack( side=tk.TOP, fill=tk.X )

        groupScroll = Scrollable( controlFrame, vertical=True )
        groupScroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        groupList = GroupList( groupScroll, self.group.groups, "New Group", self.group.create, lambda idx:None, self.editGroupCb )
        groupList.pack()

# make the window
top = MainWindow()
top.mainloop()

# save current settings
if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
top.format.save()
top.ledger.save()
top.group.save()