from EditGroup import editGroupCb
from Format import FormatMan
from Group import Partition, GroupMan
from ImportLedger import importLedgerCb
from Ledger import LedgerMan
from List import ListView
from Scrollable import Scrollable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import matplotlib.pyplot as plt
import os
import pandas as pd
import tkinter as tk

import pdb

pd.plotting.register_matplotlib_converters()

class GroupList( ListView ):
    def __init__( self, parent, back=[], addButton=None, addCb=lambda:None, activeCb=lambda idx, state:None, editCb=lambda idx, activator:None, **kwargs ):
        self.addCb = addCb
        self.activeCb = activeCb
        self.editCb = editCb
        ListView.__init__( self, parent, back, addButton, **kwargs )

    def makeCell( self, label, **kwargs ):
        groupCell = ttk.Frame( self )
        groupCell.grid_columnconfigure( 0, weight=1 )
        var = tk.IntVar()
        var.set( 0 )
        def activate( label=label, var=var ):
            self.activeCb( label, bool( var.get() ) )
        activator = ttk.Checkbutton( groupCell, variable=var, text=self.back[ label ].title, command=activate )
        activator.grid( row=0, column=0, rowspan=2, sticky=tk.NSEW )
        def remove( *args, groupCell=groupCell, label=label ):
            self.activeCb( label, False )
            del self.back[ label ]
            groupCell.destroy()
        remover = ttk.Button( groupCell, text='X', command=remove )
        remover.grid( row=0, column=1, sticky=tk.NSEW )
        def edit( *args, label=label, activator=activator ):
            self.editCb( label, activator )
        editor = ttk.Button( groupCell, text='E', command=edit )
        editor.grid( row=1, column=1, sticky=tk.NSEW )
        return groupCell
    
    def appendCell( self ):
        self.cells.append( self.initCell( self.addCb() ) )

typesInclusive = [ "event", "cumulative" ]
typesExclusive = typesInclusive + [ "stack", "pie" ]
choiceToFunc = dict(
    event="plotAmount",
    cumulative="plotCumulative",
    stack="plotStack",
    pie="plotPie",
)

def setMenuOptions( widget, var, options ):
    if var.get() not in options:
        var.set( next( o for o in options ) )
    widget[ 'menu' ].delete( 0, 'end' )
    for o in options:
        widget[ 'menu' ].add_command( label=o, command=tk._setit( var, o ) )

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )
        self.plotType = "plotAmount"
        self.exclusive = True
        self.makeChart()
        self.format = FormatMan()
        self.group = GroupMan( updateCb=self.redraw )
        self.ledger = LedgerMan( updateCb=self.redraw )
        self.loadData()
        self.build()
    
    def loadData( self ):
        self.format.load()
        self.group.load()
        self.ledger.load()
    
    def redraw( self, *args ):
        df = self.ledger.df
        active = self.group.active
        self.fig.clf()
        if not active:
            self.chartWidget.draw()
            return
        self.ax = self.fig.add_subplot( 111 )
        if self.exclusive:
            groups = [ self.group.groups[ a ] for a in active ]
            blacklist = sum( ( g.whitelist for k, g in self.group.groups.items() if k not in active ), start=[] )
            part = Partition( groups=groups, blacklist=blacklist )
            getattr( part, self.plotType )( df, self.ax )
        else:
            for a in active:
                getattr( self.group.groups[ a ], self.plotType )( df, self.ax )
        self.chartWidget.draw()
    
    def makeChart( self ):
        self.fig = plt.Figure()
        self.chartWidget = FigureCanvasTkAgg( self.fig, self )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )
    
    def editGroup( self, idx, activator ):
        editGroupCb( self, self.group.groups[ idx ], self.ledger, 20, activator )()
        
    def setPlotType( self, *args ):
        self.plotType = choiceToFunc[ self.plotTypeVar.get() ]
        self.redraw()
    
    def activateGroup( self, label, state ):
        self.group.setActive( label, state )
        self.redraw()

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        controlFrame = ttk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        importLedgerButton = ttk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( self, self.ledger, self.format, 20 ) )
        importLedgerButton.pack( side=tk.TOP, fill=tk.X )

        groupScroll = Scrollable( controlFrame, vertical=True )
        groupScroll.pack( side=tk.TOP, fill=tk.BOTH, expand=True )
        groupList = GroupList( groupScroll, self.group.groups, "New Group", self.group.create, self.activateGroup, self.editGroup )
        groupList.pack()
        
        self.plotTypeVar = tk.StringVar()
        self.plotTypeVar.trace( 'w', self.setPlotType )
        self.plotTypeMenu = ttk.OptionMenu( controlFrame, self.plotTypeVar, typesExclusive[ 0 ], *typesExclusive )
        self.plotTypeMenu.pack( side=tk.BOTTOM, fill=tk.X )

        exclusiveVar = tk.IntVar()
        exclusiveVar.set( 1 )
        def exclusiveCb():
            self.exclusive = bool( exclusiveVar.get() )
            setMenuOptions( self.plotTypeMenu, self.plotTypeVar, typesExclusive if self.exclusive else typesInclusive )
            self.redraw()

        exclusiveToggle = ttk.Checkbutton( controlFrame, variable=exclusiveVar, text="Exclusive", command=exclusiveCb )
        exclusiveToggle.pack( side=tk.BOTTOM, fill=tk.X )

# make the window
top = MainWindow()
top.title( "lucre" )
top.mainloop()

# save current settings
if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
top.format.save()
top.ledger.save()
top.group.save()