const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

const fs = require('fs');

function createWindow() {
  // Create the browser window with nodeIntegration enabled and contextIsolation disabled.
  const win = new BrowserWindow({
    width: 1600,
    height: 1600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

ipcMain.on('run-python', (event, args) => {
  console.log("IPC event 'run-python' received", args);
  const scriptPath = path.join(__dirname, 'suno-api/test.py');
  const pythonProcess = spawn('python', [scriptPath, JSON.stringify(args.emotion), args.genre]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    event.reply('python-done', data.toString().trim());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
    event.reply('python-done', code);
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
