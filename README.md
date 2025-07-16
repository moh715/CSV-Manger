# CSV Manager

### Video Demo: [Watch on YouTube](https://youtu.be/ncG8kf0L3Qg)

### Description:
**CSV Manager** is a rule-based chatbot built with **spaCy** that allows you to create, view, add to, delete from, and manage CSV files using natural language commands.

For example:
- `make new budget file`
- `add "Milk, 10" to groceries file`
- `delete "Price > 100" from sales list`
- `open expenses file`
- `help`

---

## Features

- Create CSV files with custom field names
- Add multiple rows using simple language
- Delete rows based on conditions
- Show file contents in a readable table
- Delete entire CSV files
- Help and fallback responses for invalid input

---

## How to Use

Once the chatbot is running, simply type your commands in the terminal. Here are some examples:

### Open or View a File
- `open groceries file`
- `show me the expenses list`
- `what is in my budget file`

### Create a New File
- `make a new groceries file`
- `make me a file called expenses`
- `make a new groceries file "Item, Amount, Date"` (to include fields directly)

The bot will ask for field names if not provided.

### Add Data to a File
- `add "Milk, 3, 2025-04-12" to groceries file`
- `add "Rent, 1000, April" to expenses list`

Or use:
- `add to groceries file`  
To add multiple rows interactively.

### Delete Data from a File
- `delete "Amount > 50" from expenses file`
- `remove "Item == Milk" from groceries file`

Or use:
- `delete from expenses file`  
- `remove from expenses list`  
To delete by row number.

### Delete a File Completely
- `delete groceries file`
- `remove my budget list`

### Get Help
- `help`

---

## Extra Notes

- 🔗 **You can chain commands** with `then`:

`make todo list "task, time" then add "go to gym, 11am" to todo list then show me todo file`


-  You can skip extra words like `my`, `the`, `to`, or `me` — they're optional:
- `open groceries file`
- `open my groceries file`
- `open the groceries file` → All mean the same thing.

-  `file` and `list` are treated the same — but you **must use one** of them in the command:
-  `expenses file` = `expenses list`




