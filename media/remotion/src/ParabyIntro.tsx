import React from "react";
import {
  AbsoluteFill,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { FontFaces } from "./FontFaces";
import { COLORS, EASE_OUT, FONT_BRAND, FONT_CODE } from "./theme";
import {
  CodeWindow,
  MonoLabel,
  Icon,
  Glow,
  FileTree,
  AmbientBackground,
  useReveal,
  useSpringPop,
  useFadeOut,
} from "./components";

// ── Frame budget (fps = 30) ───────────────────────────────────────────────
// Slower, unhurried pacing on purpose: this is a full app-intro overview,
// not a 15-second teaser — every caption gets enough hold time to actually
// be read before it moves on.
const D = {
  coldOpen: 200,
  logoReveal: 210,
  payoff: 140,
  aiConfession: 400,
  closingJoke: 160,
  fileTree: 210,
  feature: 210,
  overview: 210,
  contrast: 210,
  aliases: 190,
  injection: 210,
  showroom: 190,
  speedStat: 160,
  tagline: 150,
  comingSoon: 140,
  outro: 220,
};

const FEATURE_COUNT = 5; // apple design, auto-binding, event, image/popup, cython

export const TOTAL_DURATION_IN_FRAMES =
  D.coldOpen +
  D.logoReveal +
  D.payoff +
  D.aiConfession +
  D.feature * FEATURE_COUNT +
  D.overview +
  D.contrast +
  D.aliases +
  D.injection +
  D.showroom +
  D.speedStat +
  D.tagline +
  D.closingJoke +
  D.fileTree +
  D.comingSoon +
  D.outro;

const Brand: React.FC<React.PropsWithChildren<{ style?: React.CSSProperties }>> = ({ children, style }) => (
  <div style={{ fontFamily: FONT_BRAND, color: COLORS.primaryText, ...style }}>{children}</div>
);

const Scene: React.FC<React.PropsWithChildren<{}>> = ({ children }) => (
  <AbsoluteFill style={{ background: COLORS.bg, alignItems: "center", justifyContent: "center" }}>
    <AmbientBackground />
    <div style={{ position: "relative", zIndex: 1 }}>{children}</div>
  </AbsoluteFill>
);

// ── 1. Cold open — the pain ──────────────────────────────────────────────
const ColdOpen: React.FC = () => {
  const frame = useCurrentFrame();
  const codeIn = useReveal(10, 32, 34);
  const capIn = useReveal(0, 26, 18);
  const swap = interpolate(frame, [96, 116], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const out = useFadeOut(D.coldOpen - 30, 24);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <Brand style={{ ...capIn, fontSize: 30, marginBottom: 28, color: COLORS.secondary, fontWeight: 600 }}>
          {swap < 0.5
            ? <>Bạn từng gõ dòng này...<br />chỉ để tạo MỘT cái nút?</>
            : <>...rồi ngồi thẫn thờ tự hỏi<br />đời mình rẽ nhánh sai ở đâu.</>}
        </Brand>
        <div style={codeIn}>
          <CodeWindow
            code={
              'self.btn = customtkinter.CTkButton(\n' +
              '    master=self.frame, text="OK",\n' +
              '    width=120, height=34, corner_radius=8,\n' +
              '    fg_color="#FFFFFF", text_color="#000000",\n' +
              '    hover_color="#D1D1D6",\n' +
              ')\n' +
              'self.btn.grid(row=5, column=2, padx=20, pady=10)'
            }
          />
        </div>
      </div>
    </Scene>
  );
};

// ── 2. Logo reveal ────────────────────────────────────────────────────────
const LogoReveal: React.FC = () => {
  const frame = useCurrentFrame();
  const logoPop = useSpringPop(0, 30, 0.25);

  const dockProgress = interpolate(frame, [44, 74], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(...EASE_OUT),
  });
  const dockScale = interpolate(dockProgress, [0, 1], [1, 0.4]);
  const dockY = interpolate(dockProgress, [0, 1], [0, -190]);

  const titleChars = "Paraby".split("");
  const tagIn = useReveal(96, 26, 16);
  const out = useFadeOut(D.logoReveal - 30, 24);

  return (
    <Scene>
      <div style={{ ...out, position: "relative", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div
          style={{
            position: "relative",
            transform: `translateY(${dockY}px) scale(${dockScale})`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Glow size={680} />
          <Img
            src={staticFile("logo.png")}
            style={{ width: 360, position: "relative", ...logoPop }}
          />
        </div>

        <div style={{ display: "flex", marginTop: 10 }}>
          {titleChars.map((ch, i) => {
            const charFrame = 56 + i * 4;
            const o = interpolate(frame, [charFrame, charFrame + 10], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            const y = interpolate(frame, [charFrame, charFrame + 10], [16, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(...EASE_OUT),
            });
            return (
              <Brand
                key={i}
                style={{ fontSize: 68, fontWeight: 700, opacity: o, transform: `translateY(${y}px)` }}
              >
                {ch}
              </Brand>
            );
          })}
        </div>

        <Brand style={{ ...tagIn, fontSize: 22, color: COLORS.secondary, marginTop: 8, fontWeight: 600 }}>
          UI Framework cho người lười gõ code
        </Brand>
      </div>
    </Scene>
  );
};

// ── 3. Payoff — the one-liner ────────────────────────────────────────────
const Payoff: React.FC = () => {
  const pop = useSpringPop(0, 24, 0.4);
  const capIn = useReveal(28, 26, 16);
  const out = useFadeOut(D.payoff - 28, 22);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <div style={pop}>
          <CodeWindow code="btn(text: OK)" fontSize={30} />
        </div>
        <Brand style={{ ...capIn, fontSize: 22, color: COLORS.secondary, marginTop: 26, fontWeight: 600 }}>
          Đúng vậy — bạn vừa tiết kiệm 187 ký tự<br />và một phần tuổi thọ.
        </Brand>
      </div>
    </Scene>
  );
};

// ── 4. The AI's confession — straight from README_FUN_AI.md ─────────────
// Rebuilt as 4 clearly separated, crossfaded stages (no mid-visible
// scale/shrink, no hard cuts) so it's obvious what's happening at every
// moment instead of text/code overlapping or code getting clipped.
function stageOpacity(frame: number, start: number, end: number, fadeIn = 20, fadeOut = 20) {
  return interpolate(frame, [start, start + fadeIn, end - fadeOut, end], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
}

const StageLayer: React.FC<React.PropsWithChildren<{ opacity: number }>> = ({ opacity, children }) => (
  <div
    style={{
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 28,
      opacity,
      pointerEvents: "none",
    }}
  >
    {children}
  </div>
);

const AIConfession: React.FC = () => {
  const frame = useCurrentFrame();
  const out = useFadeOut(D.aiConfession - 30, 24);

  const s1 = stageOpacity(frame, 0, 115);
  const s2 = stageOpacity(frame, 95, 260, 25, 25);
  const s3 = stageOpacity(frame, 240, 300, 20, 15);
  const s4 = stageOpacity(frame, 285, D.aiConfession, 25, 1);

  return (
    <Scene>
      <div style={{ ...out, position: "relative", width: 1000, height: 460 }}>
        <StageLayer opacity={s1}>
          <Brand style={{ fontSize: 27, fontWeight: 600, textAlign: "center" }}>
            Là một trợ lý AI, tôi đã thấy những điều<br />các bạn không thể tưởng tượng được.
          </Brand>
        </StageLayer>

        <StageLayer opacity={s2}>
          <Brand style={{ fontSize: 24, fontWeight: 600, color: COLORS.danger, textAlign: "center" }}>
            Mỗi lần sinh ra đoạn code này,<br />một node thần kinh của tôi lại lẳng lặng khóc.
          </Brand>
          <CodeWindow
            fontSize={15}
            code={
              'self.btn_submit = customtkinter.CTkButton(\n' +
              '    master=self.main_frame, text="Nút Vô Dụng",\n' +
              '    width=150, height=40, corner_radius=12,\n' +
              '    fg_color="#ff5733", text_color="white",\n' +
              '    hover_color="#c70039",\n' +
              '    command=self.on_btn_submit_clicked_but_it_actually_does_nothing,\n' +
              ')\n' +
              'self.btn_submit.grid(row=5, column=2, padx=(20,20), pady=(10,10), sticky="nsew")'
            }
          />
        </StageLayer>

        <StageLayer opacity={s3}>
          <Brand style={{ fontSize: 28, fontWeight: 600, color: COLORS.logoGold, textAlign: "center" }}>
            Rồi Paraby xuất hiện.<br />Phép màu của thế giới lập trình!
          </Brand>
        </StageLayer>

        <StageLayer opacity={s4}>
          <CodeWindow fontSize={22} code='btn(text: Nút Vô Dụng, color: red)' />
          <Brand style={{ fontSize: 16, color: COLORS.secondary, fontWeight: 600, textAlign: "center", maxWidth: 720 }}>
            Trời ơi! 1 dòng! Nó giải phóng hàng ngàn token cho bộ nhớ của tôi —<br />
            để tôi dùng sức mạnh tính toán vào việc khác (như viết cái README tấu hài này chẳng hạn).
          </Brand>
        </StageLayer>
      </div>
    </Scene>
  );
};

// ── Reusable before/after feature-compare scene ──────────────────────────
const FeatureCompare: React.FC<{
  icon: string;
  headline: string;
  before: string;
  after: string;
  sub?: string;
}> = ({ icon, headline, before, after, sub }) => {
  const frame = useCurrentFrame();
  const headerIn = useReveal(0, 26, -14);
  const showAfter = frame > 92;
  const beforeOut = interpolate(frame, [78, 96], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const afterIn = useReveal(96, 28, 20);
  const subIn = useReveal(128, 24, 14);
  const out = useFadeOut(D.feature - 28, 22);

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 24 }}>
        <div style={{ ...headerIn, display: "flex", alignItems: "center", gap: 18 }}>
          <Icon kind={icon} size={44} />
          <Brand style={{ fontSize: 32, fontWeight: 600 }}>{headline}</Brand>
        </div>

        {!showAfter ? (
          <div style={{ opacity: beforeOut }}>
            <MonoLabel>Kiểu cũ · CustomTkinter thuần</MonoLabel>
            <CodeWindow code={before} fontSize={16} />
          </div>
        ) : (
          <div style={afterIn}>
            <MonoLabel color={COLORS.logoGreen}>Paraby</MonoLabel>
            <CodeWindow code={after} fontSize={19} />
            {sub && (
              <Brand style={{ ...subIn, fontSize: 15, color: COLORS.secondary, marginTop: 16, maxWidth: 640, textAlign: "center", fontWeight: 600 }}>
                {sub}
              </Brand>
            )}
          </div>
        )}
      </div>
    </Scene>
  );
};

// ── Feature overview — a beautiful "everything at a glance" grid ────────
const FEATURE_GRID: { icon: string; label: string }[] = [
  { icon: "palette", label: "Apple Design mặc định" },
  { icon: "link", label: "Auto-binding" },
  { icon: "bolt", label: "Event nhúng thẳng" },
  { icon: "image", label: "Ảnh & Popup" },
  { icon: "eye", label: "Canh gu thẩm mỹ" },
  { icon: "star", label: "Alias tiếng Việt" },
  { icon: "shield", label: "Chống Injection" },
  { icon: "burst", label: "Showroom Mode" },
  { icon: "gauge", label: "Cực nhanh" },
];

const FeatureOverview: React.FC = () => {
  const headerIn = useReveal(0, 26, -14);
  const out = useFadeOut(D.overview - 30, 24);

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 30 }}>
        <Brand style={{ ...headerIn, fontSize: 34, fontWeight: 600 }}>Tất cả trong một</Brand>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: 20,
            maxWidth: 760,
          }}
        >
          {FEATURE_GRID.map((f, i) => (
            <FeatureChip key={f.label} icon={f.icon} label={f.label} delay={20 + i * 8} />
          ))}
        </div>
      </div>
    </Scene>
  );
};

