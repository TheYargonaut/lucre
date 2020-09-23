import tkinter as tk
from Scrollable import Scrollable
from Table import tableFromDf, Table
# window for editing a group

class EditGroupWindow( tk.Toplevel ):
    def __init__( self, master, group, ledger, *args, **kwargs ):
        tk.Toplevel.__init__( self, master, *args, **kwargs )
        self.group = group
        self.ledger = ledger
        self.build()
    
    def build( self ):
        self.grid_rowconfigure( 0, weight=1 )
        self.grid_columnconfigure( 0, weight=1 )
        mainFrame = tk.Frame( self )
        mainFrame.grid( row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
        mainFrame.grid_rowconfigure( 1, weight=1 )
        mainFrame.grid_columnconfigure( 0, weight=1 )
        listFrame = tk.Frame( self )
        listFrame.grid( row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W )
        listFrame.grid_rowconfigure( 0, weight=1 )
        listFrame.grid_rowconfigure( 1, weight=1 )
        listFrame.grid_columnconfigure( 0, weight=1 )
        
        doneButton = tk.Button( listFrame, text="Done", command=self.destroy )
        doneButton.grid( row=3, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
        whiteScroll = Scrollable( listFrame, vertical=True )
        whiteScroll.grid( row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
        whiteList = Table( whiteScroll, ( 2, 1 ) )
        whiteList.pack()
        blackScroll = Scrollable( listFrame, vertical=True )
        blackScroll.grid( row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
        blackList = Table( blackScroll, ( 2, 1 ) )
        blackList.pack()

        nameFrame = tk.Frame( mainFrame )
        nameFrame.grid( row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W )
        name = tk.Entry( nameFrame, exportselection=0 )
        name.pack( side=tk.LEFT, fill=tk.X, expand=True )
        var = tk.StringVar( nameFrame )
        var.set( "income" )
        style = tk.OptionMenu( nameFrame, var, "income", "expense" )
        style.pack( side=tk.RIGHT, fill=tk.NONE, expand=False )

        scroll = Scrollable( mainFrame, True, True )
        preview = tableFromDf( scroll, self.ledger.df )
        preview.pack( fill=tk.BOTH, expand=True )
        scroll.grid( row=1, column=0, sticky=tk.N+tk.S+tk.E )

def editGroupCb( master, group, ledger ):
    def cb( master=master, group=group, ledger=ledger ):
        window = EditGroupWindow( master, group, ledger )
        master.wait_window( window )
    return cb