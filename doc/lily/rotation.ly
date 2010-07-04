\version "2.12.0"

%% inversion example

bracketUp = {
      \override Staff.HorizontalBracket #'direction = #UP
}

bracketRevert = {
      \revert Staff.HorizontalBracket #'direction
}

music = {
  \relative c'' {
    \cadenzaOn
    \bracketUp
    g4\startGroup^\markup{A} a b c\stopGroup
    \bar "||"
    g4\startGroup^\markup{Rotation (A, 1)} c f d,\stopGroup
    \bar "||"
    a'4\startGroup^\markup{Rotation (A, 2)} bes g aes\stopGroup
    \bar "||"
    f'4\startGroup^\markup{Rotation (A, 3)} f, fis g\stopGroup
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
    paper-height = 2.8\cm
    paper-width = 12\cm
    indent = 0\cm
    top-margin = 0\cm
    left-margin = 0.5\cm
  }
}