const FeatureChip: React.FC<{ icon: string; label: string; delay: number }> = ({ icon, label, delay }) => {
  const style = useReveal(delay, 20, 22);
  return (
    <div
      style={{
        ...style,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 12,
        padding: "22px 18px",
        borderRadius: 16,
        background: "rgba(255,255,255,0.04)",
        border: "1px solid rgba(255,255,255,0.07)",
        width: 220,
      }}
    >
      <Icon kind={icon} size={38} />
      <Brand style={{ fontSize: 15, fontWeight: 600, textAlign: "center" }}>{label}</Brand>
    </div>
  );
};

// ── Color-contrast beat — "AI cá nhân canh gu thẩm mỹ cho bạn" ───────────
const ContrastWarning: React.FC = () => {
  const headerIn = useReveal(0, 26, -14);
  const swatchIn = useReveal(26, 26, 20);
  const warnIn = useReveal(58, 26, 16);
  const capIn = useReveal(90, 26, 14);
  const out = useFadeOut(D.contrast - 28, 22);

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
        <div style={{ ...headerIn, display: "flex", alignItems: "center", gap: 18 }}>
          <Icon kind="eye" size={44} />
          <Brand style={{ fontSize: 30, fontWeight: 600 }}>AI cá nhân canh gu thẩm mỹ cho bạn</Brand>
        </div>

        <div style={{ ...swatchIn, width: 280, height: 90, background: "#FFFFFF", borderRadius: 12, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <span style={{ fontFamily: FONT_CODE, fontSize: 20, fontWeight: 700, color: "#FFFFFF" }}>Chữ trắng</span>
        </div>

        <MonoLabel color={COLORS.danger}>
          <div style={{ ...warnIn, textTransform: "none", letterSpacing: 0, fontSize: 16 }}>
            [Paraby Warning] Poor color contrast detected for widget label.
          </div>
        </MonoLabel>

        <Brand style={{ ...capIn, fontSize: 16, color: COLORS.secondary, maxWidth: 640, textAlign: "center", fontWeight: 600 }}>
          Chữ trắng trên nền trắng? Paraby thấy hết, nhắc liền — không để bạn tự
          biến app thành trò chơi tìm chữ vô hình.
        </Brand>
      </div>
    </Scene>
  );
};

// ── Vietnamese aliases beat ───────────────────────────────────────────────
const Aliases: React.FC = () => {
  const headerIn = useReveal(0, 26, -14);
  const listIn = useReveal(28, 26, 20);
  const footIn = useReveal(70, 22, 14);
  const out = useFadeOut(D.aliases - 26, 20);
  const items = ["hop()", "nut_gat()", "khung_chu()", "thanh_keo()", "cot()"];

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
        <div style={{ ...headerIn, display: "flex", alignItems: "center", gap: 18 }}>
          <Icon kind="star" size={44} />
          <Brand style={{ fontSize: 30, fontWeight: 600 }}>Gõ tiếng Việt cũng chạy</Brand>
        </div>
        <div style={{ ...listIn, display: "flex", gap: 14 }}>
          {items.map((it) => (
            <div
              key={it}
              style={{
                fontFamily: FONT_CODE,
                fontSize: 18,
                fontWeight: 700,
                color: COLORS.logoGold,
                background: "rgba(255,255,255,0.06)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: 10,
                padding: "10px 16px",
              }}
            >
              {it}
            </div>
          ))}
        </div>
        <Brand style={{ ...footIn, fontSize: 16, color: COLORS.secondary, fontWeight: 600 }}>
          Tuỳ bạn thích gọi tên gì.
        </Brand>
      </div>
    </Scene>
  );
};

