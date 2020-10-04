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

class ToggleButton( tk.Button ):
    def __init__( self, *args, command=lambda state:None, **kwargs):
        def cb( *args ):
            if self.config( 'relief' )[ -1 ] == 'sunken':
                self.config( relief="raised" )
                command( False )
            else:
                self.config( relief="sunken" )
                command( True )
        tk.Button.__init__( self, *args, command=cb, **kwargs )

class GroupList( ListView ):
    def __init__( self, parent, back=[], addButton=None, addCb=lambda:None, activeCb=lambda idx:None, editCb=lambda idx, activator:None, **kwargs ):
        self.addCb = addCb
        self.activeCb = activeCb
        self.editCb = editCb
        ListView.__init__( self, parent, back, addButton, **kwargs )

    def makeCell( self, label, **kwargs ):
        groupCell = tk.Frame( self )
        groupCell.grid_columnconfigure( 0, weight=1 )
        def activate( state, label=label ):
            self.activeCb( label, state )
        activator = ToggleButton( groupCell, text=self.back[ label ].title, command=activate )
        activator.grid( row=0, column=0, rowspan=2, sticky=tk.NSEW )
        def remove( *args, groupCell=groupCell, label=label ):
            self.activeCb( label, False )
            del self.back[ label ]
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
        self.group = GroupMan( updateCb=self.setPart )
        self.ledger = LedgerMan( updateCb=self.setDf )
        self.loadData()
        self.build()
    
    def loadData( self ):
        self.format.load()
        self.group.load()
        self.ledger.load()
    
    def redraw( self, df, active ):
        self.ax.cla()
        for a in active:
            self.group.groups[ a ].plotDelta( df, self.ax )
        self.chartWidget.draw()
    
    def makeChart( self ):
        fig = plt.Figure()
        self.ax = fig.add_subplot( 111 )
        self.chartWidget = FigureCanvasTkAgg( fig, self )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )
    
    def editGroupCb( self, idx, activator ):
        editGroupCb( self, self.group.groups[ idx ], self.ledger, 20, activator )()
    
    def setDf( self, df ):
        self.redraw( df=df, active=self.group.active )

    def setPart( self, active ):
        # set group/partition to be drawn
        self.redraw( df=self.ledger.df, active=active )

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        controlFrame = tk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        importLedgerButton = tk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( self, self.ledger, self.format ) )
        importLedgerButton.pack( side=tk.TOP, fill=tk.X )

        groupScroll = Scrollable( controlFrame, vertical=True )
        groupScroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        groupList = GroupList( groupScroll, self.group.groups, "New Group", self.group.create, self.group.setActive, self.editGroupCb )
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