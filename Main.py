from Group import load as loadGroups
from Ledger import loadLedger
import matplotlib.pyplot as plt
import pandas as pd

import pdb

# import all the data
ledger = loadLedger()

# make an overall graph
pd.plotting.register_matplotlib_converters()
plt.figure()
ax = plt.gca()
for g in loadGroups():
    g.plotCumulative( ledger, ax )
plt.show()