from Group import load as loadGroups, Partition
from Ledger import loadLedger
import matplotlib.pyplot as plt
import pandas as pd

import pdb

# import all the data
ledger = loadLedger()
groups = loadGroups()

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