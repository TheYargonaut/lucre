from Format import internalFmt

import os
import pandas as pd

# mass import tool
# def fileGen( startDir, recurse=False, ext=None ):
#     for root, _, files in os.walk( startDir ):
#         for f in files:
#             if ext is None or f[ -len(ext): ] == ext:
#                 yield( os.path.join( root, f ) )
#         if not recurse:
#             break
# def ledgerGen( fileGen, fmt=internalFmt ):
#     for f in fileGen:
#         df = pd.read_csv( f, index_col=None, header=None, names=fmt )
#         yield df[ internalFmt ]
# def massLoadLedger( startDir, fmt=internalFmt, recurse=False, ext=None ):
#     'grabs all ledgers in a directory and preprocesses to internal format'
#     fg = fileGen( startDir, recurse, ext )
#     lg = ledgerGen( fg, fmt )
#     return preprocess( pd.concat( lg, ignore_index=True ) )

def preprocess( df ):
    ledger = df[ internalFmt ].copy()
    ledger[ 'date' ] = pd.to_datetime( ledger[ 'date' ] ).dt.date
    pd.DataFrame.drop_duplicates( ledger, inplace=True )
    ledger.sort_values( 'date', inplace=True )
    ledger.reset_index( drop=True, inplace=True )
    return ledger

defaultFile = os.path.join( '.', 'userdata', 'ledger.csv' )

class LedgerMan( object ):
    def __init__( self, df=pd.DataFrame( columns=internalFmt ), updateCb=lambda:None ):
        self.df = df
        self.updateCb = updateCb
    
    def add( self, df ):
        self.df = preprocess( self.df.append( preprocess( df ) ) )
        self.updateCb( self.df )
    
    def load( self, filename=defaultFile, fmt=internalFmt ):
        'load groups from file, add to existing groups. returns successful'
        try:
            df = pd.read_csv( filename, index_col=None, header=None, names=fmt )
            df = preprocess( df )
            self.df = preprocess( self.df.append( df ) )
            self.updateCb( self.df )
            return True
        except FileNotFoundError:
            return False

    def save( self, filename=defaultFile ):
        self.df.to_csv( filename, header=False, index=False )