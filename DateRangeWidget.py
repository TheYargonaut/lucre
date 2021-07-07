import pandas as pd
from tkinter import ttk
import tkinter as tk

from pandas._libs.tslibs import NaTType

# with of full date + boundaries
dateWidth = 10 + 2

class DateRangeWidget( ttk.Frame ):
    def __init__( self, parent, rangeCb=lambda *_:None, **kwargs ):
        '''call rangeCb with new range (low,high) after each succesful set'''
        ttk.Frame.__init__( self, parent, **kwargs )
        self.rangeCb = rangeCb

        self.lowEntry = None
        self.highEntry = None

        # string literal input, datetime object
        self.prevLow = ( "", None )
        self.prevHigh = ( "", None )

        self.validCmd = self.register( self.validDate )
        self.invLow = self.register( self.invalidLow )
        self.invHigh = self.register( self.invalidHigh )

        self.entryStyle = dict(
            width=dateWidth,
            validate='focusout',
            justify='center',
        )

        self.build()
    
    def build( self ):
        tk.Label( self, text="Date Range:" ).pack( side=tk.LEFT )

        self.lowTxt = tk.StringVar( self )
        self.lowEntry = ttk.Entry(
            self, textvariable=self.lowTxt, validatecommand=( self.validCmd, '%P' ),
            invalidcommand=self.invLow, **self.entryStyle )
        self.lowEntry.bind( '<FocusOut>', self.lowCb )
        self.lowEntry.pack( side=tk.LEFT )
        
        ttk.Label( self, text="-" ).pack( side=tk.LEFT )

        self.highTxt = tk.StringVar( self )
        self.highEntry = ttk.Entry(
            self, textvariable=self.highTxt, validatecommand=( self.validCmd, '%P' ),
            invalidcommand=self.invHigh, **self.entryStyle )
        self.highEntry.bind( '<FocusOut>', self.highCb )
        self.highEntry.pack( side=tk.LEFT )
    
    def validDate( self, new ):
        if not new:
            return True # allow a cleared one to mean no bound
        return not isinstance( pd.to_datetime( new, errors='coerce' ), NaTType )

    def invalidLow( self ):
        self.lowTxt.set( self.prevLow[ 0 ] )
    
    def invalidHigh( self ):
        self.highTxt.set( self.prevHigh[ 0 ] )

    def lowCb( self, *_ ):
        s = self.lowTxt.get()
        if not self.validDate( s ):
            return
        d = None if not s else pd.to_datetime( s ).date()
        repeat = d == self.prevLow[ 1 ]
        self.prevLow = s, d
        if repeat:
            return
        self.rangeCb( self.prevLow[ 1 ], self.prevHigh[ 1 ] )
        

    def highCb( self, *_ ):
        s = self.highTxt.get()
        if not self.validDate( s ):
            return
        d = None if not s else pd.to_datetime( s ).date()
        repeat = d == self.prevHigh[ 1 ]
        self.prevHigh = s, d
        if repeat:
            return
        self.rangeCb( self.prevLow[ 1 ], self.prevHigh[ 1 ] )