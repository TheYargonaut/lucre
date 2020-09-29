import os, yaml, pdb
import pandas as pd
from functools import reduce
from Format import internalFmt

# basic event grouping

def matchAny( regexList, df, column='memo' ):
    return reduce( lambda x,y: x | y,
                   ( df[ column ].str.contains( r ) 
                     for r in regexList ) )

class Group( object ):
    def __init__( self, title="", whitelist=[], blacklist=[], negate=False ):
        '''blacklist overrides whitelist'''
        self.title = title
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.negate = negate
    
    def applyWhitelist( self, df ):
        return matchAny( self.whitelist, df )
    
    def applyBlacklist( self, df ):
        return ~matchAny( self.blacklist, df )

    def filter( self, df ):
        '''returns filtered pandas dataframe
        first applies whitelist, then blacklist'''
        f = df[ 'memo' ].str.contains( '.*' )
        if self.whitelist:
            f &= self.applyWhitelist( df )
        if self.blacklist:
            f &= self.applyBlacklist( df )
        return f
    
    def plotDelta( self, df, ax ):
        df = df[ self.filter( df ) ]
        if self.negate:
            df[ self.title ] = -df[ 'delta' ]
        else:
            df[ self.title ] = df[ 'delta' ]
        df.plot( x='date', y=self.title, ax=ax )
    
    def plotCumulative( self, df, ax ):
        df = df[ self.filter( df ) ]
        if self.negate:
            df[ self.title ] = -df[ 'delta' ].cumsum()
        else:
            df[ self.title ] = df[ 'delta' ].cumsum()
        df.plot( x='date', y=self.title, ax=ax, drawstyle="steps-post" )

    def keys( self ):
        return 'title', 'whitelist', 'blacklist', 'negate'
    def __getitem__( self, key ):
        return getattr( self, key )

class Partition( object ):
    def __init__( self, groups=[], blacklist=[], negate=False ):
        'negate applies to the other group'
        self.groups = groups
        self.blacklist = blacklist
        self.negate = negate
    
    def filter( self, df, edges=True ):
        'split into g+1 groups and return as dictionary'
        df = df.copy()
        if self.blacklist:
            df = df[ ~matchAny( self.blacklist, df ) ]
        early = pd.DataFrame( dict( date=df[ 'date' ].min(),
                                    delta=0,
                                    memo='' ), index=[ 0 ] )
        late = pd.DataFrame( dict( date=df[ 'date' ].max(),
                                   delta=0,
                                   memo='' ), index=[ 0 ] )
        r = {}
        for g in self.groups:
            f = g.filter( df )
            if edges:
                r[ g.title ] = pd.concat( [ early, df[ f ], late ] ).reset_index( drop=True )
            else:
                r[ g.title ] = df[ f ]
            if g.negate:
                r[ g.title ][ 'delta' ] = -r[ g.title ][ 'delta' ]
            df = df[ ~f ]
        if edges:
            r[ 'other' ] = pd.concat( [ early, df, late ] ).reset_index( drop=True )
        else:
            r[ 'other' ] = df
        if self.negate:
            r[ 'other' ][ 'delta' ] = -r[ 'other' ][ 'delta' ]
        return r
    
    def plotDelta( self, df, ax ):
        for title, data in self.filter( df, False ).items():
            data[ title ] = data[ 'delta' ]
            if not data.empty:
                data.plot( x='date', y=title, ax=ax )

    def plotCumulative( self, df, ax ):
        for title, data in self.filter( df ).items():
            data[ title ] = data[ 'delta' ].cumsum()
            if not data.empty:
                data.plot( x='date', y=title, ax=ax, drawstyle='steps-post' )

    def plotLayer( self, stack, layer, title, ax ):
        if stack is None:
            stack = layer
        else:
            stack = pd.concat( [ stack, layer ] ).sort_values( 'date' ).reset_index( drop=True )
        stack[ title ] = stack[ 'delta' ].cumsum()
        stack.plot( x='date', y=title, ax=ax, drawstyle='steps-post' )
        return stack[ internalFmt ]

    def plotStack( self, df, ax ):
        data = self.filter( df )
        stack = None
        for g in self.groups:
            stack = self.plotLayer( stack, data[ g.title ], g.title, ax )
        self.plotLayer( stack, data[ 'other' ], 'other', ax )
    
    def plotPie( self, df, ax ):
        total = { title: data[ 'delta' ].sum() for title, data in self.filter( df ).items() }
        pd.Series( total ).sort_values().plot.pie( ax=ax )        

defaultFile = os.path.join( '.', 'userdata', 'groups.yaml' )
class GroupMan( object ):
    def __init__( self, groups=[], parts=[] ):
        self.groups = groups
        self.parts = parts
    
    def load( self, filename=defaultFile ):
        'load groups from file, add to existing groups. returns successful'
        try:
            with open( filename, 'r' ) as f:
                self.groups += [ Group( **g ) for g in yaml.load( f, Loader=yaml.FullLoader ) ]
            return True
        except FileNotFoundError:
            return False

    def save( self, filename=defaultFile ):
        'save groups to file'
        with open( filename, 'w' ) as f:
            yaml.dump( [ dict( g ) for g in self.groups ], f )