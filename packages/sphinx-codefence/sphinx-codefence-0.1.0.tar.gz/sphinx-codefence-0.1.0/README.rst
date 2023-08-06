===========================
Sphinx Code Fence Extension
===========================

This is a single-module sphinx extension that monkey-patches docutils adding
the ability to parse code fences. For example, the following code fence is
rendered as a block of python code:

.. code::

    ~~~py
    def hello_codefence():
      print("I am in a codefence!")
    ~~~
