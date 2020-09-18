import tkinter as tk
from Scrollable import Scrollable
from Table import tableFromDf
# window for editing a group

def editGroupCb( master, group, ledger ):
    def cb( master=master, group=group, ledger=ledger ):
        top = tk.Toplevel( master )
        mainFrame = tk.Frame( top )
        mainFrame.pack( side=tk.LEFT, fill=tk.BOTH, expand=True)
        listFrame = tk.Frame( top )
        listFrame.pack( side=tk.RIGHT, fill=tk.Y, expand=True )
        
        whiteList = Scrollable( listFrame, vertical=True )
        whiteList.pack( side=tk.TOP, fill=tk.Y )
        blackList = Scrollable( listFrame, vertical=True )
        blackList.pack( side=tk.BOTTOM, fill=tk.Y )

        nameFrame = tk.Frame( mainFrame )
        nameFrame.pack( side=tk.TOP, fill=tk.X, expand=True )
        name = tk.Entry( nameFrame, exportselection=0 )
        name.pack( side=tk.LEFT, fill=tk.X, expand=True )
        var = tk.StringVar( nameFrame )
        var.set( "income" )
        style = tk.OptionMenu( nameFrame, var, "income", "expense" )
        style.pack( side=tk.RIGHT, fill=tk.NONE, expand=False )

        scroll = Scrollable( mainFrame, True, True )
        scroll.pack( side=tk.BOTTOM, fill=tk.BOTH, expand=True )
        preview = tableFromDf( scroll, ledger.df )
        preview.pack( fill=tk.BOTH, expand=True )

        master.wait_window( top )
    return cb