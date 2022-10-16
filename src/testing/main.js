const { mainHandler } = require("../handlers/main");

const main = async () => {
  const event = {
    httpMethod: "POST",
    body: JSON.stringify({}),
  };
  const res = await mainHandler(event);
  console.log(res);
};

main();
