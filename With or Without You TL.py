<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>"With or Without You" U2  Drag & Drop</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #e6f2ff; 
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .sticky-header {
      position: sticky;
      top: 0;
      background-color: #e6f2ff;
      padding: 15px 0;
      width: 100%;
      z-index: 100;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }
    .container {
      display: flex;
      justify-content: space-between;
      gap: 30px;
      margin-bottom: 30px;
      width: 90%;
      max-width: 1200px;
    }
    .column {
      width: 45%;
      position: relative;
    }
    .sticky-column {
      position: sticky;
      top: 160px; 
      max-height: calc(100vh - 200px);
      overflow-y: auto;
      padding-right: 10px;
    }
    .word, .definition {
      padding: 15px;
      border: 1px solid #ccc;
      margin: 10px 0;
      background-color: #fff;
      cursor: pointer;
      border-radius: 5px;
      transition: background-color 0.3s ease;
    }
    .word:hover, .definition:hover {
      background-color: #b3e0ff;
    }
    .droppable {
      min-height: 50px;
      border: 2px dashed #ddd;
      padding: 15px;
      margin-bottom: 10px;
      background-color: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 5px;
    }
    .correct {
      background-color: #a5d6a7;
      color: #2e7d32;
    }
    .incorrect {
      background-color: #ffccbc;
      color: #d32f2f;
    }
    .matched-pair {
      display: flex;
      border-radius: 5px;
      overflow: hidden;
      margin-bottom: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .matched-pair .word {
      flex: 1;
      margin: 0;
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }
    .matched-pair .definition {
      flex: 3;
      margin: 0;
      border-top-left-radius: 0;
      border-bottom-left-radius: 0;
      border-left: none;
    }
    #feedback {
      margin-top: 20px;
      font-size: 1.2em;
      text-align: center;
    }
    .game-controls {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 20px;
      margin-bottom: 20px;
      width: 100%;
    }
    .popup {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: white;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      z-index: 1000;
      text-align: center;
    }
    .overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.5);
      z-index: 999;
    }
    .signature {
      margin-top: 30px;
      font-size: 0.9em;
      text-align: center;
      width: 100%;
    }
    
    .content-padding {
      height: 100px;
    }
  </style>
</head>
<body>
<div class="sticky-header">
  <div class="game-controls">
    <label for="time-limit">Time Limit:</label>
    <select id="time-limit">
      <option value="0">No Limit</option>
      <option value="180">3 Minutes</option>
      <option value="300">5 Minutes</option>
      <option value="420">7 Minutes</option>
      <option value="600">10 Minutes</option>
    </select>
    <div id="timer">Time: --:--</div>
    <div id="score">Score: 0/10</div>
    <button id="reset-game">Reset Game</button>
  </div>

  <h2>"With or Without You" U2 ::  Drag & Drop (Target Language)</h2>

  <p>Drag the word to the correct definition on the right.</p>
</div>

<div class="container">
  <!-- Words Column -->
  <div class="column">
    <div id="words" class="sticky-column">
      <!-- Words will be populated by JavaScript -->
    </div>
  </div>

  <!-- Definitions Column -->
  <div class="column">
    <div id="definitions">
      <!-- Definitions will be populated by JavaScript -->
    </div>
  </div>
</div>

<div id="feedback"></div>

<div class="content-padding"></div>

