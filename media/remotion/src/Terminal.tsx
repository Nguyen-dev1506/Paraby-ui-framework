import React from "react";
import { useCurrentFrame } from "remotion";
import { FONT_CODE } from "./theme";

// ── Typed-text hook: reveals `text` one character at a time starting at
//    `startFrame`, `framesPerChar` frames per character. ──────────────────
export function useTypedText(text, startFrame, framesPerChar = 2) {
  const frame = useCurrentFrame();
  const local = Math.max(0, frame - startFrame);
  const charCount = Math.min(text.length, Math.floor(local / framesPerChar));
  const isDone = charCount >= text.length;
  const doneAtFrame = startFrame + text.length * framesPerChar;
  return { typed: text.slice(0, charCount), isDone, doneAtFrame };
}

// A blinking block cursor, on for ~15 frames / off for ~15 frames.
export const Cursor: React.FC<{ visible?: boolean }> = ({ visible = true }) => {
  const frame = useCurrentFrame();
  if (!visible) return null;
  const on = Math.floor(frame / 15) % 2 === 0;
  return (
    <span style={{ opacity: on ? 1 : 0, background: "#D4D4D4", marginLeft: 2 }}>
      &nbsp;
    </span>
  );
};

// ── macOS-style terminal window shell ────────────────────────────────────
export const TerminalWindow: React.FC<{
  children: React.ReactNode;
  width?: number;
  minHeight?: number;
}> = ({ children, width = 760, minHeight = 320 }) => (
  <div
    style={{
      background: "rgba(20, 20, 22, 0.94)",
      backdropFilter: "blur(20px)",
      borderRadius: 16,
      border: "1px solid rgba(255,255,255,0.08)",
      boxShadow: "0 30px 80px rgba(0,0,0,0.55)",
      width,
      minHeight,
      textAlign: "left",
      overflow: "hidden",
    }}
  >
    <div style={{ display: "flex", gap: 8, padding: "14px 18px" }}>
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ff5f56" }} />
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ffbd2e" }} />
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#27c93f" }} />
    </div>
    <div style={{ fontFamily: FONT_CODE, fontSize: 19, lineHeight: 1.7, color: "#D4D4D4", padding: "4px 24px 26px" }}>
      {children}
    </div>
  </div>
);

// A single "$ <typed command>" prompt line with blinking cursor while typing.
export const PromptLine: React.FC<{ command: string; startFrame: number; framesPerChar?: number }> = ({
  command,
  startFrame,
  framesPerChar = 2,
}) => {
  const { typed, isDone } = useTypedText(command, startFrame, framesPerChar);
  return (
    <div>
      <span style={{ color: "#3ACB6E" }}>$ </span>
      <span>{typed}</span>
      <Cursor visible={!isDone} />
    </div>
  );
};
