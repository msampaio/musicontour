\version "2.12.0"

%% 1 6 9 3 2 4

musicUp = \relative c' {
  \time 6/8
  \override Stem #'direction = #up
  d8^"1"[
  \once \override Stem #'transparent = ##t
  e'^"6"
  g^"9"
  \override Stem #'transparent = ##t
  a,^"3"
  f^"2"
  \override Stem #'transparent = ##f
  c']^"4"
}

musicDown = \relative c' {
  \override Stem #'direction = #down
  d8[
  \override Stem #'transparent = ##t
  e'
  g
  a,
  \override Stem #'transparent = ##f
  f
  c']
}

\score {
  \new Staff \with {
    \remove Clef_engraver
    \remove Bar_engraver
    \remove Time_signature_engraver
    \remove Staff_symbol_engraver
  }
  {
    <<
      \musicUp
      \\
      \musicDown
    >>
  }
}
\paper {
  tagline = 0
  paper-height = 3\cm
  paper-width = 4\cm
  top-margin = 0\cm
  left-margin = -1\cm
}
