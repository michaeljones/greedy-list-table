
Greedy List Table
=================

The concept of the GreedyListTable is a list-table implementation that does
not mind you having different numbers of cells in each row.  It simply
finds the longest row and then extends the first or last cell of all
shorter rows to span the number of columns required to catch up.

This makes the table only marginally more flexible but that is enough to
avoid using the full reStructuredText table syntax in some situations.


