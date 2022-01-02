from DateRangeWidget import DateRangeWidget
from PlotSettings import PlotSettings

from tkinter import ttk
import tkinter as tk

class PlotSettingsWidget( ttk.Frame ):
    typesInclusive = [ "event", "cumulative" ]
    typesExclusive = typesInclusive + [ "stack", "bar", "pie" ]

    def __init__( self, master, settingsContainer, *args, **kwargs ):
        ttk.Frame.__init__( self, master, *args, **kwargs )
        self.settings = settingsContainer

        self.exclusiveVar = tk.IntVar()
        self.exclusiveVar.set( 1 )
        self.plotTypeVar = tk.StringVar()
        self.plotTypeVar.set( PlotSettingsWidget.typesExclusive[ 0 ] )

        self.build()

    def setMenuOptions( self, widget, var, options ):
        if var.get() not in options:
            var.set( next( o for o in options ) )
        widget[ 'menu' ].delete( 0, 'end' )
        for o in options:
            widget[ 'menu' ].add_command( label=o, command=tk._setit( var, o ) )
    
    def exclusiveCb( self ):
        e = bool( self.exclusiveVar.get() )
        if e:
          options = PlotSettingsWidget.typesExclusive
        else:
          options = PlotSettingsWidget.typesInclusive
        self.setMenuOptions( self.plotTypeMenu, self.plotTypeVar, options )
        self.settings.setExclusive( e )

    def plotTypeCb( self, *args ):
        self.settings.setPlotType( self.plotTypeVar.get() )
    
    def dateRangeCb( self, low, high ):
        self.settings.setDateRange( low, high )

    def build( self ):
        self.grid_columnconfigure( 0, weight=1 )
        self.grid_rowconfigure( 0, weight=1 )

        exclusiveToggle = ttk.Checkbutton(
          self,
          variable=self.exclusiveVar,
          text="Exclusive",
          command=self.exclusiveCb
        )
        exclusiveToggle.grid( row=0, column=0, sticky=tk.NSEW )

        self.plotTypeMenu = ttk.OptionMenu(
            self,
            self.plotTypeVar,
            None,
            *self.typesExclusive
        )
        self.plotTypeMenu.grid( row=1, column=0, sticky=tk.NSEW )
        self.plotTypeVar.trace( 'w', self.plotTypeCb )

        self.dateRangeW = DateRangeWidget( self, self.dateRangeCb )
        self.dateRangeW.grid( row=2, column=0, sticky=tk.NSEW )