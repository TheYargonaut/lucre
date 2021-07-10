import tkinter as tk
from tkinter import ttk
from List import ListView

# control widget for groups

class GroupControlWidget( ttk.Frame ):
    def __init__( self, parent, label, back, addCb=lambda:None, activeCb=lambda *_:None, editCb=lambda *_:None ):
        ttk.Frame.__init__( self, parent )

        self.label = label
        self.back = back
        self.addCb = addCb
        self.activeCb = activeCb
        self.editCb = editCb

        self.active = tk.IntVar()
        self.active.set( 0 )

        self.activateButton = None
        self.color = None

        self.build()

    def build( self ):
        self.grid_columnconfigure( 0, weight=1 )

        self.activateButton = ttk.Checkbutton(
            self,
            variable=self.active,
            text=self.back[ self.label ].title,
            command=self.activate
        )
        self.activateButton.grid( row=0, column=0, rowspan=2, sticky=tk.NSEW )
        
        remover = ttk.Button( self, text='Delete', command=self.remove )
        remover.grid( row=0, column=1, sticky=tk.NSEW )
        editor = ttk.Button( self, text='Edit', command=self.edit )
        editor.grid( row=1, column=1, sticky=tk.NSEW )

        self.color = tk.Label( self, text="\u2B1B", fg=self.back[ self.label ].color )
        self.color.grid( row=0, column=2, rowspan=2, sticky=tk.NSEW )

    def activate( self ):
        self.activeCb( self.label, self.active.get() )

    def remove( self ):
        self.activeCb( self.label, False )
        del self.back[ self.label ]
        self.destroy()

    def edit( self ):
        self.editCb( self.label )
        self.activateButton.config( text=self.back[ self.label ].title )
        self.color.config( fg=self.back[ self.label ].color )

class GroupList( ListView ):
    def __init__( self, parent, back=[], addButton=None, addCb=lambda:None, activeCb=lambda *_:None, editCb=lambda *_:None, **kwargs ):
        self.addCb = addCb
        self.activeCb = activeCb
        self.editCb = editCb
        ListView.__init__( self, parent, back, addButton, **kwargs )

    def makeCell( self, label, **kwargs ):
        return GroupControlWidget( self, label, self.back, self.addCb, self.activeCb, self.editCb )
    
    def appendCell( self ):
        self.cells.append( self.initCell( self.addCb() ) )