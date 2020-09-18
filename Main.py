from Group import load as loadGroups, save as saveGroups, Partition, Group
from Ledger import loadLedger, loadFormats, saveFormats, saveLedger, importLedger, Ledger
from Table import tableFromDf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from Scrollable import Scrollable
from ImportLedger import importLedgerCb
from EditGroup import editGroupCb

import pdb

pd.plotting.register_matplotlib_converters()

# import all the data
ledger = loadLedger()
groups = loadGroups()
formats = loadFormats()

ledgerManager = Ledger( ledger )

# make the window
top = tk.Tk()

fig = plt.Figure()
ax = fig.add_subplot( 111 )
chartWidget = FigureCanvasTkAgg( fig, top )
chartWidget.get_tk_widget().pack( side=tk.LEFT, fill=tk.BOTH, expand=True )

controlFrame = tk.Frame( top )
controlFrame.pack( side=tk.RIGHT, fill=tk.Y )

importLedgerButton = tk.Button( controlFrame, text="Import Ledger", command=importLedgerCb( top, ledgerManager ) )
importLedgerButton.pack( side=tk.TOP, fill=tk.X )

addGroupButton = tk.Button( controlFrame, text="New Group", command=editGroupCb( top, Group(), ledgerManager ) )
addGroupButton.pack( side=tk.BOTTOM, fill=tk.X )

top.mainloop()


expensePart = Partition( [ g for g in groups if g.negate ], sum( [
   g.whitelist + g.blacklist for g in groups if not g.negate
], [] ), negate=True )

# make an overall graph

plt.figure()
ax = plt.gca()
expensePart.plotPie( ledgerManager.df, ax )
# for g in loadGroups():
#     g.plotCumulative( ledger, ax )
plt.show()

# save current settings
if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
saveFormats( formats )
saveLedger( ledgerManager.df )
saveGroups( groups )