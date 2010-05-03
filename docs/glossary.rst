Glossary
========


.. glossary::

    cardinality
        The quality related to the contour size. The number of
        elements of a contour.

    contour
        Shape, format or outline of an object.

    c-space
        Contour space. The abstraction of musical elements ordered
        from low to high disregarding their absolute values.

    cseg
        Contour segment. A contour space subset with adjacent or
        non-adjacent elements.

    cpitch
        Contour pitch. Each element of a cseg.

    contour class
        A class of csegs that shares the same prime form. We use
        Morris definition, instead Friedmann (see `Friedmann 1987
        <contour-theories.html>`_).

    contour equivalence classes
        Two csegs have equivalent class if they have the same
        comparison Matrix, or if they are related by identity,
        translation, retrograde, inversion and retrograde-inversion.

    prime form


    normal form
        A contour representation in which elements are enumerated in
        integers from 0, to lowest cpitch to n - 1, to highest pitch,
        where n is contour cardinality. Equal to Friedmann contour
        class.

    internal diagonal
        The diagonals above zero main diagonal in a Comparison
        Matrix.

    contour adjacency series (CAS)
        The series of ascendent and descendent movements between
        adjacent elements of a contour. The first internal diagonal
        returns CAS.

    contour adjacency series vector (CASV)
        Two digit summation of ups and downs in Contour Adjacency
        Series of a contour segment. The first digit signifies ups,
        and second, downs.

    contour interval
        Diference between two cpitch values in a cseg.

    contour interval succession
        A succession of all adjacent contour intervals in a cseg.

    contour interval array
        An array with the multiplicity of contour intervals types in a
        cseg.

    contour class vector I
        Two digit summation of the frequency of ups and
        downs. Final result is the sum of number of elements and
        contour interval multiplication.

    contour class vector II
        Two digit summation of the frequency of ups and downs. Final
        result is the sum of number of elements of a contour interval
        type.

    contour similarity
        A numeric measure for similarity between csegs with the same
        cardinality. It varies from 0 to 1, representing minimum to
        maximum similarity.

    embed contour
        A numeric measure for similarity between csegs with different
        cardinality. A embed contour has its comparison matrix embed
        in bigger contour.
