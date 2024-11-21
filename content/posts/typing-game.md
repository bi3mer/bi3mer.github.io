+++
date = '2020-08-20T18:27:14-05:00'
draft = false
title = 'Typing Game'
+++
In this post, I want to show how to implement a simple web-based typing game. A version of the final product is online; the code is on Github. The game has a menu screen where users can select whether or not to allow capitals letters and press a button to start the game. When the player begins the game, they’ll see characters—not necessarily a valid word, more an assortment of letters—to type. After the user has finished typing, the next value will be longer than the previous one. The game continues until the player mistypes. At which point, the user can see how well they did and restart.

# Finite State Machine
To implement and organize the top-level behavior of the game, we are going to use a [finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine). A finite-state machine is a set of states and transitions where only one state can be active at a time. A state can have many transitions, both incoming and outgoing. A state defines expected behavior. A transition is a link between two states, it is not bidirectional, and it can have conditions—such as transition can only run when X is less than Y. A state cannot have multiple valid transitions at a time to guarantee deterministic behavior.

## States

At the minimum, we need three states: menu, game, and game over. The game state could be broken down into additional states like user input, check input, generate, and update UI, but this is, in my opinion, overkill as it would add complexity to the code.

### Menu State

The menu state allows players to click a button to change the state and toggle whether capital letters are allowed. Capturing a button click is simple in JavaScript and is in the code below.

```js
document.getElementById('startButton').onclick = () => {
  document.getElementById('menu').style.display = "none";
  document.getElementById('game').style.display = "";

  runGame();
};
```

Looking at the code block, you’ll see that there is HTML that defines a start button and two elements: `menu` and `game`. These are divs that contain each state’s HTML. When the user switches between states, one div is hidden and the other is exposed. Furthermore, there is a `runGame` function which we’ll look at in the game state section. For now, know that it switches the state from `menu` to `game`.

