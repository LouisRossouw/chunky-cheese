chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("Dot Squad Agent: Received runtime message", message);

  if(message.type === "LED_TRIGGER"){
    fetch(`http://127.0.0.1:4001/run/${message.pattern}`, {
      method: "POST",
    }).catch((err) => {
      console.error(`Failed to trigger LED notification`, err);
    });
  }

});
