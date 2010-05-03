Contour Operations
==================

Contour theories provides many contour operations. Eight of them are
implemented in |VLCM|:

.. index:: Retrograde

Retrograde
----------

Reverse cseg.

For instance::

 A < 0 1 2 3 >

 Retrograde(A) = < 3 2 1 0 >

.. index:: Inversion

Inversion
---------

The cseg horizontal inversion. The cseg is renumbered under `Morris
(1987) <contour-theories.html>`_ inversion formula::

 I(x)n = (n - 1) - x

where n = contour cardinality and x is cpitch.

For instance::

 A < 5 3 4 1 2 0 >

 n = 6

 I(5)6 = (6 - 1) - 5 = 0
 I(3)6 = (6 - 1) - 3 = 2
 I(4)6 = (6 - 1) - 4 = 1
 I(1)6 = (6 - 1) - 1 = 4
 I(2)6 = (6 - 1) - 2 = 3
 I(0)6 = (6 - 1) - 0 = 5

Thus::

 Inversion(A) = <0 2 1 4 3 5>

.. index:: Rotation

Rotation
--------

In rotation the cseg is split and the primer cpitches become the
last ones. It accepts a rotation parameter.

For instance::

 A = < 0 1 2 3 >

 Rotation(A, 1) = < 1 2 3 0 >
 Rotation(A, 2) = < 2 3 0 1 >
 Rotation(A, 3) = < 3 0 1 2 >

.. index:: Normal form
.. index:: Translation

Normal form (translation)
-------------------------

A contour is in its Normal form when reenumerated in integers from 0
to lower cpitch to (n - 1) to highest cpitch, where n is the contour
cardinality. Normal form is accomplished by translation operation.

For instance::

 A = < 2 5 8 9 1 >
 Translation(A) = < 1 2 3 4 0 >

 B = < 3 34 21 55 >
 Translation(B) = < 0 2 1 3 >

.. index:: Prime form

Prime form
----------

The Prime form is calculated by Marvin and Laprade Prime Form
Algorithm `(1987) <contour-theories.html>`_::

 1) Translate, if not consecutive integers 0 to (n - 1):
 2) Invert, if [(n - 1) - last cpitch] < first cpitch
 3) Retrograde, if last cpitch < first cpitch

For instance::

 A < 3 0 2 1 >
 2) Inversion(A) = < 0 3 1 2 >

 B < 1 2 0 4 >
 1) Translation(B) = B' < 1 2 0 3>
 2) Invertion(B') = B'' < 2 1 3 0 >
 3) Retrograde(B'') = < 0 3 1 2 >

In this example, A and B have the same prime form::

 < 0 3 1 2 >

In GUI, Prime form operation returns also the contour segment class
number, like in Marvin and Laprade C-space segment-classes table
`(1987) <contour-theories.html>`_.

For example::

 A < 5 2 9 4 1 3 >
 Prime form(A) = 6-163 < 1 4 0 2 5 3 >

The pair 6-163 means cardinality and Prime form order.

.. index:: Comparison Matrix
.. index:: COM-Matrix

Comparison Matrix
-----------------

Comparison Matrix (also known as COM-Matrix) returns a matrix with
comparison between all elements of a contour. The result of a
comparison is 0, + ou -. The Comparison Matrix is described by `Morris
(1987) <contour-theories.html>`_.

For example, matrix for < 0 3 1 2 >::

   | 0 3 1 2
 -----------
 0 | 0 + + +
 3 | - 0 - -
 1 | - + 0 +
 2 | - + - 0

In this example, in the first line, all cpitches of cseg are compared
with first column element, 0. So, assuming that COM(a, b) is the
comparison function between a and b elements::

 COM(0, 0) = 0
 COM(0, 3) = +
 COM(0, 1) = +
 COM(0, 2) = +

 COM(3, 0) = -
 COM(3, 3) = 0
 COM(3, 1) = -
 COM(3, 2) = -

Internal Diagonal
-----------------

The Internal diagonals are yanked from the Comparison matrix, from top
left to bottom right, above the main diagonal. The main diagonal is
filled by zeros.

In this figure, INT_1, INT_2, and INT_3 means internal diagonal 1, 2,
and 3. 

.. image:: figs/internal_diagonals.png

For this Comparison matrix, internal diagonals are::

 Internal diagonal(1) = < + - + >
 Internal diagonal(2) = < + - >
 Internal diagonal(3) = < + >

