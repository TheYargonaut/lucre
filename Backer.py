class Backer( object ):
  def __init__( self, data ):
    self.data = data
    self.viewer = {}
    self.idGen = 0

  def register( self, onUpdate ):
    self.idGen += 1
    self.viewer[ self.idGen ] = onUpdate
    return self.idGen
  
  def unregister( self, id ):
    if id in self.viewer:
      del self.viewer[ id ]
  
  def push( self ):
    for v in self.viewer.values():
      v()