The other functionality is the [toggle](https://www.w3schools.com/howto/howto_css_switch.asp) for capital letters. The link shows how to create a toggle in HTML, and now we need to save the user’s preferences. If they come back to the page, they will have their setting from before by using [cookies](https://www.w3schools.com/js/js_cookies.asp). To set the cookie we use:

```js
allowCapitals = document.getElementById('allowCapitals').checked; 
document.cookie = `capitals=${allowCapitals};`;
```

The cookie could update on changes to the toggle. In this implementation, though, the value is saved when the user exits the menu state. With the cookie stored, we can use it on startup:

```js
(() => {
  const cookies = document.cookie.split(';');
  for(let cookie of cookies) {
    console.log(typeof cookie);
    if(cookie.includes('capitals')) {
      allowCapitals = cookie.split('=')[1] === 'true' ? true : false;
      document.getElementById('allowCapitals').checked = allowCapitals;
    }
  }
})();
```

This block of code searches for the cookie. If it finds it, it will split the cookie up to find whether or not the stored value is true or false and update the HTML. Before the game starts it will check the HTML, so there is no reason to store the value found.

### Game State
In the game state, we need to handle generating words, validating input, and ending the game.

```js
const characters = 'abcdefghijklmnopqrstuvwxyz';
function generateNonsenseWord(size) {
  let string = '';
  for(var i = 0; i < size; ++i) {
    let char = characters[Math.floor(Math.random() * characters.length)];
    if(allowCapitals === true && Math.random() > 0.5) {
      char = char.toUpperCase()
    }
    
    string += char;
  }

  return string;
}
```

This function handles the generation of nonsense words and uses a constant variable named characters that contains every letter in the alphabet. We start with an empty string and add random characters to it until it is the requested length. To capitalize, JavaScript has a convenient function `toUpperCase`. It is used if the user has asked for capital letters, and a random number—between 0 and 1—is greater than 0.5.

We can now display the word to the user. But when we do that, we want to do a bit more. In this game, the user has five seconds to input the nonsense word till they lose. To get this behavior [setInterval](https://www.w3schools.com/jsref/met_win_setinterval.asp) is used; this isn’t an approach that I’d recommend, and I discuss a better, more organized way in the improvements section below.

```js
function setUpNextWord() {
  if(timer !== null) {
    clearInterval(timer);
  }

  wordIndex = 0;
  timeVal = 5;
  document.getElementById('timer').innerText = timeVal;

  timer = setInterval(() => {
    timeVal -= 1;
    timeElapsed += 1;
    document.getElementById('timer').innerText = timeVal;

    if(timeVal <= 0) {
      endGame();
    }
  }, 1000);

  wordsTyped += 1;
  word = generateNonsenseWord(wordsTyped + 1);
  document.getElementById('textHere').innerText = word;
};
```

This function first clears the previously created interval if it exists. If we don’t do this, then the game will automatically terminate after five seconds have passed. Note that creating a new interval does not destroy an existing one. From there, we update the `wordIndex` to 0. This variable represents where in the word the user is typing. So if the user is given the word “asdf” than at 0, they are expected to type “a”. This is a cruel way of building the game because it doesn’t allow for any mistyping.

From there, it updates the `timeVal` to 5; the user has five seconds to type the next word and the UI updates to show this. Then, an interval is created and stored. The interval will, every second, reduce the `timeVal` and increment the `timeElapsed` variable. The latter represents how long the player has played the current game session; not the total time they have had the web application open. After it will update the UI, and if the `timeVal` is less than or equal to 0, it will call the `endGame` function. After creating the interval, we increment the number of words typed—the `wordsTyped` variable starts at -1, so they don’t get credit for a word not yet typed—and the UI shows the next value for the user to type.

```js
function runGame() {
  state = 'game';
  timeElapsed = 0;
  wordsTyped = -1;

  allowCapitals = document.getElementById('allowCapitals').checked; 
  document.cookie = `capitals=${allowCapitals};`;

  document.getElementById('words').focus();
  setUpNextWord();
}
```

Above is the second to last function related to the game state and does a few things. It updates the state and resets variables for the time elapsed and the number of words typed. You’ll recognize the next two lines of code for getting whether or not capitals are allowed and storing the result as a cookie. The next line focuses the input field; the user can type without having to click on the UI. Finally, we call the function we just described in detail, which starts the game process.

```js
document.getElementById('words').oninput = (data) => {
  if(word[wordIndex] === data.data) {
    ++wordIndex;
    if(wordIndex >= word.length) {
      setUpNextWord();
    }
  } else {
    endGame();
  }
};
```

This code block uses the `oninput` event for the input field. Every time the user types a character, this function is called. It receives an argument that has a value that represents the new keypress. We check that keypress against the expected value. If the characters match, then the word index is incremented. If that index is larger than the expected word length, a new word is set up. Else, we wait for the next input from the user or for the interval to end the game. If the input does not match the expected value, then we end the game.

### Game Over State
This state displays the results from the game and has a button that the player can click to restart.

```js
function endGame() {
  state = 'end';
  if(timer !== null) {
    clearInterval(timer);
  }

  document.getElementById('game').style.display = "none";

  const resultText = `You successfully typed ${wordsTyped} nonsense words in ${timeElapsed} seconds without any errors!`
  document.getElementById('endResults').innerText = resultText;
}
```

The state is updated, and the interval is destroyed. If we don’t do this then we can get into an undefined state; this is one of the reasons why intervals are not the best tool. We also change the display to the end game state. The text built says how many words the user typed in the elapsed time—the UI updates to display the text.

```js
document.getElementById('restartButton').onclick = () => {
  document.getElementById('end').style.display = "none";
  document.getElementById('game').style.display = "";

  runGame();
};
```

This code restarts the game. The UI hides the end game HTML and shows the game HTML. Then the run game function is called to start the game.

# Improvements

The use of intervals is problematic. There are edge-cases like the player inputting the last character at precisely 5 seconds. Will the input be called first, or will the interval be called first? As a programmer, I cannot say, and that is a problem. In a typical game engine, a loop determines the order of operations for everything. In a web-based JavaScript game, a top-level loop will freeze the browser. There is an alternative: [requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame). It runs every frame and can call any function given as an argument; the input function receives an argument of delta time which is the time between the last call and the current call. We can now keep track of time and make the order of operations deterministic. Unfortunately, we can’t by default get a list of key presses between frames. To implement this, we would use the [on keypress event](https://stackoverflow.com/questions/16089421/how-do-i-detect-keypresses-in-javascript/16089470#16089470) to store the values in a list that can be accessed in the loop. Before the loop finishes, the last action would be to clear the list of key presses.

# Conclusion

In this post, I have shown you the basics of creating a simple typing game in JavaScript with HTML as a UI. The full code is available on [GitHub](https://github.com/bi3mer/AnotherTypingGame), which is necessary as I haven’t gone through the HTML side of this. I have also shown the basics of a finite-state machine and how it can be used to organize a code-base for games. Finally, I have discussed why intervals in JavaScript are not the best tool for games, and I have gone over a more organized approach that can guarantee order of operations.