const io = require("socket.io")();

var sampleJson = require("./TheJsonStructure.json");
var simple = 1;

io.on("connection", (client) => {
  client.on("subscribeToTelemetry", (interval) => {
    console.log("client is subscribing to telem with interval ", interval);
    setInterval(() => {
      //console.log(sampleJson);
      client.emit("telem", simple);
      simple += 1;
    }, interval);
  });
});

const port = 8000;
io.listen(port);
console.log("listening on port ", port);
