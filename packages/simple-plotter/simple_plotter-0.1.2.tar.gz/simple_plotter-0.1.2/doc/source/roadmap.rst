Roadmap
=======

rel. 0.2
--------

- refactoring: PEP8 compliance for gui.py
- use jinja2 templates for code export?
- tool tips (for groups & buttons)
- checker for equation definition (only valid math and numpy)
- remove error/warning "QCoreApplication::exec: The event loop is already running" (doesn't seem to
  cause functionality issues)
- define/import user data points (from csv file)
- possibility to define imports and alias (import ... as ...)
- auto-resize for constants table
- write test functions for parser
- add possibility to define kwargs for plt.plot
- select scale (lin/log) for set constant generation
- improve error-handling
- improve code documentation

later releases
--------------

- add parameters (constants) optimizer (in conjunction with user data points)
- convert equations to LaTeX
- guess constant's names from function definition
- create code for gnuplot?