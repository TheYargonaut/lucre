import os, yaml, pdb
import pandas as pd
from functools import reduce
from Format import internalFmt

# basic event grouping

def matchAny( regexList, df, column='memo' ):
    return reduce( lambda x,y: x | y,
                   ( df[ column ].str.contains( r ) 
                     for r in regexList if r ),
                   False )

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
    
    def plotAmount( self, df, ax ):
        df = df[ self.filter( df ) ].copy()
        if self.negate:
            df[ self.title ] = -df[ 'amount' ]
        else:
            df[ self.title ] = df[ 'amount' ]
        df.plot( x='date', y=self.title, ax=ax, style='o' )
    
    def plotCumulative( self, df, ax ):
        early = pd.DataFrame( dict( date=df[ 'date' ].min(),
                                    amount=0,
                                    memo='' ), index=[ 0 ] )
        late = pd.DataFrame( dict( date=df[ 'date' ].max(),
                                   amount=0,
                                   memo='' ), index=[ 0 ] )
        df = df[ self.filter( df ) ].copy()
        df = pd.concat( [ early, df, late ] ).reset_index( drop=True )
        if self.negate:
            df[ self.title ] = -df[ 'amount' ].cumsum()
        else:
            df[ self.title ] = df[ 'amount' ].cumsum()
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
                                    amount=0,
                                    memo='' ), index=[ 0 ] )
        late = pd.DataFrame( dict( date=df[ 'date' ].max(),
                                   amount=0,
                                   memo='' ), index=[ 0 ] )
        r = {}
        for g in self.groups:
            f = g.filter( df )
            if edges:
                r[ g.title ] = pd.concat( [ early, df[ f ], late ] ).reset_index( drop=True )
            else:
                r[ g.title ] = df[ f ].copy()
            if g.negate:
                r[ g.title ].loc[ :, 'amount' ] = -r[ g.title ][ 'amount' ]
            df = df[ ~f ]
        if edges:
            r[ 'Other' ] = pd.concat( [ early, df, late ] ).reset_index( drop=True )
        else:
            r[ 'Other' ] = df
        if self.negate:
            r[ 'Other' ].loc[ :, 'amount' ] = -r[ 'Other' ][ 'amount' ]
        return r
    
    def plotAmount( self, df, ax ):
        for title, data in self.filter( df, False ).items():
            data.loc[ :, title ] = data[ 'amount' ]
            if not data.empty:
                data.plot( x='date', y=title, ax=ax, style='o' )

    def plotCumulative( self, df, ax ):
        for title, data in self.filter( df ).items():
            data[ title ] = data[ 'amount' ].cumsum()
            if not data.empty:
                data.plot( x='date', y=title, ax=ax, drawstyle='steps-post' )

    def plotLayer( self, stack, layer, title, ax ):
        if stack is None:
            stack = layer
        else:
            stack = pd.concat( [ stack, layer ] ).sort_values( 'date' ).reset_index( drop=True )
        stack[ title ] = stack[ 'amount' ].cumsum()
        stack.plot( x='date', y=title, ax=ax, drawstyle='steps-post' )
        return stack[ internalFmt ]

    def plotStack( self, df, ax ):
        data = self.filter( df )
        stack = None
        for g in self.groups:
            stack = self.plotLayer( stack, data[ g.title ], g.title, ax )
        self.plotLayer( stack, data[ 'Other' ], 'Other', ax )
    
    def plotPie( self, df, ax ):
        total = { title: abs( data[ 'amount' ].sum() ) for title, data in self.filter( df ).items() }
        series = pd.Series( total, name="" ).sort_values()
        series.plot.pie( ax=ax, autopct='%1.0f%%', startangle=90,
                         labels=[ "%s:$%1.2f" % item for item in series.iteritems() ] )

defaultFile = os.path.join( '.', 'userdata', 'groups.yaml' )
class GroupMan( object ):
    def __init__( self, groups=[], updateCb=lambda active:None ):
        self.groups = { i:g for i, g in enumerate( groups ) }
        self.updateCb = updateCb
        self.uids = len( self.groups )
        self.active = set() # keys pointing to active groups
    
    def create( self ):
        i = self.uids
        self.uids += 1
        self.groups[ i ] = Group( "Untitled", [], [], False )
        return i
    
    def setActive( self, key, state ):
        if state:
            self.active.add( key )
        else:
            self.active.discard( key )
        self.updateCb( self.active )
    
    def load( self, filename=defaultFile ):
        'load groups from file, add to existing groups. returns successful'
        try:
            with open( filename, 'r' ) as f:
                ingroup = { i:Group( **g ) for i, g in enumerate( yaml.load( f, Loader=yaml.FullLoader ), start=self.uids ) }
                self.uids += len( ingroup )
                self.groups.update( ingroup )
                self.updateCb( self.active )
            return True
        except FileNotFoundError:
            return False

    def save( self, filename=defaultFile ):
        'save groups to file'
        with open( filename, 'w' ) as f:
            yaml.dump( [ dict( g ) for g in self.groups.values() ], f )