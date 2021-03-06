import React from "react";
import { Gauge, SmoothGauge } from "./Gauge";

function GaugeGrid(props) {
  return (
    <div class="container my-12 mx-auto px-4 md:px-12">
      <div class="flex flex-wrap -mx-1 lg:-mx-4">
        {/* <AnimatedGuage value={sping.smoothValue} /> */}
        {/* <SmoothGauge value={props.value} units="kg" label="Mass" /> */}
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        <GaugeCard value={props.value} units="kg" label="Mass" />
        {/* <GaugeCard value={props.value} />
        <GaugeCard value={props.value} />
        <GaugeCard value={props.value} />
        <GaugeCard value={props.value} /> */}
      </div>
    </div>
  );
}

function GaugeCard({ value, min, max, label, units }) {
  return (
    <div className="max-w-sm mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4 px-14 pb-20 pt-6 bg-opacity-5 mb-5">
      {/* Gauge */}
      <SmoothGauge
        value={value}
        units={units}
        label={label}
        min={min}
        max={max}
      />
    </div>
  );
}

export { GaugeCard, GaugeGrid };
