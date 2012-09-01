
Greedy List Table
=================

Allows you to write::

   .. greedy-list-table::
      :bias: left

      * - The greedy list table is
        - an easy way
        - to create a table which has merged 

      * - cells without going to

      * - all the trouble of using the
        - full reStructuredText syntax 
        - which, whilst rather spiffing for reading in plain text,

      * - can be a little high maintenance.
        - This hopes to help that situation.

      * - In order to be able to pull this off in the relatively
        - simple syntax of the list-table
        - we insist that their is only one cell on each
        - row which can span multiple columns

      * - and that it must be the first or the last.
        - This is only makes the list-table a little more flexible
        - but that little bit is very useful in some circumstances.

And have it render as:

.. greedy-list-table::

   * - The greedy list table is
     - an easy way
     - to create a table which has merged 

   * - cells without going to

   * - all the trouble of using the
     - full reStructuredText syntax 
     - which, whilst rather spiffing for reading in plain text,

   * - can be a little high maintenance.
     - This hopes to help that situation.

   * - In order to be able to pull this off in the relatively
     - simple syntax of the list-table
     - we insist that their is only one cell on each
     - row which can span multiple columns

   * - and that it must be the first or the last.
     - This is only makes the list-table a little more flexible
     - but that little bit is very useful in some circumstances.


And if we switch the bias to 'left' we get:

.. greedy-list-table::
   :bias: left

   * - The greedy list table is
     - an easy way
     - to create a table which has merged 

   * - cells without going to

   * - all the trouble of using the
     - full reStructuredText syntax 
     - which, whilst rather spiffing for reading in plain text,

   * - can be a little high maintenance.
     - This hopes to help that situation.

   * - In order to be able to pull this off in the relatively
     - simple syntax of the list-table
     - we insist that their is only one cell on each
     - row which can span multiple columns

   * - and that it must be the first or the last.
     - This is only makes the list-table a little more flexible
     - but that little bit is very useful in some circumstances.


