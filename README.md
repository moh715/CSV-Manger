# Csv Manager
#### Video Demo:  https://youtu.be/ncG8kf0L3Qg
#### Description:
Csv Manger is a rule-based chatbot built with spaCy that can create, add to,remove, delete from, and display CSV files using natural language commands like:

- `make new budget file`
- `add "Milk, 10" to groceries file`
- `delete "Price > 100" from sales list`
- `open expenses file`
- `help`

---

## Features

- Create CSV files with custom field names
- Add multiple rows of data with a natural syntax
- Delete specific rows based on conditions
- Show file contents in a readable table format
- Delete entire CSV files
- Help & fallback responses

---
## How to use it
Once the chatbot is running, just type your commands into the terminal. Here are some examples of what you can say:
### Open or View a File

- `open groceries file`
- `show me the expenses list`
- `what is in my budget file`

### Create a New File

- `make a new groceries file`
- `make me a file called expenses`

    The bot will ask you for the field names (e.g., Item, Amount, Date)
##### Or enter:
- `make a new gorceries file "Item, Amount, Date"
to enter the field names directly
### Add Data to a File

- `add "Milk, 3, 2025-04-12" to groceries file
- `add "Rent, 1000, April" to expenses list

    The chatbot will insert this into the matching file based on the field names.
##### Or enter:
- `add to groceries file`
to add or than one row in the same time

### Delete Data from a File

- `delete "Amount > 50" from expenses file`
- `remove "Item == Milk" from groceries file`
##### or enter:
- `delete from expenses file`
- `remove from expenses list`
To choose what you want to delete by row's number

### Delete a File Completely

- `delete groceries file`
- `remove my budget list`

### Get Help

- `help`
---
## 📝 Side Notes

> 💡 **Side Note 1:**
> You can **combine multiple commands** using the word `then`.
> For example:
> `make todo list "task, time" then add "go to gym, 11am" to todo list then show me todo file`

> 🔄 **Side Note 2:**
> You don’t need to include words like `my`, `the`, `to`, or `me` — they are totally optional.
> ✅ These all work the same:
> - `open groceries file`
> - `open my groceries file`
> - `open the groceries file`

> 📁 **Side Note 3:**
> The words **file** and **list** are treated the same, but you must include **one of them** in your command.
> So saying `expenses file` is the same as `expenses list`.




