import { subscribeToTelemetry, socket } from "./api/apiUtils";
import logo from "./logo.svg";
import React from "react";
import Dashboard from "./components/Dashboard";
import "./App.css";
import SensorCard from "./components/dashboard/Card";
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
    telem: 0,
  };

  render() {
    return (
      <div className="App">
        <p className="text-gray-500">
          This is the timer value: {JSON.stringify(this.state.telem)}{" "}
        </p>
        {/* <Dashboard /> */}
        <Dashboard telem={this.state.telem} />
      </div>
    );
  }
}

export default App;
