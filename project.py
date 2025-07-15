import csv
import os
from rich.console import Console
from rich.table import Table
import spacy
from spacy.language import Language
from spacy.tokens import Span
from spacy.matcher import Matcher
import random
import re
import operator


class CsvManger():
    def __init__(self, filename: str):
        self.filename = filename

    def fieldnames(self):
        with open(self.filename) as f:
            reader = csv.DictReader(f)
            feilds = reader.fieldnames
        return feilds

    def data(self):
        with open(self.filename) as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
        return data

    def add_rows(self, data):
        field = self.fieldnames()
        data = sorted(data, key=lambda s: s[field[0]])
        marged = marge(self.data(), data, lambda s: s[field[0]])
        with open(self.filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writeheader()
            writer.writerows(marged)

    def delete_from_file(self, filtered_data):
        reader = self.data()
        if len(reader) <= 0:
            return

        new_reader = list(filter(lambda x: x not in filtered_data, reader))
        field = self.fieldnames()
        # Rewrite file
        with open(self.filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writeheader()
            writer.writerows(new_reader)

    def show_data(self, title, to_fileter=lambda s: True, sort_key=0):
        console = Console()
        table = Table(title=title)
        fields = self.fieldnames()
        data = self.data()
        table.add_column("#", style="dim")
        for fild in fields:
            table.add_column(fild, style="cyan", justify="left")
        fileter_data = list(filter(to_fileter, data))
        for num, value in enumerate(sorted(fileter_data, key=lambda s: s[fields[sort_key]]), start=1):
            values = [str(v) if v else "no data" for k, v in value.items()]
            values = [str(num)] + values
            table.add_row(*values)

        with console.capture() as capture:
            console.print(table)
        return f"this is {self.filename}\n{capture.get()}"

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        if filename[-4:] != ".csv":
            filename = f"{filename}.csv"
        if not os.path.exists(filename):
            raise ValueError("file not exists")
        with open(filename) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = sorted([row for row in reader], key=lambda s: s[fieldnames[0]])
        with open(filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        self._filename = filename

    def filtering(self, strfilter: str):
        ops = {
            "=": operator.eq,
            "==": operator.eq,
            "!=": operator.ne,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le
        }
        conditions = strfilter.replace("\"", "").replace("'", "").split(",")
        filtered_data = self.data()
        for condition in conditions:
            if len(filtered_data) == 0:
                break
            if not (cond_match := re.match(r"(\w+)\s*([=!><]=?)\s*(.+)", condition)):
                raise ValueError("input is not valid")
            field, op, value = cond_match.groups()
            if field not in self.fieldnames():
                raise ValueError(
                    f"Error: '{field}' is not a valid column in {self.filename.replace(".csv", "")}.")
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    value = value.strip('"').strip("'")

            filter_op = ops.get(op)
            match_data = []
            for row in filtered_data:
                if not filter_op:
                    raise ValueError(
                        f"Error: Unsupported operator '{op_symbol}'. Use ==, !=, >, <, >=, or <=.")
                try:
                    # Convert row_value to the same type as value
                    row_value = type(value)(row[field])
                except (ValueError, TypeError):
                    pass  # If conversion fails, keep row_value as is

                if filter_op(row_value, value):
                    match_data.append(row)
            filtered_data = list(filter(lambda x: x in match_data, filtered_data))
            match_data = []
        return filtered_data

    @classmethod
    def make_file(cls, filename, feildnames: str = None):
        if filename[-4:] != ".csv":
            filename = f"{filename}.csv"
        if not feildnames:
            # ask the user what is the feilds call
            feildnames = map(lambda s:s.strip(), input(f"Enter field names for '{filename}', separated by commas: ").split(","))
        else:
            feildnames = map(lambda s:s.strip(), re.sub("(\"|')","", feildnames).split(","))
        with open(filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=feildnames)
            writer.writeheader()
        return cls(filename)

    @classmethod
    def make_show(cls, filename: str, filterd: str = None):
        f = cls(filename)
        if not f.data():
            return f"{filename.replace(".csv", "")} is empty."
        if filterd:
            try:
                filterd_data = f.filtering(filterd)
            except Exception as e:
                return e
            return f.show_data("", lambda x: x in filterd_data)
        return f.show_data("")




# making the nlp and the matcher
nlp = spacy.blank("en")
matcher = Matcher(nlp.vocab)


def main():
    # BOT loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        print("Csv Manger:", chatbot_response(user_input))


@Language.component("FILE_NAME_ner")
def FILE_NAME_ner(doc):
    ole = list(doc.ents)
    for i in range(len(doc)):
        if doc[i].text.lower() in ["list", "file"]:
            new_ent = Span(doc, i-1, i, label="FILE_NAME")
            ole.append(new_ent)
    doc.ents = ole
    return doc


@Language.component("SECOND_INPUT_ner")
def SECOND_INPUT_ner(doc):
    patterns2 = r"(\"|')[^\"']+(\"|')"
    ole = list(doc.ents)
    matches = re.finditer(patterns2, doc.text)
    for match in matches:
        start, end = match.span()
        span = doc.char_span(start, end)
        new_ent = Span(doc, span.start, span.end, label="SECOND_INPUT")
        if new_ent:
            ole.append(new_ent)
    doc.ents = ole
    return doc


nlp.add_pipe("FILE_NAME_ner", last=True)
nlp.add_pipe("SECOND_INPUT_ner", last=True)


# function patterns
patterns = {
    "open_file": [[{"LOWER": {"IN": ["open", "show", "what"]}}, {"LOWER": {"IN": ["is", "in", "my", "the", "me"]}, "OP": "*"}, {"ENT_TYPE": "FILE_NAME"}, {"ENT_TYPE": "SECOND_INPUT", "OP": "*"}]],
    "delete_file": [[{"LOWER": {"IN": ["delete", "remove"]}},  {"LOWER": {"IN": ["is", "in", "my", "the"]}, "OP": "*"}, {"ENT_TYPE": "FILE_NAME"}]],
    "make_file": [[{"LOWER": "make"}, {"LOWER": {"IN": ["new", "me", "to", "call"]}, "OP": "*"}, {"ENT_TYPE": "FILE_NAME"}, {"ENT_TYPE": "SECOND_INPUT", "OP": "*"}]],
    "add_to_file": [[{"LOWER": "add"}, {"ENT_TYPE": "SECOND_INPUT", "OP": "*"}, {"IS_ASCII": True, "OP": "+"}, {"LOWER": {"IN": ["to", "the"]}, "OP": "*"}, {"ENT_TYPE": "FILE_NAME"}]],
    "delete_from_file": [[{"LOWER": {"IN": ["delete", "remove"]}}, {"ENT_TYPE": "SECOND_INPUT", "OP": "*"}, {"LOWER": "from"}, {"ENT_TYPE": "FILE_NAME"}]]
}
# add all the patterns to the matcher
for k, v in patterns.items():
    matcher.add(k, v)


def marge(a, b, func=lambda s: s):
    marged = []
    pa = 0
    pb = 0
    all_len = len(a) + len(b)
    while len(marged) < all_len:
        if pa == len(a):
            marged.extend(b[pb:])
            break
        if pb == len(b):
            marged.extend(a[pa:])
            break
        if func(a[pa]) > func(b[pb]):
            marged.append(b[pb])
            pb += 1
        elif func(a[pa]) < func(b[pb]):
            marged.append(a[pa])
            pa += 1
        else:
            marged.append(a[pa])
            marged.append(b[pb])
            pa += 1
            pb += 1
    return marged


def delete_file(filename):
    if filename[-4:] != ".csv":
        filename = f"{filename}.csv"
    if os.path.exists(filename):
        confirm = input(f"Are you sure you want to delete '{filename}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            try:
                os.remove(filename)
                return f"File '{filename.replace(".csv", "")}' has been deleted."
            except Exception as e:
                return f"Sorry, I couldn't delete {filename}. Error: {str(e)}"
        else:
            return "Deletion canceled."
    else:
        return f"File '{filename}' not found."


def make_file(filename,fieldnames=None):
    if os.path.exists(filename):
        return f"File '{filename}' already exists."
    f = CsvManger.make_file(filename, fieldnames)
    return f"file '{filename.replace(".csv", "")}' created with fields: {', '.join(f.fieldnames())}"


# Function to classify user input and extract filename
def classify(sentence):
    doc = nlp(sentence.lower())
    matches = matcher(doc)
    if matches:
        match_id, start, end = matches[0]
        filename = next((ent.text for ent in doc.ents if ent.label_ == "FILE_NAME"), None)
        second_input = next((ent.text for ent in doc.ents if ent.label_ == "SECOND_INPUT"), None)
        func = nlp.vocab.strings[match_id]
        if second_input:
            return func, [filename, second_input]
        return func, filename
    if "help" in sentence:
        return "help", None
    if "hello" in sentence or "hi" in sentence:
        return "greeting", None
    if "bye" in sentence or "goodbye" in sentence:
        return "farewell", None

    return "fallback", None


def chatbot_response(user_input: str):
    doc = nlp(user_input)
    # response for help, hallo, bye and any thing unknown
    responses = {
        "greeting": ["Hello!", "Hi there!", "Hey! How can I assist you?"],
        "farewell": ["Goodbye!", "See you later!", "Take care!"],
        "help": [
            "Here's what I can help you with:\n"
            "- 📂 Open or view a file: say things like 'open test file', 'show me the groceries list', or 'what is in budget file'\n"
            "- ➕ Add to a file: e.g., 'add Food, 10, 2024-04-10 to expenses list'\n"
            "- 🗑️ Delete from a file: e.g., 'delete Amount > 50 from groceries file'\n"
            "- ❌ Delete an entire file: e.g., 'delete budget file' or 'remove savings list'\n"
            "- 🆕 Make a new file: e.g., 'make a new groceries list', 'make me a file called expenses file'\n"
            "- 💬 Type 'help' anytime to see this again."
        ],
        "fallback": [
            "Sorry, I didn't understand that. Type 'help' to see what I can do.",
            "Hmm, that doesn't look like a command I know. Try 'help' for a list of options.",
            "I'm only able to work with CSV files. Need help? Just type 'help'.",
            "I couldn't figure out what you meant. Maybe check 'help' to see the available commands.",
            "Oops! That doesn't match any CSV operation I can handle. Try 'help'."
        ]
    }
    responses_list = []
    # {what the matcher return: the function} all the chatbot functions
    command_functions = {"open_file": CsvManger.make_show, "delete_file": delete_file,
                         "make_file": make_file, "add_to_file": add_to_file, "delete_from_file": delete_from_file}
    sentences = user_input.split(" then ")
    for sentence in sentences:
        category, inputs = classify(sentence)

        if category in command_functions:  # Check if the command exists in the dictionary
            if isinstance(inputs, list):
                if category != "make_file":
                    try:
                        f = CsvManger(inputs[0])
                    except Exception as e:
                        responses_list.append(e)
                        continue
                responses_list.append(command_functions[category](inputs[0], inputs[1]))
            else:
                if category != "make_file":
                    try:
                        f = CsvManger(inputs)
                    except ValueError:
                        responses_list.append(f"The file '{inputs}' doesn't exist. Please check the name or create it first using 'make new {inputs}'.")
                        continue
                responses_list.append(command_functions[category](inputs))
        elif category in responses:  # Handle predefined responses (greeting, farewell, etc.)
            responses_list.append(random.choice(responses[category]))

    return "\n".join(responses_list)


def add_to_file(filename, to_add_input=None):
    f = CsvManger(filename)
    fieldnames = f.fieldnames()
    to_add = {}
    final_add = []
    if to_add_input:
        adds = re.sub("('|\")", "", to_add_input).split(",")
        adds = [value.strip() for value in adds]
        if len(adds) != len(fieldnames):
            return f"Error: You provided {len(adds)} values, but the file expects {len(fieldnames)} fields: {fildnames}  (use '.' for empty valuse)."
        to_add = {fieldnames[i]: adds[i] if adds[i] != '.' else "" for i in range(len(fieldnames))}
        f.add_rows([to_add])
        return f"Success! {to_add} has been added to {filename.replace(".csv", "")}"
    # add the thing user want to dict
    print(f"Enter values for {', '.join(fieldnames)}:")
    for field in fieldnames:
        to_add[field] = list(map(lambda s: s.strip(), input(
            f"Enter values for '{field}' (separate multiple values with commas): ").split(",")))

        if len(to_add[field]) != len(to_add[fieldnames[0]]):
            return "Error: All fields must have the same number of values. Please enter the same number of values for each field.(use '.' for empty values)"

    for i in range(len(to_add[fieldnames[0]])):
        # for key, value in to_add.items()
        item = {key: value[i] if value[i] != '.' else "" for key, value in to_add.items()}
        final_add.append(item)

    f.add_rows(final_add)
    return f"Success! {len(to_add[fieldnames[0]])} new entries have been added to '{filename}'."


def delete_from_file(filename: str, to_delete: str = None):
    f = CsvManger(filename)
    if not f.data():
        return f"no data found in {filename.replace(".csv", "")}"
    if to_delete:
        try:
            filtered_data = f.filtering(to_delete)
        except Exception as e:
            return e
        if len(filtered_data) == 0:
            return f"No rows in {filename} where {to_delete.replace(",", " and ")}"
        f.delete_from_file(filtered_data)
        return f"{len(filtered_data)} has been deleted form {filename}"

    print(f.show_data("Current data in file:"))

    row_numbers = input(
        "Enter row number to delete(separate multiple values with commas): ").split(",")
    success_n = []
    success_r = []
    data = f.data()
    for n in row_numbers:
        n = n.strip()
        if n.isdigit():
            if int(n) > 0 and int(n) - 1 < len(data):
                success_r.append(data[int(n)-1])
                success_n.append(n)
    f.delete_from_file(success_r)

    return f"Row {",".join(success_n)} deleted from '{f.filename.replace(".csv", "")}'."


if __name__ == "__main__":
    main()