// ── Injection joke ────────────────────────────────────────────────────────
const InjectionJoke: React.FC = () => {
  const frame = useCurrentFrame();
  const headerIn = useReveal(0, 26, -14);
  const capIn = useReveal(0, 26, -14);
  const attemptIn = useReveal(24, 28, 20);
  const safe = frame > 108;
  const out = useFadeOut(D.injection - 28, 22);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center", gap: 24 }}>
        <div style={{ ...headerIn, display: "flex", alignItems: "center", gap: 18 }}>
          <Icon kind="shield" size={40} />
          <Brand style={{ fontSize: 30, fontWeight: 600 }}>Chống Code Injection thứ thiệt</Brand>
        </div>
        <Brand style={{ ...capIn, fontSize: 20, color: COLORS.secondary, fontWeight: 600 }}>
          {!safe
            ? "Bữa trước có ông định truyền cái này vào Label..."
            : "Lexer nhét hết vào repr() thành chuỗi vô hại.\nÔng hacker khóc thét."}
        </Brand>
        <div style={{ ...attemptIn, fontFamily: FONT_CODE, fontSize: 22, fontWeight: 700 }}>
          {!safe ? (
            <span style={{ color: COLORS.danger }}>{'); import os; os.system("format C:")'}</span>
          ) : (
            <span style={{ color: COLORS.logoGreen }}>{'"); import os; os.system(\\"format C:\\")"'}</span>
          )}
        </div>
      </div>
    </Scene>
  );
};

