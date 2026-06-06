chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Dot Squad Agent: Received runtime message", message);

  if (message.type === "LED_TRIGGER") {
    const url = `http://127.0.0.1:4001/run/${message.pattern}`;
    console.log("Dot Squad Agent: Fetching", url);

    fetch(url, {
      method: "POST",
    })
      .then((res) => {
        console.log("Dot Squad Agent: Fetch success", res.status);
      })
      .catch((err) => {
        console.error(`Dot Squad Agent: Failed to trigger LED notification`, err);
      });
  }
});
