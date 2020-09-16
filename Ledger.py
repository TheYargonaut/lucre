import os, yaml
import pandas as pd
import tkinter as tk

knownFmt = { 'internal' : [ 'date', 'delta', 'memo' ] }
defaultFmtFn = os.path.join( '.', 'userdata', 'formats.yaml' )
def loadFormats( filename=defaultFmtFn ):
    try:
        with open( filename, 'r' ) as f:
            return yaml.load( f, Loader=yaml.FullLoader )
    except FileNotFoundError:
        return knownFmt
def saveFormats( formats, filename=defaultFmtFn ):
    with open( filename, 'w' ) as f:
        yaml.dump( formats, f )

def preprocess( df ):
    ledger = df[ knownFmt[ 'internal' ] ]
    ledger[ 'date' ] = pd.to_datetime( ledger[ 'date' ] )
    ledger.sort_values( 'date', inplace=True )
    ledger.reset_index( drop=True, inplace=True )
    pd.DataFrame.drop_duplicates( ledger )
    return ledger

defaultLedgerFn = os.path.join( '.', 'userdata', 'ledger.csv' )
def loadLedger( filename=defaultLedgerFn, fmt=knownFmt[ 'internal' ] ):
    try:
        df = pd.read_csv( filename, index_col=None, header=None, names=fmt )
        return preprocess( df )
    except FileNotFoundError:
        return pd.DataFrame( columns=knownFmt[ 'internal' ] )
def importLedger( existingLedger, filename=defaultLedgerFn, fmt=knownFmt[ 'internal' ] ):
    return preprocess( existingLedger.append( loadLedger( filename, fmt ) ) )
def saveLedger( dataFrame, filename=defaultLedgerFn ):
    dataFrame.to_csv( filename, header=False, index=False )

# mass import tool
def fileGen( startDir, recurse=False, ext=None ):
    for root, _, files in os.walk( startDir ):
        for f in files:
            if ext is None or f[ -len(ext): ] == ext:
                yield( os.path.join( root, f ) )
        if not recurse:
            break
def ledgerGen( fileGen, fmt=knownFmt[ 'internal' ] ):
    for f in fileGen:
        df = pd.read_csv( f, index_col=None, header=None, names=fmt )
        yield df[ knownFmt[ 'internal' ] ]
def massLoadLedger( startDir, fmt=knownFmt[ 'internal' ], recurse=False, ext=None ):
    'grabs all ledgers in a directory and preprocesses to internal format'
    fg = fileGen( startDir, recurse, ext )
    lg = ledgerGen( fg, fmt )
    return preprocess( pd.concat( lg, ignore_index=True ) )

class Ledger( object ):
    def __init__( self, df=None, updateCb=lambda:None ):
        self.df = df
        self.updateCb = updateCb
    
    def add( self, df ):
        self.df = preprocess( self.df.append( preprocess( df ) ) )