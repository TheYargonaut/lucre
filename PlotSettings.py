from Backer import Backer

class PlotSettings( Backer ):
    choiceToFunc = dict(
        event="plotAmount",
        cumulative="plotCumulative",
        stack="plotStack",
        pie="plotPie",
        bar="plotBar"
    )

    def __init__( self ):
        Backer.__init__( self, None )
        self.exclusive = True
        self.plotType = next( v for v in self.choiceToFunc.values() )
        self.dateRange = None, None

    def setPlotType( self, choice ):
        # TODO: decouple the display from the internal choice
        self.plotType = self.choiceToFunc[ choice ]
        self.push()
    
    def setExclusive( self, exclusive ):
        self.exclusive = bool( exclusive )
        self.push()
    
    def setDateRange( self, low, high ):
        self.dateRange = low, high
        self.push()