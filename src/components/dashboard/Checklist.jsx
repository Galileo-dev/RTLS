import React from "react";

function Checklist() {
  return (
    <div>
      <Item />
      <Item />
      <Item />
      <Item />
    </div>
  );
}

function Item() {
  return (
    <div class="max-w-2xl bg-none rounded-md tracking-wide text-left mt-14">
      <div id="header" class="flex ">
        <div class="">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            color="green"
            viewBox="0 0 24 24"
            stroke="currentColor"
            width="30"
            className=""
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <div id="body" class="flex flex-col ml-2">
          <h4
            id="name"
            class="text-xl font-semibold text-gray-400 whitespace-nowrap "
          >
            All System Check
          </h4>
          <p id="Status" class="text-gray-200 mt-1 ">
            Normal
          </p>
        </div>
      </div>
    </div>
  );
}

export { Item, Checklist };