Michael Friedmann `(1985) <bibliography.html>`_ named the ups and
downs of a contour as Contour Adjacency Series.

.. index:: Subsets

Subsets
-------

Returns subsets from a contour with a given cardinality.

For example, for a given contour A, all 3 elements subsets::

 A < 0 3 1 2 >
 Subsets(3) =  < 0 1 2 >, < 0 3 1 >, < 0 3 2 >, < 3 1 2 >

.. index:: Contour segments for an internal diagonal

Contour segments for an internal diagonal
-----------------------------------------

Returns all possible csegs for a given internal diagonal.

For instance::

 INT(1) = < - + - >
 Possible csegs:
 < 1 0 3 2 >
 < 2 0 3 1 >
 < 2 1 3 0 >
 < 3 0 2 1 >
 < 3 1 2 0 >

The other internal diagonals can be used as input::

 INT(2) = < - + >
 Csegs:
 < 1 2 0 3 >
 < 2 0 1 3 >
 < 2 1 0 3 >
 < 3 0 1 2 >
 < 3 0 2 1 >
 < 3 1 0 2 >

In |VLCM| GUI, the internal diagonal must be given with 1 and -1, and
internal number must be in parameter entry::

 Main entry: -1 1 -1 
 Parameter: 1

.. index:: Contour Adjacency Series Vector (CASV)

Contour Adjacency Series Vector (CASV)
--------------------------------------

Two digit summation of ascendent and descendent movements in Contour
Adjacency Series (Internal diagonal 1) of a contour segment. The first
digit signifies ups, and second, downs. Also known as CASV.

For instance::

 A < 0 4 1 3 2 5 >
 Internal diagonal(A, 1): < + - + - + >
 ups: 3
 downs: 2
 Contour Adjacency Series Vector(A): < 3 , 2 >

.. index:: Contour Interval Succession (CIS)

Contour Interval Succession (CIS)
---------------------------------

A succession of all adjacent contour intervals in a cseg. Also known
as CIS.

For instance::

 A < 0 4 1 >
 Contour Interval Succession(A): < +4, -1 >

 B < 0 3 2 4 >
 Contour Interval Succession(B): < +3, -1, +2 >

.. index:: Contour Interval Array (CIA)

Contour Interval Array (CIA)
----------------------------

An array with the multiplicity of contour intervals types in a cseg.

For instance::

 A < 0 3 2 4 >
 Contour Interval Array(A): [[1, 2, 1], [1, 0, 0]]

Cseg A has one ascendent contour interval of type 1 (3 4), two of type
2 (0 2 and 2 4), one of type 3: (0 3). Cseg A has also one descendent
contour interval of type -1: (3 2), and zero contour interval of types
-2 and -3.

.. index:: Contour Class Vector I (CCVI)

Contour Class Vector I (CCVI)
-----------------------------

Two digit summation of the frequency of ascendent and descendent
movements. Final result is the sum of number of elements and contour
interval multiplication.

For instance::

 A < 0 3 2 4 >
 Contour Interval Array(A): [[1, 2, 1], [1, 0, 0]]
 Contour Class Vector I(A): [8, 1]

 Contour Class Vector I(A): [(1*1)+(2*2)+(3*1), (1*1)+(2*0)+(3*0)]

.. index:: Contour Class Vector II (CCVII)

Contour Class Vector II (CCVII)
-----------------------------

Two digit summation of the frequency of ups and downs. Final result is
the sum of number of elements of a contour interval type.

For instance::

 A < 0 3 2 4 >
 Contour IInterval Array(A): [[1, 2, 1], [1, 0, 0]]
 Contour Class Vector II(A): [4, 1]

 Contour Class Vector II(A): [1+2+1, 1+0+0]

.. index:: Contour Similarity

Contour Similarity
------------------

A numeric measure for similarity between csegs with the same
cardinality. It varies from 0 to 1, representing minimum to maximum
similarity. Each specific position of comparison matrix superior
triangle of one contour segment is compared with the corresponding
position in the other contour segment. The similarity value is given
by the quotient between sum of similar content positions and total of
positions.

.. image:: figs/superior_triangle.png

For instance, these two contour segments, < 0 3 1 2 > and < 0 2 1 3 >
differ in comparison matrix superior triangle only in one position
(marked in figure). Five of six positions have the same value in both
segments. Thus, contour similarity is 5/6, or 0.83.

.. |VLCM| replace:: Villa-Lobos Contour Module
