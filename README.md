# lucre

This is a simple visualization tool intended to help visualize personal finances.

If you ever wondered where all your money was going and thought a graph would help, this tool may be of use.

## Getting Started

0. Set up a Python3 environment with the packages listed in `requirements.txt`
1. From your financial institution's web page, download your activity for each account you are interest in as a Comma-Separated Value (CSV) spreadsheet
2. Run this program from `Main.py` using your python environment from step **0**
3. Use the "Import Ledger" button on the main screen to load the spreadsheets from step **1** to the program
4. Use the Groups on the right to group transactions to display together
5. Use the options at the bottom right to control what type of graph is made with the transactions and groups

## Feature List

- Group transactions together using regular expressions with a simple real-time preview
- Allow the groups to overlap or have them own transactions exclusively
- Specify whether each group tracks mainly income or expenses
- Import from different layouts by specifying relevant columns
- Save and re-use groups, formats, and your ledger
- Provide easy access to multiple different kinds of chart, including individual events, cumulative change, combined change, and pie charts

## Potential Features

- Specify budget for a group and compare to actual transactions
- Specify an amount in an account in order to track state and not just changes
- Collect common downloadable formats for various financial institutions
- Integrate with financial institution APIs
- Basic prediction and analysis tools
- Controls for graph including export image, appearance adjustment, subplots, date range
- Undo/redo buffer
- Ledger editing
- Look less ugly
- Installer that doesn't require knowledge of python and git