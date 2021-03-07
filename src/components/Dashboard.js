import React from "react";
import SensorCard from "./dashboard/Card";
import { Checklist } from "./dashboard/Checklist";
import { GaugeGrid } from "./dashboard/GridOfGauges";

export default function Dashboard(props) {
  return (
    <main class="flex w-full h-screen overflow-hidden">
      <div class="w-80 h-screen hidden sm:block">
        <div class="flex flex-col justify-between h-screen p-4 px-12">
          {/* check list */}
          <Checklist />
          {/* Launch / Abort Button */}
          <div class="flex p-3 text-white bg-red-500 rounded cursor-pointer text-center text-sm justify-center w-1/2 ">
            <button class="rounded inline-flex items-center ">
              <svg
                class="w-4 h-4 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span class="font-semibold text-m">Launch</span>
            </button>
          </div>
        </div>
      </div>

      <GaugeGrid value={props.telem} />

      <div class="w-80 h-screen hidden sm:block">
        <div class="flex flex-col justify-between h-screen p-4 px-12">
          {/* check list */}
          <Checklist />
          {/* Launch / Abort Button */}
          <div class="flex p-3 text-white bg-red-500 rounded cursor-pointer text-center text-sm justify-center w-1/2 ">
            <button class="rounded inline-flex items-center ">
              <svg
                class="w-4 h-4 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
                  clipRule="evenodd"
                />
              </svg>
              <span class="font-semibold text-m">Launch</span>
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
