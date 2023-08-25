# League-of-Legends-Chat-Filter

### About the program
This program is used to filter your chat in League of Legends. It deletes all your bad words defined in the ban_words.txt file. It should be run before jumping in a game, but will also work if you start it after.
It is made to work only when the game is in focus, meaning that if you're doing something else it doesn't read your input. Though it might be flagged by your antivirus as a chat-logger, it has no harm.

### Before you start
Its recomended to first test it in the practice tool mode, so you can change some setting if it takes up lots of CPU usage and to setup your x and y points of the chat box, defined in the on_mouse_click() function. The thing that could be changed for better preformance are the 2 time.sleep functions,
or using only the on_key_press() function by itself without threads.


### To start the program run this command
```
 python FuncionalityForProgramFinished.py
```

### Things to be finished

I'm currently working on implementing a snippet tool that enables you to create a rectangle where your chat box is located and hopefully a gui for easier use.


