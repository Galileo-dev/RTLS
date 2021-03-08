import React from "react";
import { scaleLinear } from "d3-scale";
import { useSpring, animated } from "react-spring";

function ProgressBarList({ value }) {
  return (
    <div>
      <ProgressBar
        progress={value}
        color="#298BFE"
        name={"Altitude"}
        units={"km"}
        min={0}
        max={1000}
      />
      <ProgressBar
        progress={value}
        color="#298BFE"
        name={"Altitude"}
        units={"km"}
        min={0}
        max={1000}
      />
      <ProgressBar
        progress={value}
        color="#298BFE"
        name={"Altitude"}
        units={"km"}
        min={0}
        max={1000}
      />
      <ProgressBar
        progress={value}
        color="#298BFE"
        name={"Altitude"}
        units={"km"}
        min={0}
        max={1000}
      />
    </div>
  );
}

function ProgressBar({ progress, color, name, units, min, max }) {
  const percentScale = scaleLinear().domain([min, max]).range([0, 100]);
  const percent = percentScale(progress);
  const PercentSpring = useSpring({ value: percent });
  const props = useSpring({ width: `${percent}%`, from: { width: "0%" } });
  return (
    <div className="relative pt-12">
      <div className="flex mb-2 items-center justify-between w-full">
        <div>
          <span className="text-xs font-semibold inline-block py-0.5 uppercase text-white">
            Task in progress
          </span>
        </div>
        <div className="text-right">
          <span className="text-xs font-semibold inline-block text-white">
            {`${Math.round(percent)}%`}
          </span>
        </div>
      </div>
      <div className="overflow-hidden h-2 mb-4 text-xs flex rounded bg-gray-400 bg-opacity-10">
        <animated.div
          style={{ backgroundColor: color, width: props.width }}
          className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center opacity-100"
        ></animated.div>
      </div>
    </div>
  );
}

export { ProgressBar, ProgressBarList };
