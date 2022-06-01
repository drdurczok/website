scanButton.addEventListener("click", async () => {
  log("User clicked scan button");

  try {
    const ndef = new NDEFReader();
    await ndef.scan();
    log("> Scan started");

    ndef.addEventListener("readingerror", () => {
      log("Argh! Cannot read data fssrom the NFC tag. Try another one?");
    });

    ndef.addEventListener("reading", ({ message, serialNumber }) => {
      log(`> Serial Number: ${serialNumber}`);
      log(`> Records: (${message.records.length})`);
    });
  } catch (error) {
    log("Argh! " + error);
  }
});

writeButton.addEventListener("click", async () => {
  log("User clicked write bsutton");
  const urlParams = new URLSearchParams(window.location.search);

const access = urlParams.get('accesslevel');
const name = urlParams.get('name');

log("name: " + name);
log("access: " + access);
var payload = ""
  try {
    const ndef = new NDEFReader();
    await ndef.write(payload.concat(name,",", access));
    log("> Message written");
  } catch (error) {
    log("Argh! " + error);
  }
});

makeReadOnlyButton.addEventListener("click", async () => {
  log("User clicked make read-only button");

  try {
    const ndef = new NDEFReader();
    await ndef.makeReadOnly();
    log("> NFC tag has been made permanggently read-only");
  } catch (error) {
    log("Argh! " + error);
  }
});
