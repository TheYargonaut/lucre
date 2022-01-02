from Backer import Backer
from Format import internalFmt

import os, yaml, pdb
import pandas as pd
from functools import reduce
import numpy as np

# basic event grouping

def matchAny( regexList, df, column='memo' ):
    return reduce( lambda x,y: x | y,
                   ( df[ column ].str.contains( r ) 
                     for r in regexList if r ),
                   False )

class Group( object ):
    def __init__( self, title="", whitelist=[], blacklist=[], negate=False, color=None ):
        '''blacklist overrides whitelist'''
        self.title = title
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.negate = negate
        self.color = color
    
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
        df.plot( x='date', y=self.title, ax=ax, marker='o', color=self.color, linestyle='' )
    
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
        df.plot( x='date', y=self.title, ax=ax, drawstyle="steps-post", color=self.color )

    def keys( self ):
        return 'title', 'whitelist', 'blacklist', 'negate', 'color'

    def __getitem__( self, key ):
        return getattr( self, key )

class Partition( object ):
    def __init__( self, groups=[], blacklist=[], negate=False, otherColor=None ):
        'negate applies to the other group'
        self.groups = groups
        self.blacklist = blacklist
        self.negate = negate
        self.otherColor = otherColor
    
    def colorDict( self ):
        cd = { g.title : g.color for g in self.groups }
        cd[ 'Other' ] = self.otherColor
        return cd
    
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
        cd = self.colorDict()
        for title, data in self.filter( df, False ).items():
            data.loc[ :, title ] = data[ 'amount' ]
            if not data.empty:
                data.plot( x='date', y=title, ax=ax, marker='o', color=cd[ title ], linestyle='' )

    def plotCumulative( self, df, ax ):
        cd = self.colorDict()
        for title, data in self.filter( df ).items():
            data[ title ] = data[ 'amount' ].cumsum()
            if not data.empty:
                data.plot( x='date', y=title, ax=ax, drawstyle='steps-post', color=cd[ title ] )

    def plotLayer( self, stack, layer, title, ax, cd ):
        if stack is None:
            stack = layer
        else:
            stack = pd.concat( [ stack, layer ] ).sort_values( 'date' ).reset_index( drop=True )
        stack[ title ] = stack[ 'amount' ].cumsum()
        stack.plot( x='date', y=title, ax=ax, drawstyle='steps-post', color=cd[ title ] )
        return stack[ internalFmt ]

    def plotStack( self, df, ax ):
        cd = self.colorDict()
        data = self.filter( df )
        stack = None
        for g in self.groups:
            stack = self.plotLayer( stack, data[ g.title ], g.title, ax, cd )
        self.plotLayer( stack, data[ 'Other' ], 'Other', ax, cd )
    
    def plotPie( self, df, ax ):
        total = { title: abs( data[ 'amount' ].sum() ) for title, data in self.filter( df ).items() }
        series = pd.Series( total, name="" ).sort_values()
        cd = self.colorDict()
        colors = [ cd[s] for s in series.keys() ]
        series.plot.pie( ax=ax, autopct='%1.0f%%', labeldistance=1.1,
                         title="Total: $%1.2f" % sum( total.values() ),
                         labels=[ "%s: $%1.2f" % item for item in series.iteritems() ],
                         colors=colors )
    
    def plotBar( self, df, ax ):
        total = { title: abs( data[ 'amount' ].sum() ) for title, data in self.filter( df ).items() }
        series = pd.Series( total, name="" ).sort_values( ascending=False )
        cd = self.colorDict()
        colors = [ cd[s] for s in series.keys() ]
        series.plot.bar( ax=ax, color=colors )

defaultFile = os.path.join( '.', 'userdata', 'groups.yaml' )
def randomColor():
    return '#%06x' % np.random.randint( 0xFFFFFF )
class GroupMan( Backer ):
    def __init__( self, groups=[] ):
        self.groups = { i:g for i, g in enumerate( groups ) }
        Backer.__init__( self, self.groups )
        self.uids = len( self.groups )
        self.active = set() # keys pointing to active groups
        self.newColorCache = None
    
    def newColor( self ):
        colors = [ g.color.lower() for g in self.groups.values() if g.color ]
        nc = self.newColorCache
        while ( not nc ) or nc in colors:
            nc = randomColor()
        self.newColorCache = nc
        return nc
    
    def create( self ):
        i = self.uids
        self.uids += 1
        self.groups[ i ] = Group( "Untitled", [], [], False, self.newColor() )
        return i
    
    def setActive( self, key, state ):
        if state:
            self.active.add( key )
        else:
            self.active.discard( key )
        self.push()
    
    def load( self, filename=defaultFile ):
        'load groups from file, add to existing groups. returns successful'
        try:
            with open( filename, 'r' ) as f:
                raw = yaml.load( f, Loader=yaml.FullLoader )
        except FileNotFoundError:
            return False
        if raw:
            ingroup = { i:Group( **g ) for i, g in enumerate( raw, start=self.uids ) }
            self.uids += len( ingroup )
            # assign color where it doesn't exist yet
            # for g in ingroup.values():
            #     if not g.color:
            #         g.color = self.newColor()
            self.groups.update( ingroup )
            self.push()
        return True

    def save( self, filename=defaultFile ):
        'save groups to file'
        with open( filename, 'w' ) as f:
            yaml.dump( [ dict( g ) for g in self.groups.values() ], f )