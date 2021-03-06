from DateRangeWidget import DateRangeWidget
from GroupControlWidget import GroupList
from EditGroupWindow import editGroupCb
from ViewLedgerWindow import viewLedgerCb
from ImportLedgerWindow import importLedgerCb
from Format import FormatMan
from Group import Partition, GroupMan
from Ledger import LedgerMan
from Scrollable import Scrollable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import matplotlib.pyplot as plt
import os
import pandas as pd
import tkinter as tk

pd.plotting.register_matplotlib_converters()

typesInclusive = [ "event", "cumulative" ]
typesExclusive = typesInclusive + [ "stack", "bar", "pie" ]
choiceToFunc = dict(
    event="plotAmount",
    cumulative="plotCumulative",
    stack="plotStack",
    pie="plotPie",
    bar="plotBar"
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
        self.dateRange = None, None
        self.makeChart()
        
        self.format = FormatMan()
        self.group = GroupMan( updateCb=self.redraw )
        self.ledger = LedgerMan( updateCb=self.redraw )
        self.loadData()

        self.exclusiveVar = tk.IntVar()
        self.exclusiveVar.set( 1 )
        self.plotTypeVar = tk.StringVar()
        self.plotTypeVar.set( typesExclusive[ 0 ] )
        self.plotTypeVar.trace( 'w', self.setPlotType )
        self.build()
    
    def loadData( self ):
        self.format.load()
        self.group.load()
        self.ledger.load()
    
    def redraw( self, *args ):
        df = self.ledger.df
        if self.dateRange[ 0 ]:
            df = df.loc[ df[ 'date' ] >= self.dateRange[ 0 ] ]
        if self.dateRange[ 1 ]:
            df = df.loc[ df[ 'date' ] <= self.dateRange[ 1 ] ]
        active = self.group.active
        self.fig.clf()
        if not active:
            self.chartWidget.draw()
            return
        self.ax = self.fig.add_subplot( 111 )
        if self.exclusive:
            groups = [ self.group.groups[ a ] for a in active ]
            blacklist = sum( ( g.whitelist for k, g in self.group.groups.items() if k not in active ), [] )
            part = Partition( groups=groups, blacklist=blacklist, otherColor=self.group.newColor() )
            getattr( part, self.plotType )( df, self.ax )
        else:
            for a in active:
                getattr( self.group.groups[ a ], self.plotType )( df, self.ax )
        if self.plotType != 'plotPie':
            self.ax.legend( handles=self.ax.lines )
        self.chartWidget.draw()
    
    def makeChart( self ):
        chartFrame = ttk.Frame( self )
        chartFrame.grid( row=0, column=0, sticky=tk.NSEW )
        chartFrame.grid_rowconfigure( 0, weight=1 )
        chartFrame.grid_columnconfigure( 0, weight=1 )
        self.fig = plt.Figure()
        self.chartWidget = FigureCanvasTkAgg( self.fig, chartFrame )
        self.chartWidget.get_tk_widget().grid( row=0, column=0, sticky=tk.NSEW )
        self.dateRangeW = DateRangeWidget( chartFrame, self.setDateRange )
        self.dateRangeW.grid( row=1, column=0, sticky=tk.W )
    
    def editGroup( self, idx ):
        editGroupCb( self, self.group.groups[ idx ], self.ledger, 25 )()
        
    def viewLedger( self ):
        viewLedgerCb( self, self.group.groups, self.ledger.df )()

    def setPlotType( self, *args ):
        self.plotType = choiceToFunc[ self.plotTypeVar.get() ]
        self.redraw()
    
    def setDateRange( self, l, h ):
        self.dateRange = l, h
        self.redraw()
    
    def activateGroup( self, label, state ):
        self.group.setActive( label, state )
    
    def exclusiveCb( self ):
        self.exclusive = bool( self.exclusiveVar.get() )
        setMenuOptions(
            self.plotTypeMenu,
            self.plotTypeVar,
            typesExclusive if self.exclusive else typesInclusive
        )
        self.redraw()

    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )

        controlFrame = ttk.Frame( self )
        controlFrame.grid( row=0, column=1, sticky=tk.NSEW )

        controlFrame.grid_columnconfigure( 0, weight=1 )
        controlFrame.grid_rowconfigure( 2, weight=1 )

        importLedgerButton = ttk.Button(
            controlFrame, text="Import Ledger",
            command=importLedgerCb( self, self.ledger, self.format, 25 )
        )
        importLedgerButton.grid( row=0, column=0, sticky=tk.NSEW )
        viewLedgerButton = ttk.Button( controlFrame, text="Browse Ledger", command=self.viewLedger )
        viewLedgerButton.grid( row=1, column=0, sticky=tk.NSEW )

        groupScroll = Scrollable( controlFrame, vertical=True )
        groupScroll.grid( row=2, column=0, sticky=tk.NSEW )
        groupList = GroupList(
            groupScroll,
            self.group.groups,
            "New Group",
            self.group.create,
            self.activateGroup,
            self.editGroup
        )
        groupList.pack()

        self.plotTypeMenu = ttk.OptionMenu(
            controlFrame,
            self.plotTypeVar,
            None,
            *typesExclusive
        )
        self.plotTypeMenu.grid( row=4, column=0, sticky=tk.NSEW )

        exclusiveToggle = ttk.Checkbutton( controlFrame, variable=self.exclusiveVar, text="Exclusive", command=self.exclusiveCb )
        exclusiveToggle.grid( row=3, column=0, sticky=tk.NSEW )

# make the window
top = MainWindow()
top.title( "lucre" )
top.tk.call( 'wm', 'iconphoto', top._w, tk.PhotoImage( file='logo.png' ) )
top.mainloop()

# save current settings
userDataPath = os.path.join( '.', 'userdata' )
if not os.path.exists( userDataPath ):
    os.mkdir( userDataPath )
top.format.save()
top.ledger.save()
top.group.save()