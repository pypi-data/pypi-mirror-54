########
a3cosmos
########

********************************************************************
A Python Package of A3COSMOS Astronomical Data and Catalog Utilities
********************************************************************




A simple introduction:
======================

This Python package contains some useful functions to query A3COSMOS catalog and make cutout images. 

It is currently under development. 




A simple usage:
===============

To query source by RA Dec coordinate::
    import a3cosmos as a3c
    a3cosmos.find_source(RA = 150.0, Dec = 2.0)



To make a cutout image centered at a source RA Dec coordinate::
    import a3cosmos as a3c
    a3cosmos.make_cutout(RA = 150.0, Dec = 2.0, FoV = 10, Band='Ks')
    # Note that this is currently not working for ALMA images because our data are still waiting to be released on COSMOS IRSA website.



More functions underway::
    TODO




