from Backer import Backer

class PlotSettings( Backer ):
    # static members
    typesInclusive = [ "event", "cumulative" ]
    typesExclusive = typesInclusive + [ "stack", "bar", "pie" ]
    choiceToFunc = dict(
        event="plotAmount",
        cumulative="plotCumulative",
        stack="plotStack",
        pie="plotPie",
        bar="plotBar"
    )

    def __init__(self):
        Backer.__init__( self, None )
        self.exclusive = True
        self.plotType = list(self.choiceToFunc.values() )[ 0 ]
        self.dateRange = None, None

    def setPlotType( self, choice ):
        # TODO: decouple the display from the internal choice
        self.plotType = self.choiceToFunc[ choice ]
        self.push()