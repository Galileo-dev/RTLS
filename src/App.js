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
        {/* <Dashboard /> */}
        <Dashboard telem={this.state.telem} />
      </div>
    );
  }
}

export default App;
