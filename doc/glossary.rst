Glossary
========


.. glossary::

    Cardinality
        The quality related to the contour size. The number of
        elements of a contour.

    Contour
        Shape, format or outline of an object.

    Contour Adjacency Series (CAS)
        The series of ascendent and descendent movements between
        adjacent elements of a contour. The first internal diagonal
        returns CAS.

    Contour Adjacency Series Vector (CASV)
        Two digit summation of ups and downs in Contour Adjacency
        Series of a contour segment. The first digit signifies ups,
        and second, downs.

    Contour Class
        A class of csegs that shares the same prime form. We use
        Morris definition, instead Friedmann (see `Friedmann 1987
        <contour-theories.html>`_).

    Contour Class Vector I (CCVI)
        Two digit summation of the frequency of ups and
        downs. Final result is the sum of number of elements and
        contour interval multiplication.

    Contour Class Vector II (CCVII)
        Two digit summation of the frequency of ups and downs. Final
        result is the sum of number of elements of a contour interval
        type.

    Contour Equivalence Classes
        Two csegs have equivalent class if they have the same
        comparison Matrix, or if they are related by identity,
        translation, retrograde, inversion and retrograde-inversion.

    Contour Interval (CI)
        Diference between two cpitch values in a cseg.

    Contour Interval Array (CIA)
        An array with the multiplicity of contour intervals types in a
        cseg.

    Contour Interval Succession (CIS)
        A succession of all adjacent contour intervals in a cseg.

    Cpitch
        Contour pitch. Each element of a cseg.

    Cseg
        Contour segment. A contour space subset with adjacent or
        non-adjacent elements.

    Contour Similarity
        A numeric measure for similarity between csegs with the same
        cardinality. It varies from 0 to 1, representing minimum to
        maximum similarity.

    C-space
        Contour space. The abstraction of musical elements ordered
        from low to high disregarding their absolute values.

    Embed Contour
        A numeric measure for similarity between csegs with different
        cardinality. A embed contour has its comparison matrix embed
        in bigger contour.

    Internal Diagonal
        The diagonals above zero main diagonal in a Comparison
        Matrix.

    Maximum pitch (Morris 1993, p. 212)
        Given three adjacent pitches in a contour, if the second is
        higher than or equal to the others it is a maximum. A set of
        maximum pitches is called a maxima. The first and last pitches
        of a contour are maxima by definition.

    Minimum pitch (Morris 1993, p. 212)
        Given three adjacent pitches in a contour, if the second is
        lower than or equal to the others it is a minimum. A set of
        minimum pitches is called a minima. The first and last pitches
        of a contour are minima by definition.

    Normal form
        A contour representation in which elements are enumerated in
        integers from 0, to lowest cpitch to n - 1, to highest pitch,
        where n is contour cardinality. Equal to Friedmann contour
        class.

    Prime form
