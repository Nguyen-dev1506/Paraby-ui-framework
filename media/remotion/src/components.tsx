import React from "react";
import { Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { tokenizeLine } from "./highlight";
import { COLORS, EASE_OUT, FONT_CODE } from "./theme";

// ── Entrance motion helpers ──────────────────────────────────────────────

// The premium, restrained reveal used almost everywhere: a soft blur-in with
// a small upward drift and a confident glide-to-rest curve — no bounce, no
// overshoot. This is the Apple-keynote-style default; spring() is reserved
// for the handful of genuine "hero" moments (the logo, the outro mark).
export function useReveal(delayFrames: number, durationInFrames = 22, distance = 26) {
  const frame = useCurrentFrame();
  const local = frame - delayFrames;
  const bezier = Easing.bezier(...EASE_OUT);
  const progress = interpolate(local, [0, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: bezier,
  });
  const y = interpolate(progress, [0, 1], [distance, 0]);
  const blur = interpolate(progress, [0, 1], [8, 0]);
  const opacity = interpolate(local, [0, durationInFrames * 0.7], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return {
    transform: `translateY(${y}px)`,
    filter: `blur(${blur}px)`,
    opacity,
  } as React.CSSProperties;
}

export function useSpringPop(delayFrames = 0, durationInFrames = 22, from = 0.3) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const local = Math.max(0, frame - delayFrames);
  const progress = spring({ frame: local, fps, durationInFrames, config: { damping: 12, mass: 0.7 } });
  const scale = interpolate(progress, [0, 1], [from, 1]);
  const opacity = interpolate(local, [0, durationInFrames * 0.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return { transform: `scale(${scale})`, opacity } as React.CSSProperties;
}

export function useFadeOut(startFrame: number, durationInFrames = 16) {
  const frame = useCurrentFrame();
  const bezier = Easing.bezier(...EASE_OUT);
  const opacity = interpolate(frame, [startFrame, startFrame + durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: bezier,
  });
  const y = interpolate(frame, [startFrame, startFrame + durationInFrames], [0, -14], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return { opacity, transform: `translateY(${y}px)` } as React.CSSProperties;
}

// ── Ambient background — slow-drifting soft color blobs, the quiet depth
//    cue Anthropic/Apple product pages use instead of a flat black void ──
export const AmbientBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / 30;
  const blob = (phaseX: number, phaseY: number, speed: number, color: string, size: number) => {
    const x = 50 + Math.sin(t * speed + phaseX) * 22;
    const y = 50 + Math.cos(t * speed * 0.8 + phaseY) * 18;
    return (
      <div
        style={{
          position: "absolute",
          left: `${x}%`,
          top: `${y}%`,
          width: size,
          height: size,
          transform: "translate(-50%, -50%)",
          borderRadius: "50%",
          background: color,
          filter: "blur(90px)",
          opacity: 0.5,
        }}
      />
    );
  };
  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      {blob(0, 1.2, 0.06, `${COLORS.logoPurple}33`, 480)}
      {blob(2, 0.4, 0.05, `${COLORS.logoGreen}22`, 420)}
      {blob(4, 3, 0.045, `${COLORS.accentBlue}22`, 460)}
    </div>
  );
};

// ── macOS-style code window, hand-tokenized (no Shiki dependency) ───────
export const CodeWindow: React.FC<{
  code: string;
  fontSize?: number;
  style?: React.CSSProperties;
}> = ({ code, fontSize = 20, style }) => {
  const lines = code.split("\n");
  return (
    <div
      style={{
        background: "rgba(30, 30, 32, 0.92)",
        backdropFilter: "blur(20px)",
        borderRadius: 16,
        border: "1px solid rgba(255,255,255,0.08)",
        boxShadow: "0 30px 80px rgba(0,0,0,0.55), 0 0 0 0.5px rgba(255,255,255,0.04) inset",
        padding: "16px 26px 22px",
        display: "inline-block",
        textAlign: "left",
        ...style,
      }}
    >
      <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
        <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ff5f56" }} />
        <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ffbd2e" }} />
        <span style={{ width: 12, height: 12, borderRadius: 999, background: "#27c93f" }} />
      </div>
      <div style={{ fontFamily: FONT_CODE, fontSize, lineHeight: 1.55, whiteSpace: "pre" }}>
        {lines.map((line, i) => (
          <div key={i}>
            {tokenizeLine(line).map((tok, j) => (
              <span key={j} style={{ color: tok.color }}>
                {tok.text}
              </span>
            ))}
            {line.length === 0 ? " " : null}
          </div>
        ))}
      </div>
    </div>
  );
};

export const MonoLabel: React.FC<{ children: React.ReactNode; color?: string }> = ({
  children,
  color = COLORS.secondary,
}) => (
  <div
    style={{
      fontFamily: FONT_CODE,
      fontSize: 14,
      fontWeight: 700,
      letterSpacing: "0.08em",
      textTransform: "uppercase",
      color,
      marginBottom: 10,
      opacity: 0.9,
    }}
  >
    {children}
  </div>
);

// ── Simple vector icons (SVG), no emoji/glyph dependency ───────────────
export const Icon: React.FC<{ kind: string; size?: number }> = ({ kind, size = 56 }) => {
  const s = size;
  switch (kind) {
    case "palette":
      return (
        <svg width={s} height={s * 0.5} viewBox="0 0 90 45">
          <circle cx="20" cy="22" r="20" fill={COLORS.logoGold} />
          <circle cx="45" cy="22" r="20" fill={COLORS.logoGreen} opacity={0.95} />
          <circle cx="70" cy="22" r="20" fill={COLORS.accentBlue} opacity={0.95} />
        </svg>
      );
    case "link":
      return (
        <svg width={s} height={s * 0.6} viewBox="0 0 90 55">
          <circle cx="30" cy="27" r="22" fill="none" stroke={COLORS.accentBlue} strokeWidth="10" />
          <circle cx="60" cy="27" r="22" fill="none" stroke={COLORS.logoGreen} strokeWidth="10" />
        </svg>
      );
    case "bolt":
      return (
        <svg width={s * 0.6} height={s} viewBox="0 0 40 70">
          <polygon points="26,0 6,38 18,38 14,70 34,30 20,30" fill={COLORS.logoGold} />
        </svg>
      );
    case "image":
      return (
        <svg width={s} height={s * 0.75} viewBox="0 0 80 60">
          <rect x="2" y="2" width="76" height="56" rx="6" fill="none" stroke={COLORS.accentBlue} strokeWidth="4" />
          <circle cx="20" cy="18" r="7" fill={COLORS.logoGold} />
          <polyline points="8,50 30,28 44,42 56,26 74,50" fill="none" stroke={COLORS.logoGreen} strokeWidth="4" />
        </svg>
      );
    case "star":
      return (
        <svg width={s} height={s} viewBox="0 0 100 100">
          <polygon
            points="50,4 61,37 96,37 68,58 79,91 50,70 21,91 32,58 4,37 39,37"
            fill={COLORS.logoGold}
          />
        </svg>
      );
    case "burst":
      return (
        <svg width={s} height={s} viewBox="0 0 100 100">
          <polygon
            points="50,6 58,35 82,20 66,44 96,50 66,56 82,80 58,65 50,94 42,65 18,80 34,56 4,50 34,44 18,20 42,35"
            fill={COLORS.logoGold}
          />
          <circle cx="18" cy="18" r="5" fill={COLORS.accentBlue} />
          <circle cx="84" cy="20" r="5" fill={COLORS.logoGreen} />
          <circle cx="70" cy="86" r="5" fill={COLORS.danger} />
        </svg>
      );
    case "no":
      return (
        <svg width={s} height={s} viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="38" fill="none" stroke={COLORS.danger} strokeWidth="9" />
          <line x1="24" y1="76" x2="76" y2="24" stroke={COLORS.danger} strokeWidth="9" />
        </svg>
      );
    case "play":
      return (
        <svg width={s} height={s} viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="42" fill="none" stroke={COLORS.accentBlue} strokeWidth="7" />
          <polygon points="40,32 40,68 72,50" fill={COLORS.logoGold} />
        </svg>
      );
    case "shield":
      return (
        <svg width={s * 0.8} height={s} viewBox="0 0 70 84">
          <path
            d="M35 2 L66 14 V40 C66 62 52 76 35 82 C18 76 4 62 4 40 V14 Z"
            fill="none"
            stroke={COLORS.logoGreen}
            strokeWidth="5"
          />
          <path d="M20 42 L31 53 L52 30" fill="none" stroke={COLORS.logoGreen} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    case "gauge":
      return (
        <svg width={s} height={s * 0.7} viewBox="0 0 100 70">
          <path d="M8 62 A42 42 0 0 1 92 62" fill="none" stroke={COLORS.secondary} strokeWidth="8" />
          <path d="M8 62 A42 42 0 0 1 68 24" fill="none" stroke={COLORS.logoGold} strokeWidth="8" />
          <line x1="50" y1="62" x2="72" y2="34" stroke={COLORS.primaryText} strokeWidth="5" strokeLinecap="round" />
          <circle cx="50" cy="62" r="6" fill={COLORS.primaryText} />
        </svg>
      );
    case "eye":
      return (
        <svg width={s} height={s * 0.6} viewBox="0 0 100 60">
          <path d="M2 30 C20 4 80 4 98 30 C80 56 20 56 2 30 Z" fill="none" stroke={COLORS.accentBlue} strokeWidth="6" />
          <circle cx="50" cy="30" r="14" fill={COLORS.accentBlue} />
        </svg>
      );
    default:
      return (
        <svg width={s} height={s} viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="35" fill={COLORS.accentBlue} />
        </svg>
      );
  }
};

// ── File tree — what you actually get after `git clone` + `pip install` ──
type TreeLine = { depth: number; label: string; kind: "dir" | "file" };

export const FileTree: React.FC<{ lines: TreeLine[]; fontSize?: number }> = ({ lines, fontSize = 18 }) => (
  <div
    style={{
      background: "rgba(30, 30, 32, 0.92)",
      backdropFilter: "blur(20px)",
      borderRadius: 16,
      border: "1px solid rgba(255,255,255,0.08)",
      boxShadow: "0 30px 80px rgba(0,0,0,0.55), 0 0 0 0.5px rgba(255,255,255,0.04) inset",
      padding: "18px 30px 24px",
      display: "inline-block",
      textAlign: "left",
    }}
  >
    <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ff5f56" }} />
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#ffbd2e" }} />
      <span style={{ width: 12, height: 12, borderRadius: 999, background: "#27c93f" }} />
    </div>
    <div style={{ fontFamily: FONT_CODE, fontSize, lineHeight: 1.7 }}>
      {lines.map((l, i) => (
        <div key={i} style={{ paddingLeft: l.depth * 26 }}>
          <span style={{ color: COLORS.secondary }}>{l.depth > 0 ? "└─ " : ""}</span>
          <span style={{ color: l.kind === "dir" ? COLORS.accentBlue : "#D4D4D4", fontWeight: l.kind === "dir" ? 700 : 400 }}>
            {l.label}
          </span>
        </div>
      ))}
    </div>
  </div>
);

export const Glow: React.FC<{ color?: string; size?: number }> = ({
  color = COLORS.logoPurple,
  size = 520,
}) => (
  <div
    style={{
      position: "absolute",
      width: size,
      height: size,
      borderRadius: "50%",
      background: `radial-gradient(circle, ${COLORS.logoGold}33 0%, ${COLORS.logoGreen}22 35%, ${color}18 65%, transparent 75%)`,
      filter: "blur(2px)",
    }}
  />
);
