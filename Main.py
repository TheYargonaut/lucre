from Group import load as loadGroups, save as saveGroups, Partition
from Ledger import loadLedger, loadFormats, saveFormats, saveLedger, importLedger, Ledger
from Table import tableFromDf
import matplotlib.pyplot as plt
import pandas as pd
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from Scrollable import Scrollable
from ImportLedger import importLedgerCb

import pdb

# import all the data
ledger = loadLedger()
groups = loadGroups()
formats = loadFormats()

ledgerManager = Ledger( ledger )

top = tk.Tk()
importLedgerButton = tk.Button( top, text="Import Ledger", command=importLedgerCb( top, ledgerManager ) )
importLedgerButton.pack()
top.mainloop()


expensePart = Partition( [ g for g in groups if g.negate ], sum( [
   g.whitelist + g.blacklist for g in groups if not g.negate
], [] ), negate=True )

# make an overall graph
pd.plotting.register_matplotlib_converters()
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