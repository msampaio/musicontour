\version "2.12.0"

%% retrograde example

bracketUp = {
      \override Staff.HorizontalBracket #'direction = #UP
}

bracketRevert = {
      \revert Staff.HorizontalBracket #'direction
}

music = {
  \relative c'' {
    \bracketUp
    g4\startGroup^\markup{A} b d fis\stopGroup
    \bar "||"
    g\startGroup^\markup{Retrograde (A)} ges f e\stopGroup
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
