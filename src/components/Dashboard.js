import React from "react";
import SensorCard from "./dashboard/Card";
import { GaugeGrid } from "./dashboard/GridOfGauges";

export default function Dashboard(props) {
  return (
    <div>
      <GaugeGrid value={props.telem} />
    </div>
  );
}
