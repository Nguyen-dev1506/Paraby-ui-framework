import { TOKEN_COLORS } from "./theme";

// A tiny, dependency-free Python-ish tokenizer for the handful of short code
// snippets used in this video. Not a real language server — just enough to
// make the macOS-style code windows look properly syntax-highlighted without
// pulling in a full highlighter (Shiki/Prism) for a dozen short lines.
const KEYWORDS = new Set([
  "def", "if", "else", "elif", "return", "import", "from", "as", "self",
  "None", "True", "False", "class", "for", "in", "while", "try", "except",
  "finally", "with", "pass", "lambda", "and", "or", "not", "is",
]);

const TOKEN_RE =
  /(#.*$)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+)|([^\sA-Za-z0-9_]+)/g;

export type Token = { text: string; color: string };

export function tokenizeLine(line: string): Token[] {
  const tokens: Token[] = [];
  let m: RegExpExecArray | null;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(line)) !== null) {
    if (m[1]) tokens.push({ text: m[1], color: TOKEN_COLORS.comment });
    else if (m[2]) tokens.push({ text: m[2], color: TOKEN_COLORS.string });
    else if (m[3]) tokens.push({ text: m[3], color: TOKEN_COLORS.number });
    else if (m[4]) {
      tokens.push({
        text: m[4],
        color: KEYWORDS.has(m[4]) ? TOKEN_COLORS.keyword : TOKEN_COLORS.plain,
      });
    } else if (m[5]) tokens.push({ text: m[5], color: TOKEN_COLORS.plain });
    else if (m[6]) tokens.push({ text: m[6], color: TOKEN_COLORS.plain });
    if (m[0].length === 0) TOKEN_RE.lastIndex++; // safety against zero-width matches
  }
  return tokens;
}