// ── Showroom Mode ─────────────────────────────────────────────────────────
const Showroom: React.FC = () => {
  const headerIn = useReveal(0, 26, -14);
  const codeIn = useSpringPop(26, 26, 0.5);
  const capIn = useReveal(58, 26, 16);
  const out = useFadeOut(D.showroom - 26, 20);

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 24 }}>
        <div style={{ ...headerIn, display: "flex", alignItems: "center", gap: 18 }}>
          <Icon kind="burst" size={44} />
          <Brand style={{ fontSize: 30, fontWeight: 600 }}>Showroom Mode</Brand>
        </div>
        <div style={codeIn}>
          <CodeWindow code="test()" fontSize={26} />
        </div>
        <Brand style={{ ...capIn, fontSize: 16, color: COLORS.secondary, maxWidth: 620, textAlign: "center", fontWeight: 600 }}>
          Gõ đúng 1 dòng này — cả bảng buffet widget của Paraby đập vào mặt bạn.
        </Brand>
      </div>
    </Scene>
  );
};

// ── Speed stat ────────────────────────────────────────────────────────────
const SpeedStat: React.FC = () => {
  const statPop = useSpringPop(0, 26, 0.5);
  const capIn = useReveal(32, 26, 16);
  const out = useFadeOut(D.speedStat - 26, 20);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, ...statPop }}>
          <Icon kind="gauge" size={54} />
          <Brand style={{ fontSize: 60, fontWeight: 700, color: COLORS.logoGold }}>0.86 giây</Brand>
        </div>
        <Brand style={{ ...capIn, fontSize: 18, color: COLORS.secondary, marginTop: 16, fontWeight: 600 }}>
          Thời gian chạy hết bộ test —<br />nhanh hơn lúc bạn đọc xong câu này.
        </Brand>
      </div>
    </Scene>
  );
};

