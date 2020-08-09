# lucre
Budget and spending dashboard

Features
- Create groups
- use regex matching to automatially load from records (for each group) of various bank formats
- save as common format (date, change amount, original desc)
- allow blacklists to eliminate overlaps (like transfers between accounts, redundant entries)
- Graph real change over time (include amount at some time as context, adjust to amounts instead of assuming 0)

Todo
- build defaults on first run (or whenever expected config not present)
- Budgeting for each group (and plot alongside real, project into future)
- Mutually exclusive groupings to partition
- Adjust cumulative amounts given an amount at a given time so absolute amounts correct
- pie graphs given partition
- GUI, including time range choice and interactive ledger import
- collect common downloadable formats for various financial institutions (good defaults)
- integrate with financial institution APIs