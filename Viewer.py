from random import randint
# class for views that need to update to follow backer data

class Viewer( object ):
  def __init__( self, backer=[] ):
    self.backer = {}
    for b in backer:
      self.addBacker(b)
  
  def addBacker( self, backer ):
    self.backer[ backer ] = backer.register( self.onUpdate )

  def __del__( self ):
    for b, id in self.backer.items():
      b.unregister( id )

  def onUpdate( self ):
    '''implement in children'''
    pass