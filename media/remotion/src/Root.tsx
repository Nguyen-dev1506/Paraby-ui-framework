import { Composition } from "remotion";
import { ParabyIntro, TOTAL_DURATION_IN_FRAMES } from "./ParabyIntro";
import { CLITutorial, TOTAL_DURATION_IN_FRAMES as CLI_TUTORIAL_DURATION } from "./CLITutorial";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="ParabyIntro"
        component={ParabyIntro}
        durationInFrames={TOTAL_DURATION_IN_FRAMES}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="ParabyCLITutorial"
        component={CLITutorial}
        durationInFrames={CLI_TUTORIAL_DURATION}
        fps={30}
        width={1280}
        height={720}
      />
    </>
  );
};
