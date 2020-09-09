from Group import load as loadGroups, save as saveGroups, Partition
from Ledger import loadLedger, loadFormats, saveFormats, saveLedger
import matplotlib.pyplot as plt
import pandas as pd
import os

import pdb

# import all the data
ledger = loadLedger()
groups = loadGroups()
formats = loadFormats()

expensePart = Partition( [ g for g in groups if g.negate ], sum( [
   g.whitelist + g.blacklist for g in groups if not g.negate
], [] ), negate=True )

# make an overall graph
pd.plotting.register_matplotlib_converters()
plt.figure()
ax = plt.gca()
expensePart.plotPie( ledger, ax )
# for g in loadGroups():
#     g.plotCumulative( ledger, ax )
plt.show()

if not os.path.exists( os.path.join( '.', 'userdata' ) ):
    os.mkdir( os.path.join( '.', 'userdata' ) )
saveFormats( formats )
saveLedger( ledger )
saveGroups( groups )