\version "2.12.0"

%% 1 6 9 3 2 4

music = \relative c' {
  \time 6/8
  \override Stem #'transparent = ##t
  \override Beam #'transparent = ##t
  d8^"1"
  e'^"6"
  g^"9"
  a,^"3"
  f^"2"
  c'^"4"
}

\score {
  \new Staff \with {
    \remove Clef_engraver
    \remove Bar_engraver
    \remove Time_signature_engraver
    \remove Staff_symbol_engraver
  }
  {
    \music
  }
}
\paper {
  tagline = 0
  paper-height = 3\cm
  paper-width = 4\cm
  top-margin = 0\cm
  left-margin = -1\cm
}