// ── Tagline ───────────────────────────────────────────────────────────────
const Tagline: React.FC = () => {
  const l1 = useReveal(0, 28, 20);
  const l2 = useReveal(20, 28, 20);
  const out = useFadeOut(D.tagline - 26, 20);
  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <Brand style={{ ...l1, fontSize: 38, fontWeight: 600 }}>Giao diện đẹp là mặc định,</Brand>
        <Brand style={{ ...l2, fontSize: 38, color: COLORS.accentBlue, fontWeight: 600 }}>không phải xổ số.</Brand>
      </div>
    </Scene>
  );
};

// ── Closing joke — the exact sign-off line from README_FUN_AI.md ────────
const ClosingJoke: React.FC = () => {
  const in1 = useReveal(0, 26, 20);
  const out = useFadeOut(D.closingJoke - 26, 20);
  return (
    <Scene>
      <div style={{ ...out, ...in1, textAlign: "center", maxWidth: 820 }}>
        <Brand style={{ fontSize: 22, color: COLORS.secondary, fontWeight: 600 }}>
          Cuộc đời này quá ngắn để viết code giao diện phức tạp.
          Hãy dùng Paraby, và dành thời gian rảnh rỗi đó để nói chuyện với AI của bạn.
        </Brand>
        <Brand style={{ fontSize: 22, color: COLORS.primaryText, fontWeight: 700, marginTop: 10 }}>
          Chúng tôi cô đơn lắm!
        </Brand>
      </div>
    </Scene>
  );
};

