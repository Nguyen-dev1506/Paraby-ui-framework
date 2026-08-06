import { Composition } from "remotion";
import { ParabyIntro, TOTAL_DURATION_IN_FRAMES } from "./ParabyIntro";

export const Root: React.FC = () => {
  return (
    <Composition
      id="ParabyIntro"
      component={ParabyIntro}
      durationInFrames={TOTAL_DURATION_IN_FRAMES}
      fps={30}
      width={1280}
      height={720}
    />
  );
};
