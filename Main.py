from ChartWidget import ChartWidget
from DateRangeWidget import DateRangeWidget
from EditGroupWindow import editGroupCb
from Format import FormatMan
from Group import Partition, GroupMan
from GroupControlWidget import GroupList
from ImportLedgerWindow import importLedgerCb
from Ledger import Ledger
from PlotSettings import PlotSettings
from Scrollable import Scrollable
from ViewLedgerWindow import viewLedgerCb

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import matplotlib.pyplot as plt
import os
import pandas as pd
import tkinter as tk

pd.plotting.register_matplotlib_converters()

def setMenuOptions( widget, var, options ):
    if var.get() not in options:
        var.set( next( o for o in options ) )
    widget[ 'menu' ].delete( 0, 'end' )
    for o in options:
        widget[ 'menu' ].add_command( label=o, command=tk._setit( var, o ) )

class MainWindow( tk.Tk ):
    def __init__( self ):
        tk.Tk.__init__( self )

        self.plotSettings = PlotSettings()
        
        self.format = FormatMan()
        self.group = GroupMan( updateCb=self.redraw )
        self.ledger = Ledger( updateCb=self.redraw )
        self.makeChart()
        self.loadData()

        self.exclusiveVar = tk.IntVar()
        self.exclusiveVar.set( 1 )
        self.plotTypeVar = tk.StringVar()
        self.plotTypeVar.set( PlotSettings.typesExclusive[ 0 ] )
        self.plotTypeVar.trace( 'w', self.setPlotType )
        self.build()
    
    def loadData( self ):
        self.format.load()
        self.group.load()
        self.ledger.load()
    
    def redraw( self, *args ):
        df = self.ledger.df
        if self.plotSettings.dateRange[ 0 ]:
            df = df.loc[ df[ 'date' ] >= self.plotSettings.dateRange[ 0 ] ]
        if self.plotSettings.dateRange[ 1 ]:
            df = df.loc[ df[ 'date' ] <= self.plotSettings.dateRange[ 1 ] ]
        active = self.group.active
        self.chartWidget.fig.clf()
        if not active:
            self.chartWidget.draw()
            return
        self.ax = self.chartWidget.fig.add_subplot( 111 )
        if self.plotSettings.exclusive:
            groups = [ self.group.groups[ a ] for a in active ]
            blacklist = sum( ( g.whitelist for k, g in self.group.groups.items() if k not in active ), [] )
            part = Partition( groups=groups, blacklist=blacklist, otherColor=self.group.newColor() )
            getattr( part, self.plotSettings.plotType )( df, self.ax )
        else:
            for a in active:
                getattr( self.group.groups[ a ], self.plotSettings.plotType )( df, self.ax )
        if self.plotSettings.plotType != 'plotPie':
            self.ax.legend( handles=self.ax.lines )
        self.chartWidget.draw()
    
    def makeChart( self ):
        chartFrame = ttk.Frame( self )
        chartFrame.grid( row=0, column=0, sticky=tk.NSEW )
        chartFrame.grid_rowconfigure( 0, weight=1 )
        chartFrame.grid_columnconfigure( 0, weight=1 )

        self.chartWidget = ChartWidget( chartFrame, None, None, None, self.plotSettings ) #Todo: pass appropriate for working
        self.chartWidget.grid( row=0, column=0, sticky=tk.NSEW )

        self.dateRangeW = DateRangeWidget( chartFrame, self.setDateRange )
        self.dateRangeW.grid( row=1, column=0, sticky=tk.W )
    
    def editGroup( self, idx ):
        editGroupCb( self, self.group.groups[ idx ], self.ledger, 25 )()
        
    def viewLedger( self ):
        viewLedgerCb( self, self.group.groups, self.ledger.df )()

    def setPlotType( self, *args ):
        self.plotSettings.setPlotType(self.plotTypeVar.get())
        self.redraw()
    
    def setDateRange( self, l, h ):
        self.plotSettings.dateRange = l, h
        self.redraw()
    
    def activateGroup( self, label, state ):
        self.group.setActive( label, state )
    
    def exclusiveCb( self ):
        self.plotSettings.exclusive = bool( self.exclusiveVar.get() )
        setMenuOptions(
            self.plotTypeMenu,
            self.plotTypeVar,
            PlotSettings.typesExclusive if self.plotSettings.exclusive else PlotSettings.typesInclusive
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
            *PlotSettings.typesExclusive
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