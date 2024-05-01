const fs = require('fs');
const path = require('path');
const { ipcRenderer } = require('electron');

let initialFiles = new Set();
const trackList = document.getElementById('trackList');
const loadingIndicator = document.getElementById('loading');

function writeJSONFile(filename, content) {
  const filePath = path.join(__dirname, 'data', filename);
  fs.writeFileSync(filePath, JSON.stringify(content, null, 2), 'utf-8');
}

function loadInitialFiles() {
  const downloadsFolder = path.join(__dirname, 'downloads');
  fs.readdir(downloadsFolder, (err, files) => {
    if (err) {
      console.error("Failed to read downloads folder:", err);
      return;
    }
    files.forEach(file => {
      if (file.endsWith('.mp3')) {
        addTrackToList(file);
        console.log("Adding file to initial files:", file);
      }
    });
  });
}

function monitorNewFiles() {
  const downloadsFolder = path.join(__dirname, 'downloads');
  fs.watch(downloadsFolder, { encoding: 'buffer' }, (eventType, filename) => {
    if (filename && filename.toString().endsWith('.mp3')) {
      const fullPath = path.join(downloadsFolder, filename.toString());
      if (!initialFiles.has(filename.toString())) {
        alert('New song available for playback: ' + filename);
        initialFiles.add(filename.toString());
        addTrackToList(filename.toString());
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.src = fullPath;
        audioPlayer.load();
      }
    }
  });
}

function addTrackToList(filename) {
    const listItem = document.createElement('li');
    listItem.textContent = filename;
    listItem.addEventListener('click', function() {
        const downloadsFolder = path.join(__dirname, 'downloads');
        const imagesFolder = path.join(__dirname, 'images');
        const filePath = path.join(downloadsFolder, filename);
        const audioPlayer = document.getElementById('audioPlayer');
        const albumCover = document.getElementById('albumCover');

        // Replace '.mp3' with '.png' to form the image filename
        const imageFilename = filename.replace('.mp3', '.png');
        const imagePath = path.join(imagesFolder, imageFilename);

        // Update audio source
        audioPlayer.src = filePath;
        audioPlayer.load();
        audioPlayer.play();

        // Check if the specific album cover exists, if not, use the default
        albumCover.src = fs.existsSync(imagePath) ? imagePath : path.join('default_album_cover.png');
    });
    trackList.appendChild(listItem);
}


ipcRenderer.on('python-done', (event, code) => {
  document.getElementById('loading').style.display = 'none';
  console.log(`Script exit code: ${code}`);
  if (parseInt(code) === 0) {
    alert('Processing completed. Check for new songs!');
  }
  if (parseInt(code) === 1){
    alert('Error running Python script');
  }
});


// Initial setup when the application loads
document.addEventListener('DOMContentLoaded', function() {
    const albumCover = document.getElementById('albumCover');
    albumCover.src = 'default_album_cover.png'; // Set the default album cover on initial load
    // Check if the album cover's src contains the default filename
    if (albumCover.src.includes('default_album_cover.png')) {
        console.log("Using default album cover");
    } else {
        console.log("Album cover found");
    }
});

document.getElementById('run').addEventListener('click', () => {
    console.log("Generate button clicked");
    const emotion = {
        'Attention': parseInt(document.getElementById('attention').value, 10),
        'Engagement': parseInt(document.getElementById('engagement').value, 10),
        'Excitement': parseInt(document.getElementById('excitement').value, 10),
        'Relaxation': parseInt(document.getElementById('relaxation').value, 10),
        'Interest': parseInt(document.getElementById('interest').value, 10),
        'Stress': parseInt(document.getElementById('stress').value, 10)
    };
    const genre = document.getElementById('genre').value;
    const dataToSend = {
        emotion: emotion,
        genre: genre
    };
    writeJSONFile('emotion_data.json', emotion);
    writeJSONFile('genre_data.json', { genre });
    console.log("Sending data to Python:", dataToSend);
    ipcRenderer.send('run-python', dataToSend);
    document.getElementById('loading').style.display = 'block';
});

// Ensure the data directory exists
const dataDirPath = path.join(__dirname, 'data');
if (!fs.existsSync(dataDirPath)){
    fs.mkdirSync(dataDirPath);
}


// Initial setup
loadInitialFiles();
monitorNewFiles();
