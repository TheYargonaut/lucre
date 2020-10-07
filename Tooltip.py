import tkinter as tk

class Tooltip( object ):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind( "<Enter>", self.enter )
        self.widget.bind( "<Leave>", self.close )
    
    def destroy( self ):
        self.widget.unbind( "<Enter>" )
        self.widget.unbind( "<Leave>" )

    def enter( self, event=None ):
        x = y = 0
        x, y, cx, cy = self.widget.bbox( "insert" )
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel( self.widget )
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect( True )
        self.tw.wm_geometry( "+%d+%d" % ( x, y ) )
        label = tk.Label( self.tw, text=self.text, justify='left',
                          background='yellow', relief='solid', borderwidth=1 )
        label.pack( ipadx=1 )

    def close( self, event=None ):
        if self.tw:
            self.tw.destroy()