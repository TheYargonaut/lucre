import os, yaml
from functools import reduce

# basic event grouping

def matchAny( regexList, df, column='comment' ):
    return reduce( lambda x,y: x | y,
                   ( df[ column ].str.contains( r ) 
                     for r in regexList ) )

class Group( object ):
    def __init__( self, title, whitelist=[], blacklist=[], negate=False ):
        '''blacklist overrides whitelist'''
        self.title = title
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.negate = negate
    
    def applyWhitelist( self, df ):
        return df[ matchAny( self.whitelist, df ) ]
    
    def applyBlacklist( self, df ):
        return df[ ~matchAny( self.blacklist, df ) ]

    def filter( self, df ):
        '''returns filtered pandas dataframe
        first applies whitelist, then blacklist'''
        if self.whitelist:
            df = self.applyWhitelist( df )
        if self.blacklist:
            df = self.applyBlacklist( df )
        return df
    
    def plotDelta( self, df, ax ):
        df = self.filter( df )
        if self.negate:
            df[ self.title ] = -df[ 'delta' ]
        else:
            df[ self.title ] = df[ 'delta' ]
        df.plot( x='date', y=self.title, ax=ax )
    
    def plotCumulative( self, df, ax ):
        df = self.filter( df )
        if self.negate:
            df[ self.title ] = -df[ 'delta' ].cumsum()
        else:
            df[ self.title ] = df[ 'delta' ].cumsum()
        df.plot( x='date', y=self.title, ax=ax, drawstyle="steps-post" )
    def keys( self ):
        return 'title', 'whitelist', 'blacklist', 'negate'
    def __getitem__( self, key ):
        return getattr( self, key )

# TODO: prioritized partition

# file operations

defaultFile = os.path.join( '.', 'userdata', 'groups.yaml' )

def load( filename=defaultFile ):
    with open( filename, 'r' ) as f:
        return [ Group( **g ) for g in yaml.load( f, Loader=yaml.FullLoader ) ]

def save( groups, filename=defaultFile ):
    with open( filename, 'w' ) as f:
        yaml.dump( [ dict( g ) for g in groups ], f )