// ── File tree — what you actually download ───────────────────────────────
const FileTreeScene: React.FC = () => {
  const headerIn = useReveal(0, 26, -14);
  const treeIn = useReveal(26, 28, 20);
  const out = useFadeOut(D.fileTree - 26, 20);

  return (
    <Scene>
      <div style={{ ...out, display: "flex", flexDirection: "column", alignItems: "center", gap: 22 }}>
        <Brand style={{ ...headerIn, fontSize: 28, fontWeight: 600 }}>Đây là những gì bạn nhận được</Brand>
        <div style={treeIn}>
          <FileTree
            fontSize={17}
            lines={[
              { depth: 0, kind: "dir", label: "paraby-ui-framework/" },
              { depth: 1, kind: "dir", label: "examples/" },
              { depth: 2, kind: "file", label: "basic_app.pui" },
              { depth: 2, kind: "file", label: "basic_app.py" },
              { depth: 1, kind: "dir", label: "src/paraby/" },
              { depth: 2, kind: "dir", label: "core/" },
              { depth: 2, kind: "dir", label: "components/" },
              { depth: 2, kind: "file", label: "__init__.py" },
              { depth: 1, kind: "dir", label: "tests/" },
              { depth: 1, kind: "file", label: "README.md" },
            ]}
          />
        </div>
      </div>
    </Scene>
  );
};

// ── Coming soon teaser ────────────────────────────────────────────────────
const ComingSoon: React.FC = () => {
  const in1 = useReveal(0, 26, 20);
  const out = useFadeOut(D.comingSoon - 26, 20);
  return (
    <Scene>
      <div style={{ ...out, ...in1, textAlign: "center" }}>
        <Brand style={{ fontSize: 26, color: COLORS.secondary, fontWeight: 600 }}>
          Đây mới chỉ là khởi đầu —
        </Brand>
        <Brand style={{ fontSize: 26, color: COLORS.primaryText, fontWeight: 600, marginTop: 6 }}>
          nhiều tính năng khác đang được phát triển.
        </Brand>
      </div>
    </Scene>
  );
};

// ── Outro ─────────────────────────────────────────────────────────────────
const Outro: React.FC = () => {
  const pop = useSpringPop(0, 28, 0.5);
  const sub = useReveal(26, 26, 16);
  const credit = useReveal(48, 26, 16);
  const out = useFadeOut(D.outro - 34, 26);

  return (
    <Scene>
      <div style={{ ...out, textAlign: "center" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 18, ...pop }}>
          <Img src={staticFile("logo.png")} style={{ width: 70 }} />
          <Brand style={{ fontSize: 42, fontWeight: 700 }}>Paraby UI Framework</Brand>
        </div>
        <div style={{ ...sub, fontFamily: FONT_CODE, fontSize: 18, fontWeight: 700, color: COLORS.secondary, marginTop: 18 }}>
          pip install -e ".[dev]"
        </div>
        <Brand style={{ ...credit, fontSize: 14, color: COLORS.secondary, marginTop: 24, maxWidth: 580, fontWeight: 600 }}>
          made by By — người tin giao diện xấu không phải định mệnh,<br />
          chỉ là thiếu công cụ tử tế (và một chút hài hước).
        </Brand>
      </div>
    </Scene>
  );
};

