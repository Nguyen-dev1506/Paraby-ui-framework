import React from "react";
import { AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { FontFaces } from "./FontFaces";
import { COLORS, FONT_BRAND, FONT_CODE } from "./theme";
import { Icon, Glow, AmbientBackground, useReveal, useSpringPop, useFadeOut } from "./components";
import { TerminalWindow, PromptLine, useTypedText, Cursor } from "./Terminal";

// Separate deliverable from ParabyIntro — its own composition, own output
// video (media/remotion/out/ParabyCLITutorial.mp4), no shared frames.
const D = {
  titleCard: 130,
  install: 260,
  help: 240,
  demo: 190,
  inspect: 220,
  lang: 340,
  introCmd: 190,
  outro: 150,
};

export const TOTAL_DURATION_IN_FRAMES =
  D.titleCard + D.install + D.help + D.demo + D.inspect + D.lang + D.introCmd + D.outro;

const Brand: React.FC<React.PropsWithChildren<{ style?: React.CSSProperties }>> = ({ children, style }) => (
  <div style={{ fontFamily: FONT_BRAND, color: COLORS.primaryText, ...style }}>{children}</div>
);

const Scene: React.FC<React.PropsWithChildren<{}>> = ({ children }) => (
  <AbsoluteFill style={{ background: COLORS.bg, alignItems: "center", justifyContent: "center" }}>
    <AmbientBackground />
    <div style={{ position: "relative", zIndex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
      {children}
    </div>
  </AbsoluteFill>
);

const OutLine: React.FC<{ children: React.ReactNode; color?: string }> = ({ children, color = "#D4D4D4" }) => (
  <div style={{ color }}>{children}</div>
);

// A single output line that reveals itself at `delay` — MUST be its own
// component (not an inline useReveal() call inside a parent's conditional
// JSX or .map()) so the hook is always called the same number of times per
// render of whichever component owns it; conditionally MOUNTING this
// component is fine, conditionally CALLING a hook inside one component's
// body is not (React error #310 — hit this exact bug building this scene).
const RevealLine: React.FC<{
  delay: number;
  duration?: number;
  distance?: number;
  color?: string;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({ delay, duration = 14, distance = 8, color = "#D4D4D4", style, children }) => {
  const reveal = useReveal(delay, duration, distance);
  return (
    <div style={{ ...reveal, ...style }}>
      <OutLine color={color}>{children}</OutLine>
    </div>
  );
};

// A second inline "answer" prompt (no "$ " prefix) — used for the numbered
// language choice and the nickname text, echoing what the user types.
const TypedAnswer: React.FC<{ label: string; answer: string; startFrame: number; framesPerChar?: number }> = ({
  label,
  answer,
  startFrame,
  framesPerChar = 3,
}) => {
  const { typed, isDone } = useTypedText(answer, startFrame, framesPerChar);
  return (
    <div>
      <span style={{ color: "#8E8E93" }}>{label}</span>
      <span>{typed}</span>
      <Cursor visible={!isDone} />
    </div>
  );
};

// ── 0a. Title card — says plainly what this video IS ─────────────────────
const TitleCardScene: React.FC = () => {
  const logoPop = useSpringPop(0, 24, 0.3);
  const title = useReveal(28, 22, 16);
  const sub = useReveal(48, 22, 14);
  const out = useFadeOut(D.titleCard - 22, 16);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
        <div style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Glow size={280} />
          <Img src={staticFile("logo.png")} style={{ width: 130, position: "relative", ...logoPop }} />
        </div>
        <Brand style={{ ...title, fontSize: 34, fontWeight: 700 }}>Paraby CLI Tutorial</Brand>
        <Brand style={{ ...sub, fontSize: 18, color: COLORS.secondary, fontWeight: 500 }}>
          Cài đặt, và toàn bộ lệnh "paraby" bạn cần biết
        </Brand>
      </div>
    </Scene>
  );
};

// ── 0b. Installation walkthrough ─────────────────────────────────────────
const InstallScene: React.FC = () => {
  const frame = useCurrentFrame();
  const out = useFadeOut(D.install - 26, 20);

  const cmd1 = "git clone https://github.com/Nguyen-dev1506/Paraby-ui-framework.git";
  const t1End = 10 + cmd1.length * 1.2 + 8;

  const cmd2 = "cd Paraby-ui-framework";
  const t2Start = t1End + 8;
  const t2End = t2Start + cmd2.length * 2 + 8;

  const cmd3 = 'pip install -e ".[dev]"';
  const t3Start = t2End + 8;
  const t3End = t3Start + cmd3.length * 2 + 10;

  const doneStart = t3End + 10;

  return (
    <Scene>
      <Brand style={{ fontSize: 28, fontWeight: 600 }}>Bước 1 — Tải về & cài đặt</Brand>
      <div style={out}>
        <TerminalWindow width={880} minHeight={260}>
          <PromptLine command={cmd1} startFrame={10} framesPerChar={1.2} />
          {frame >= t1End && (
            <div style={{ marginTop: 4 }}>
              <PromptLine command={cmd2} startFrame={t2Start} />
            </div>
          )}
          {frame >= t2End && (
            <div style={{ marginTop: 4 }}>
              <PromptLine command={cmd3} startFrame={t3Start} />
            </div>
          )}
          {frame >= doneStart && (
            <RevealLine delay={doneStart} duration={14} distance={8} color={COLORS.logoGreen}>
              Successfully installed paraby — gõ "paraby --help" để kiểm tra!
            </RevealLine>
          )}
        </TerminalWindow>
      </div>
    </Scene>
  );
};

// ── 1. paraby --help ─────────────────────────────────────────────────────
const HelpScene: React.FC = () => {
  const cmd = "paraby --help";
  const typeEnd = 10 + cmd.length * 2 + 10;
  const out = useFadeOut(D.help - 24, 18);
  const title = useReveal(0, 20, -16);

  const lines = [
    "Paraby UI Framework — Dòng lệnh CLI",
    "",
    "Cú pháp:",
    "  paraby <file.pui>           Transpile và chạy file .pui/.pb",
    "  paraby inspect <file.pui>   Xem cheat sheet",
    "  paraby demo                 Mở Showroom demo có sẵn",
    "  paraby intro                Mở video giới thiệu Paraby",
    "  paraby --lang                Chọn ngôn ngữ / đặt nickname",
    "  paraby --help, -h            Xem hướng dẫn này",
  ];

  return (
    <Scene>
      <Brand style={{ ...title, fontSize: 30, fontWeight: 600 }}>Bước 2 — Bắt đầu với "paraby --help"</Brand>
      <div style={out}>
        <TerminalWindow minHeight={360}>
          <PromptLine command={cmd} startFrame={10} />
          {lines.map((line, i) => (
            <RevealLine key={i} delay={typeEnd + i * 3}>
              {line || " "}
            </RevealLine>
          ))}
        </TerminalWindow>
      </div>
    </Scene>
  );
};

// ── 2. paraby demo ───────────────────────────────────────────────────────
const DemoScene: React.FC = () => {
  const cmd = "paraby demo";
  const typeEnd = 10 + cmd.length * 2 + 8;
  const out = useFadeOut(D.demo - 22, 16);
  const iconPop = useSpringPop(typeEnd + 14, 22, 0.3);
  const capIn = useReveal(typeEnd + 8, 18, 10);

  return (
    <Scene>
      <div style={out}>
        <TerminalWindow minHeight={140}>
          <PromptLine command={cmd} startFrame={10} />
          <div style={capIn}>
            <OutLine color={COLORS.logoGreen}>Đang mở Showroom demo...</OutLine>
          </div>
        </TerminalWindow>
      </div>
      <div style={{ ...iconPop, display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
        <Icon kind="burst" size={64} />
        <Brand style={{ fontSize: 16, color: COLORS.secondary, fontWeight: 500 }}>
          Cả bảng buffet widget, không cần viết file nào
        </Brand>
      </div>
    </Scene>
  );
};

// ── 3. paraby inspect app.pui ────────────────────────────────────────────
const InspectScene: React.FC = () => {
  const cmd = "paraby inspect app.pui";
  const typeEnd = 10 + cmd.length * 2 + 8;
  const out = useFadeOut(D.inspect - 22, 16);

  const lines = [
    "[1] DANH SÁCH WIDGET:",
    "  - my_button (btn)",
    "  - my_label (label)",
    "",
    "[2] DATA BINDING (thời gian thực):",
    "  - user_name (tự cập nhật, khỏi .get())",
  ];

  return (
    <Scene>
      <div style={out}>
        <TerminalWindow minHeight={280}>
          <PromptLine command={cmd} startFrame={10} />
          {lines.map((line, i) => (
            <RevealLine key={i} delay={typeEnd + i * 4}>
              {line || " "}
            </RevealLine>
          ))}
        </TerminalWindow>
      </div>
    </Scene>
  );
};

// ── 4. paraby --lang — the star: language pick + nickname demo ──────────
const LangScene: React.FC = () => {
  const frame = useCurrentFrame();
  const cmd = "paraby --lang";
  const t1End = 10 + cmd.length * 2 + 10; // after "$ paraby --lang" finishes typing

  const listLines = [
    "1. English (en)",
    "2. Tiếng Việt (vi)",
    "3. Tiếng Việt (cà khịa) (vi_cakhia)",
    "4. Tiếng Việt (vui nhộn) (vi_vui)",
  ];
  const listEnd = t1End + listLines.length * 5 + 10;

  const choiceStart = listEnd + 6;
  const choiceEnd = choiceStart + 1 * 3 + 10; // typing "4"

  const savedStart = choiceEnd + 8;
  const savedEnd = savedStart + 14;

  const nickPromptStart = savedEnd + 10;
  const nickAnswer = "Sư Phụ";
  const nickEnd = nickPromptStart + nickAnswer.length * 4 + 12;

  const greetStart = nickEnd + 10;

  const out = useFadeOut(D.lang - 26, 20);

  return (
    <Scene>
      <div style={out}>
        <TerminalWindow width={800} minHeight={420}>
          <PromptLine command={cmd} startFrame={10} />

          {listLines.map((line, i) => (
            <RevealLine key={i} delay={t1End + i * 5} duration={10} distance={6} color={i === 3 ? COLORS.logoGold : "#D4D4D4"}>
              {line}
            </RevealLine>
          ))}

          {frame >= listEnd && (
            <div style={{ marginTop: 10 }}>
              <TypedAnswer label="Nhập số (mặc định: 1): " answer="4" startFrame={choiceStart} framesPerChar={6} />
            </div>
          )}

          {frame >= choiceEnd && (
            <RevealLine delay={savedStart} duration={12} distance={8} color={COLORS.logoGreen}>
              🎉 Yaaay, lưu ngôn ngữ 'Tiếng Việt (vui nhộn)' thành công rồi đó bạn!
            </RevealLine>
          )}

          {frame >= savedEnd && (
            <div style={{ marginTop: 10 }}>
              <TypedAnswer
                label="🎤 Paraby gọi bạn là gì? (Enter để bỏ qua): "
                answer={nickAnswer}
                startFrame={nickPromptStart}
                framesPerChar={4}
              />
            </div>
          )}

          {frame >= nickEnd && (
            <RevealLine delay={greetStart} duration={14} distance={10} color={COLORS.logoGold}>
              🎈 Chào Sư Phụ! Từ giờ Paraby sẽ gọi bạn vậy đó.
            </RevealLine>
          )}
        </TerminalWindow>
      </div>
    </Scene>
  );
};

// ── 5. paraby intro ───────────────────────────────────────────────────────
const IntroCmdScene: React.FC = () => {
  const cmd = "paraby intro";
  const typeEnd = 10 + cmd.length * 2 + 8;
  const out = useFadeOut(D.introCmd - 22, 16);
  const iconPop = useSpringPop(typeEnd + 14, 22, 0.3);
  const capIn = useReveal(typeEnd + 40, 20, 14);

  return (
    <Scene>
      <div style={out}>
        <TerminalWindow minHeight={140}>
          <PromptLine command={cmd} startFrame={10} />
          <div style={useReveal(typeEnd + 8, 14, 8)}>
            <OutLine color={COLORS.logoGreen}>🎬 Đang mở video intro — bấm fullscreen nha!</OutLine>
          </div>
        </TerminalWindow>
      </div>
      <div style={{ ...iconPop, display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
        <Icon kind="play" size={64} />
      </div>
      <Brand style={{ ...capIn, fontSize: 18, color: COLORS.secondary, fontWeight: 500, textAlign: "center", maxWidth: 560 }}>
        Lệnh này mở riêng video giới thiệu Paraby (khác video bạn đang xem) — bấm fullscreen để xem trọn vẹn! 🎥
      </Brand>
    </Scene>
  );
};

// ── 6. Outro ───────────────────────────────────────────────────────────────
const OutroScene: React.FC = () => {
  const pop = useSpringPop(0, 24, 0.5);
  const sub = useReveal(24, 22, 16);
  const out = useFadeOut(D.outro - 24, 20);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, ...pop }}>
          <Img src={staticFile("logo.png")} style={{ width: 60 }} />
          <Brand style={{ fontSize: 36, fontWeight: 700 }}>Paraby UI Framework</Brand>
        </div>
        <div style={{ ...sub, fontFamily: FONT_CODE, fontSize: 17, fontWeight: 700, color: COLORS.secondary, marginTop: 16 }}>
          paraby --help để bắt đầu
        </div>
      </div>
    </Scene>
  );
};

// ── Assembly ──────────────────────────────────────────────────────────────
export const CLITutorial: React.FC = () => {
  let cursor = 0;
  const seq = (dur: number) => {
    const from = cursor;
    cursor += dur;
    return from;
  };

  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      <FontFaces />
      <Sequence from={seq(D.titleCard)} durationInFrames={D.titleCard}>
        <TitleCardScene />
      </Sequence>
      <Sequence from={seq(D.install)} durationInFrames={D.install}>
        <InstallScene />
      </Sequence>
      <Sequence from={seq(D.help)} durationInFrames={D.help}>
        <HelpScene />
      </Sequence>
      <Sequence from={seq(D.demo)} durationInFrames={D.demo}>
        <DemoScene />
      </Sequence>
      <Sequence from={seq(D.inspect)} durationInFrames={D.inspect}>
        <InspectScene />
      </Sequence>
      <Sequence from={seq(D.lang)} durationInFrames={D.lang}>
        <LangScene />
      </Sequence>
      <Sequence from={seq(D.introCmd)} durationInFrames={D.introCmd}>
        <IntroCmdScene />
      </Sequence>
      <Sequence from={seq(D.outro)} durationInFrames={D.outro}>
        <OutroScene />
      </Sequence>
    </AbsoluteFill>
  );
};
