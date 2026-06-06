Dot Squad bridge

This chrome extension is responsible for monitoring the KWH values from the home pie electricity kiosk web app and comunicates with the local running dot squad service to trigger the LED patterns. The led service runs locally at 127.0.0.1:4001

Build the extension:

1. Run `npm install`
2. Run `npm run build`
3. The extension will be built in the `dist` folder

Install the extension:

1. Open chrome://extensions/
2. Enable developer mode
3. Click on "Load unpacked"
4. Select the dot_squad_bridge folder
