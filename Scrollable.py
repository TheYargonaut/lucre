import tkinter as tk

class Scrollable( tk.Frame ):
    '''wrap a frame for scrolling'''
    def __init__( self, parent, horizontal=False, vertical=False, **kwargs ):
        self.superFrame = tk.Frame( parent, **kwargs )
        self.canvas = tk.Canvas( self.superFrame )

        tk.Frame.__init__( self, self.canvas )
        self.bind( '<Configure>',
                   lambda _: self.canvas.configure(
                      scrollregion=self.canvas.bbox( 'all' ) ) )
        self.canvas.create_window( ( 0, 0 ), window=self, anchor='nw' )

        confArgs = {}
        self.horizontal = horizontal
        if horizontal:
            self.hScrollBar = tk.Scrollbar(
                self.superFrame, orient='horizontal',
                command=self.canvas.xview )
            self.hScrollBar.pack( side=tk.BOTTOM, fill=tk.X )
            confArgs[ 'xscrollcommand' ] = self.hScrollBar.set
        
        self.vertical = vertical
        if vertical:
            self.vScrollBar = tk.Scrollbar(
                self.superFrame, orient='vertical',
                command=self.canvas.yview )
            self.vScrollBar.pack( side=tk.RIGHT, fill=tk.Y )
            confArgs[ 'yscrollcommand' ] = self.vScrollBar.set
        
        if confArgs:
            self.canvas.configure( **confArgs )
        self.canvas.pack( side=tk.LEFT, fill=tk.BOTH, expand=True )
    
    def pack( self, *args, **kwargs ):
        self.superFrame.pack( *args, **kwargs )
    
    def grid( self, *args, **kwargs ):
        self.superFrame.grid( *args, **kwargs )
