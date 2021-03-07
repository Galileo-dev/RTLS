const io = require("socket.io")();

var sampleJson = require("./TheJsonStructure.json");
var simple = 1;

async function main() {
  while (true) {
    simple += 1;
    if (simple >= 1000) {
      simple = 0;
    }
    await timer(10);
  }
}
main();
io.on("connection", (client) => {
  client.on("subscribeToTelemetry", (interval) => {
    console.log("client is subscribing to telem with interval ", interval);
    setInterval(() => {
      //console.log(sampleJson);
      client.emit("telem", simple);
    }, interval);
  });
});

const port = 8000;
io.listen(port);
console.log("listening on port ", port);

function timer(ms) {
  return new Promise((res) => setTimeout(res, ms));
}
