export const COLORS = {
  bg: "#000000",
  primaryText: "#FFFFFF",
  secondary: "#8E8E93",
  accentBlue: "#3B8ED0", // Paraby's default CTk accent (dark-blue theme)
  logoPurple: "#5B4B9E",
  logoGreen: "#3ACB6E",
  logoGold: "#F0C419",
  danger: "#FF6B6B",
};

export const FONT_BRAND = "Quicksand"; // Paraby's own bundled font
export const FONT_CODE = "JetBrains Mono";

// Cubic-bezier curves matching the restrained, confident motion of
// Apple/Anthropic-style product marketing — glide-to-rest, no cartoon
// bounce, elements arrive settled rather than overshoot-and-correct.
export const EASE_OUT: [number, number, number, number] = [0.16, 1, 0.3, 1];
export const EASE_IN_OUT: [number, number, number, number] = [0.65, 0, 0.35, 1];

// Minimal VS Code "Dark+"-ish token colors for our hand-tokenized code snippets.
export const TOKEN_COLORS = {
  plain: "#D4D4D4",
  keyword: "#C586C0",
  string: "#CE9178",
  number: "#B5CEA8",
  comment: "#6A9955",
  func: "#DCDCAA",
  attr: "#4FC1FF",
};