<script>
  
  const vocabularyData = [
    { word: 'Stone', definition: 'The hard solid substance found in the ground.' },
    { word: "Sleight of hand", definition: 'Skillful hiding of the truth in order to win an advantage.' },
    { word: 'Twist of Fate', definition: 'Any change of fate.' },
    { word: 'Bed of Nails', definition: 'Figuratively something really uncomfortable.' },
    { word: 'Through', definition: 'From one end or side of something to the other .' },
    { word: 'Storm', definition: 'An extreme weather condition with heavy rain.' },
    { word: "Shore", definition: 'The land along the edge of a sea, lake or wide river.' },
    { word: 'Give Yourself Away', definition: 'To dedicate to someone without expecting anything in return' },
    { word: 'Tied', definition: 'Fastened together.' },
    { word: 'Bruised', definition: 'Hurt as a result of a bad experience.' },
  ];

  
  function shuffle(array) {
    const newArray = [...array];
    for (let i = newArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
    }
    return newArray;
  }

  
  let draggedWord = null;
  let matchedWords = 0;
  let gameTimer = null;

  
  function initGame() {
    const wordsColumn = document.getElementById('words');
    const definitionsColumn = document.getElementById('definitions');
    
    
    wordsColumn.innerHTML = '';
    definitionsColumn.innerHTML = '';

    
    const shuffledWords = shuffle([...vocabularyData]);
    
    
    const shuffledDefs = shuffle([...vocabularyData]);

    
    shuffledWords.forEach((item, index) => {
      const wordElement = document.createElement('div');
      wordElement.classList.add('word');
      wordElement.draggable = true;
      wordElement.id = `word-${index}`;
      wordElement.dataset.originalWord = item.word; // Store original word
      wordElement.dataset.originalDef = item.definition; // Store matching definition
      wordElement.textContent = item.word;
      wordElement.addEventListener('dragstart', dragStart);
      wordsColumn.appendChild(wordElement);
    });

    
    shuffledDefs.forEach((item, index) => {
      const defElement = document.createElement('div');
      defElement.classList.add('droppable');
      defElement.id = `def-${index}`;
      defElement.dataset.originalDef = item.definition; // Store original definition
      defElement.textContent = item.definition;
      defElement.addEventListener('dragover', dragOver);
      defElement.addEventListener('drop', drop);
      definitionsColumn.appendChild(defElement);
    });

    
    matchedWords = 0;
    document.getElementById('score').textContent = `Score: 0/10`;
    document.getElementById('feedback').innerHTML = '';

    
    startTimer();
  }

  
  function startTimer() {
    const timeLimit = parseInt(document.getElementById('time-limit').value);
    const timerDisplay = document.getElementById('timer');
    
    
    if (gameTimer) clearInterval(gameTimer);

    if (timeLimit > 0) {
      let timeRemaining = timeLimit;
      
      gameTimer = setInterval(() => {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        timerDisplay.textContent = `Time: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        
        if (timeRemaining <= 0) {
          clearInterval(gameTimer);
          showPopup('Time is up! Game Over', false);
        }
        
        timeRemaining--;
      }, 1000);
    } else {
      timerDisplay.textContent = 'Time: --:--';
    }
  }

  // Drag and drop events
  function dragStart(event) {
    draggedWord = event.target;
    event.dataTransfer.setData("text", event.target.id);
  }

  function dragOver(event) {
    event.preventDefault();
  }

  function drop(event) {
    event.preventDefault();
    const droppedOn = event.target.closest('.droppable');
    
    if (!droppedOn || droppedOn.classList.contains('matched')) return;

    const draggedWordDef = draggedWord.dataset.originalDef;
    const droppableDef = droppedOn.dataset.originalDef;

    if (draggedWordDef === droppableDef) {
      // Create a matched pair container
      const matchedPair = document.createElement('div');
      matchedPair.classList.add('matched-pair');
      
      
      const wordPart = document.createElement('div');
      wordPart.classList.add('word', 'correct');
      wordPart.textContent = draggedWord.textContent;
      
      
      const defPart = document.createElement('div');
      defPart.classList.add('definition', 'correct');
      defPart.textContent = droppedOn.textContent;
      
      
      matchedPair.appendChild(wordPart);
      matchedPair.appendChild(defPart);
      
      
      droppedOn.parentNode.replaceChild(matchedPair, droppedOn);
      
      
      draggedWord.style.display = 'none';
      
      
      matchedPair.classList.add('matched');
      showPopup('Correct!', true);
      
      matchedWords++;
      document.getElementById('score').textContent = `Score: ${matchedWords}/10`;

      if (matchedWords === 10) {
        clearInterval(gameTimer);
        showPopup('Congratulations! You matched all words!', true);
      }
    } else {
      showPopup('Incorrect. Try again!', false);
    }
  }

  
  function showPopup(message, isCorrect) {
    // Remove any existing popups
    const existingOverlay = document.querySelector('.overlay');
    if (existingOverlay) existingOverlay.remove();

    const overlay = document.createElement('div');
    overlay.classList.add('overlay');

    const popup = document.createElement('div');
    popup.classList.add('popup');
    popup.innerHTML = `
      <h2 style="color: ${isCorrect ? '#2e7d32' : '#d32f2f'}">${message}</h2>
      <button onclick="this.closest('.overlay').remove()">Close</button>
    `;

    overlay.appendChild(popup);
    document.body.appendChild(overlay);

    
    setTimeout(() => {
      if (document.body.contains(overlay)) {
        document.body.removeChild(overlay);
      }
    }, 2000);
  }

  
  document.getElementById('time-limit').addEventListener('change', startTimer);
  document.getElementById('reset-game').addEventListener('click', initGame);
  
  
  initGame();
</script>

<div class="signature">
  &copy; 2025 Daniel Rojas :: TΣʃ :: &#9993; <a href="mailto:CVO@tesh.pro">CVO@tesh.pro</a>
</div>
</body>
</html>
