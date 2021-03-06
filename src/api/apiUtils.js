import openSocket from "socket.io-client";
const socket = openSocket("http://localhost:8000", {
  transports: ["websocket"],
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  reconnectionAttempts: Infinity,
});

function subscribeToTelemetry(cb) {
  socket.on("telem", (telem) => cb(null, telem));
  socket.emit("subscribeToTelemetry", 200);
}
export { subscribeToTelemetry, socket };