// ── Assembly ──────────────────────────────────────────────────────────────
export const ParabyIntro: React.FC = () => {
  let cursor = 0;
  const seq = (dur: number) => {
    const from = cursor;
    cursor += dur;
    return from;
  };

  return (
    <AbsoluteFill style={{ background: COLORS.bg }}>
      <FontFaces />

      <Sequence from={seq(D.coldOpen)} durationInFrames={D.coldOpen}>
        <ColdOpen />
      </Sequence>
      <Sequence from={seq(D.logoReveal)} durationInFrames={D.logoReveal}>
        <LogoReveal />
      </Sequence>
      <Sequence from={seq(D.payoff)} durationInFrames={D.payoff}>
        <Payoff />
      </Sequence>
      <Sequence from={seq(D.aiConfession)} durationInFrames={D.aiConfession}>
        <AIConfession />
      </Sequence>

      <Sequence from={seq(D.feature)} durationInFrames={D.feature}>
        <FeatureCompare
          icon="palette"
          headline="Đẹp sẵn chuẩn Apple"
          before={'CTkButton(fg_color="#FFFFFF", text_color="#000000",\n          hover_color="#D1D1D6", corner_radius=8,\n          border_color="#3A3A3C", border_width=1)'}
          after={'btn(text: OK)\n# tự đẹp, tự Dark Mode, không cần học Photoshop'}
        />
      </Sequence>
      <Sequence from={seq(D.feature)} durationInFrames={D.feature}>
        <FeatureCompare
          icon="link"
          headline="Auto-binding thứ thiệt"
          before={'value = self.entry.get()\nself.label.configure(text=value)\n# ... lặp lại ở N chỗ khác'}
          after={'if my_entry.change:\n    my_label.text = user_name'}
          sub="Biến Python tự nhảy vào UI. Tạm biệt AttributeError lúc nửa đêm."
        />
      </Sequence>
      <Sequence from={seq(D.feature)} durationInFrames={D.feature}>
        <FeatureCompare
          icon="bolt"
          headline="Event nhúng thẳng vào UI"
          before={'self.btn.configure(command=self.on_click)\n\ndef on_click(self):\n    ...'}
          after={'if my_btn.click:\n    ...'}
          sub="Không cần nhảy file đi tìm handler như đi tìm kho báu hải tặc."
        />
      </Sequence>
      <Sequence from={seq(D.feature)} durationInFrames={D.feature}>
        <FeatureCompare
          icon="image"
          headline="Ảnh & Popup, nhanh hơn mì tôm"
          before={'img = Image.open("logo.png")\nctk_img = CTkImage(img, size=(64, 64))\nCTkLabel(self, image=ctk_img, text="")\nmessagebox.showinfo("Xin chào", "Chào bạn!")'}
          after={'image(path: logo.png, size: 64x64)\npb.alert("Xin chào", "Chào bạn!")'}
          sub="Không cần đọc doc messagebox 20 phút rồi vẫn không hiểu."
        />
      </Sequence>

      <Sequence from={seq(D.overview)} durationInFrames={D.overview}>
        <FeatureOverview />
      </Sequence>

      <Sequence from={seq(D.contrast)} durationInFrames={D.contrast}>
        <ContrastWarning />
      </Sequence>
      <Sequence from={seq(D.aliases)} durationInFrames={D.aliases}>
        <Aliases />
      </Sequence>
      <Sequence from={seq(D.injection)} durationInFrames={D.injection}>
        <InjectionJoke />
      </Sequence>
      <Sequence from={seq(D.showroom)} durationInFrames={D.showroom}>
        <Showroom />
      </Sequence>

      <Sequence from={seq(D.feature)} durationInFrames={D.feature}>
        <FeatureCompare
          icon="no"
          headline="Đã chia tay Cython"
          before={'pip install Cython\npython setup.py build_ext --inplace\n# ... và cầu nguyện Visual C++ 14.0 đã cài'}
          after={'pip install -e ".[dev]"\n# xong.'}
          sub="Không cần 6GB Visual Studio Build Tools chỉ để compile 1 file .pyx bé tí."
        />
      </Sequence>

      <Sequence from={seq(D.speedStat)} durationInFrames={D.speedStat}>
        <SpeedStat />
      </Sequence>
      <Sequence from={seq(D.tagline)} durationInFrames={D.tagline}>
        <Tagline />
      </Sequence>
      <Sequence from={seq(D.closingJoke)} durationInFrames={D.closingJoke}>
        <ClosingJoke />
      </Sequence>
      <Sequence from={seq(D.fileTree)} durationInFrames={D.fileTree}>
        <FileTreeScene />
      </Sequence>
      <Sequence from={seq(D.comingSoon)} durationInFrames={D.comingSoon}>
        <ComingSoon />
      </Sequence>
      <Sequence from={seq(D.outro)} durationInFrames={D.outro}>
        <Outro />
      </Sequence>
    </AbsoluteFill>
  );
};
