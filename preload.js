const { contextBridge, ipcRenderer } = require("electron");
const fs = require('fs');
const path = require('path');

contextBridge.exposeInMainWorld(
  'api', {
    send: (channel, data) => {
      let validChannels = ["toMain"]; // Add more channels as needed
      if (validChannels.includes(channel)) {
        ipcRenderer.send(channel, data);
      }
    },
    receive: (channel, func) => {
      let validChannels = ["fromMain"]; // Add more channels as needed
      if (validChannels.includes(channel)) {
        ipcRenderer.on(channel, (event, ...args) => func(...args));
      }
    },
    readDir: (dirPath, callback) => fs.readdir(dirPath, callback),
    watchDir: (dirPath, options, callback) => fs.watch(dirPath, options, callback),
    joinPath: (...args) => path.join(...args)
  }
);
