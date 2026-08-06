import React from "react";
import { staticFile } from "remotion";

// @font-face rules injected as a runtime <style> tag (using staticFile()
// for the URLs) instead of a plain .css file — webpack's css-loader tries
// to resolve url(...) in .css files as module imports, which breaks on a
// root-relative "/fonts/..." path. This sidesteps that entirely.
export const FontFaces: React.FC = () => (
  <style>{`
    @font-face {
      font-family: 'Quicksand';
      src: url('${staticFile("fonts/Quicksand.ttf")}') format('truetype');
      font-weight: 300 700;
    }
    @font-face {
      font-family: 'JetBrains Mono';
      src: url('${staticFile("fonts/JetBrainsMono-Regular.ttf")}') format('truetype');
      font-weight: 400;
    }
    @font-face {
      font-family: 'JetBrains Mono';
      src: url('${staticFile("fonts/JetBrainsMono-Bold.ttf")}') format('truetype');
      font-weight: 700;
    }
  `}</style>
);
