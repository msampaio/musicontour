\version "2.12.0"

%% inversion example

bracketUp = {
      \override Staff.HorizontalBracket #'direction = #UP
}

bracketRevert = {
      \revert Staff.HorizontalBracket #'direction
}

music = {
  \relative c''' {
    \cadenzaOn
    \bracketUp
    g4\startGroup^\markup{A} ees f b, cis a\stopGroup
    \bar "||"
    gis\startGroup^\markup{Inversion (A)} b ais e' c g'\stopGroup
    \bar "|."
  }
}

\book {
  \score {
    \new Staff {
      \music
    }
    \layout {
      \context {
        %% Enables startGroup
        \Voice
        \consists "Horizontal_bracket_engraver"
      }
    }
  }
  \paper {
    tagline = 0
    paper-height = 2.5\cm
    paper-width = 7.5\cm
    top-margin = 0\cm
    left-margin = -1\cm
  }
}
