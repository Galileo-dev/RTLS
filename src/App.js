import { subscribeToTelemetry, socket } from "./api";
import logo from "./logo.svg";
import React from "react";
import Dashboard from "./Dashboard";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    socket.on("connect", () => {
      console.log("connected");
      subscribeToTelemetry((err, telem) =>
        this.setState({
          telem,
        })
      );
    });
  }

  state = {
    telem: "no timestamp yet",
  };

  render() {
    return (
      <div className="App">
        This is the timer value: {JSON.stringify(this.state.telem)}
        {/* <Dashboard /> */}
      </div>
    );
  }
}

export default App;
