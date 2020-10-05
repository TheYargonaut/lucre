import tkinter as tk

class Scrollable( tk.Frame ):
    '''wrap a frame for scrolling'''
    def __init__( self, parent, horizontal=False, vertical=False, **kwargs ):
        self.superFrame = tk.Frame( parent, **kwargs )
        self.superFrame.grid_rowconfigure( 0, weight=1 )
        self.superFrame.grid_columnconfigure( 0, weight=1 )
        self.canvas = tk.Canvas( self.superFrame )

        tk.Frame.__init__( self, self.canvas )
        self.bind( '<Configure>', self.confPropagate )
        self.canvas.create_window( ( 0, 0 ), window=self, anchor='nw' )

        confArgs = {}
        self.horizontal = horizontal
        if horizontal:
            self.hScrollBar = tk.Scrollbar(
                self.superFrame, orient='horizontal',
                command=self.canvas.xview )
            self.hScrollBar.grid( row=1, column=0, sticky=tk.E+tk.W )
            confArgs[ 'xscrollcommand' ] = self.hScrollBar.set
        
        self.vertical = vertical
        if vertical:
            self.vScrollBar = tk.Scrollbar(
                self.superFrame, orient='vertical',
                command=self.canvas.yview )
            self.vScrollBar.grid( row=0, column=1, sticky=tk.N+tk.S )
            confArgs[ 'yscrollcommand' ] = self.vScrollBar.set
        
        if confArgs:
            self.canvas.configure( **confArgs )
        self.canvas.grid( row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
    
    def confPropagate( self, _ ):
        sizeArgs = dict( scrollregion=self.canvas.bbox( 'all' ) )
        if True or not self.horizontal or self.winfo_width() < self.canvas.winfo_width():
            sizeArgs[ 'width' ] = self.winfo_width()
        if True or not self.vertical or self.winfo_height() < self.canvas.winfo_height():
            sizeArgs[ 'height' ] = self.winfo_height()
        self.canvas.configure( **sizeArgs )

    
    def pack( self, *args, **kwargs ):
        self.superFrame.pack( *args, **kwargs )
    
    def grid( self, *args, **kwargs ):
        self.superFrame.grid( *args, **kwargs )
    
    def sizeCanvas( self ):
        self.canvas.config( height=self.winfo_height(), width=self.winfo_width() )