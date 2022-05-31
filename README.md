Mnemosyne: Audio Based Flash cards

Mnemosyne is proto type of an audio based flash card system designed specifically for language learning. 

The hardest part of learning a language is memorizing vocabulary. Some improvements were made with applications like Anki and WaniKani, which used SRS or Spaced Repetition Software. SRS leverages the fact that the brain learns better when exposed to pieces of informatiosn over increasing intervals of time.

 However these are less than ideal for language learning where a text based flash card is a poor substitute for audio based inputs an outputs, given that language is functionally an audio based medium.

Mnemosyne is a audio based flash card system which combines SRS with Machine Learning. Users add words to their deck in their target language. Mnemosyne uses free and opensource apis to perform the following.

1. Get the translation for a word ( from LibreTranslate )
2. Get an audio example of a word by a native speaker from HowToPronounce
3. Build a CNN (Convulutional Neural Network) using the audio data verify a users input. 

Users can then review their cards in the following manner.

1. For every card for which a review is due, the English audio is played for that card.
2. Mnemosyne then records user input, and invokes the cnn model to validate that what the user has said corresponds to the word whose translation was played
3. If the user said the word correctly, that word is advanced to the next level.
4. If the user said the word incorrectly, that word is demoted to a previous level.
5. The native audio recording of the word is played.


Currently the main pieces of the application work as expected. If you are a developer familiar with PyQT5/6 please help contribute a front end. I have also considered rewriting this project as a web application in a combination of Rust/WASM/Scala