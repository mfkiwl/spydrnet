.. _sec:api_spec:

API Specification
=================

The SpyDrNet API can be used to create, analyze, and transform a netlist. Netlist are represented in memory in an Intermediate Representation. :numref:`fig:ExampleIR` show the representation of a simple circuit in the SpyDrNet Intermediate Representation.


.. _fig:ExampleIR:
.. figure:: ../figures/ExampleCircuit.png
   :align: center
   :alt: Example Netlist in a SpyDrNet Intermediate Representation

   Example Netlist in the Intermediate Representaion

The API calls documented here can be used in Python as follows:

>>> # create an empty netlist and add an empty library to it
>>> import spydrnet as sdn
>>> netlist = sdn.ir.Netlist()
>>> library = netlist.create_library()
>>>

Similarly if the parser is used the calls can be made in the same way:

>>> # parse an edif file in and add an empty library to the netlist.
>>> import spydrnet as sdn
>>> netlist = sdn.parse('four_bit_counter.edf')
>>> library = netlist.create_library
>>>

.. automodule:: spydrnet.ir

.. autoclass:: Netlist
    :members:
    :undoc-members:
    
.. autoclass:: Library
    :members:
    :undoc-members:
    
.. autoclass:: Definition
    :members:
    :undoc-members:
    
.. autoclass:: Instance
    :members:
    :undoc-members:
    
.. autoclass:: Port
    :members:
    :undoc-members:

.. autoclass:: InnerPin
    :members:
    :undoc-members:

.. autoclass:: OuterPin
    :members:
    :undoc-members:

.. autoclass:: Cable
    :members:
    :undoc-members:

.. autoclass:: Wire
    :members:
    :undoc-members:

The following three classes are the classes from which the above elements inherit. They are included here for completeness of
documenataion and can be used if needed. if the above types will suffice it may be simpler to use them.

.. autoclass:: Pin
    :members:
    :undoc-members:

.. autoclass:: Bundle
    :members:
    :undoc-members:

.. autoclass:: Element
    :members:
    :undoc-members:
    
.. automodule:: spydrnet.util.hierarchical_reference

.. autoclass:: HRef

.. automodule:: spydrnet.clone
   :members:

.. automodule:: spydrnet.uniquify
   :members:
   
.. automodule:: spydrnet.flatten
   :members:
   
.. automodule:: spydrnet.util.get_netlists
   :members:

.. automodule:: spydrnet.util.get_libraries
   :members:
   
.. automodule:: spydrnet.util.get_definitions
   :members:

.. automodule:: spydrnet.util.get_instances
   :members:

.. automodule:: spydrnet.util.get_ports
   :members:

.. automodule:: spydrnet.util.get_pins
   :members:

.. automodule:: spydrnet.util.get_cables
   :members:

.. automodule:: spydrnet.util.get_wires
   :members:

.. automodule:: spydrnet.util.get_hinstances
   :members:

.. automodule:: spydrnet.util.get_hports
   :members:

.. automodule:: spydrnet.util.get_hpins
   :members:

.. automodule:: spydrnet.util.get_hcables
   :members:

.. automodule:: spydrnet.util.get_hwires
   :members:
