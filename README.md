# G (Mini-J)

## Table of Contents

1. [Description](#description)  
2. [Requirements and Dependencies](#requirements-and-dependencies)  
   1. [Installing ANTLR4](#installing-antlr4)  
   2. [Installing Python 3](#installing-python-3)  
3. [Installation](#installation)  
4. [How to Run the Project](#how-to-run-the-project)  
   1. [Interactive Mode](#interactive-mode)  
   2. [Evaluating a File](#evaluating-a-file)  
   3. [Running Automated Tests](#running-automated-tests)  
5. [Detailed Description](#detailed-description)  
6. [Implementation Decisions](#implementation-decisions)  
7. [Implemented Functions and Operators](#implemented-functions-and-operators)  
   1. [Basic Operations](#basic-operations)  
   2. [Relational Operators](#relational-operators)  
8. [Additional Features](#additional-features)  
9. [Project Structure](#project-structure)  
10. [Usage Examples](#usage-examples)   

---

## Description

This project implements an interpreter for **G**, a subset of the **J** programming language. G inherits J’s functional, array-oriented design and focuses on high-level list operations.  

In this `README`, you will find design decisions, descriptions of available features, and practical examples.

---

## Requirements and Dependencies

To run the **G** interpreter, you need:

- **Python 3** (version 3.6 or higher)  
- **ANTLR4** (to generate the parser and lexer from the grammar)

### Installing ANTLR4

#### On Linux (Ubuntu/Debian)
1. Make sure you have Java installed (required by ANTLR4):
   ```bash
   sudo apt update
   sudo apt install default-jdk
   ```
2. Download the ANTLR4 JAR (latest version at the time of writing):
   ```bash
   wget https://www.antlr.org/download/antlr-4.12.0-complete.jar -O antlr-4.12.0-complete.jar
   ```
3. Move the JAR to a standard location and configure environment variables:
   ```bash
   sudo mv antlr-4.12.0-complete.jar /usr/local/lib/
   echo 'export CLASSPATH=".:/usr/local/lib/antlr-4.12.0-complete.jar:$CLASSPATH"' >> ~/.bashrc
   echo 'alias antlr4="java -jar /usr/local/lib/antlr-4.12.0-complete.jar"' >> ~/.bashrc
   echo 'alias grun="java org.antlr.v4.gui.TestRig"' >> ~/.bashrc
   source ~/.bashrc
   ```
4. Verify the installation:
   ```bash
   antlr4 --version
   ```
   You should see output similar to:
   ```
   ANTLR Parser Generator 4.12.0
   ```

#### On Windows
1. Download the ANTLR4 JAR from the [official page](https://www.antlr.org/download.html).  
2. Place `antlr-4.12.0-complete.jar` (or whatever version you downloaded) in a folder, for example:  
   ```
   C:antlr-4.12.0-complete.jar
   ```
3. Add the path to your environment variables:
   - Open **Control Panel → System and Security → System → Advanced system settings → Environment Variables**.
   - Under “System variables,” locate (or create) **CLASSPATH** and add:  
     ```
     .;C:antlr-4.12.0-complete.jar
     ```
   - Create a new user variable **ANTLR4_HOME** with value:  
     ```
     C:antlr
     ```
   - Edit the **Path** variable and add:  
     ```
     %ANTLR4_HOME%antlr-4.12.0-complete.jar
     ```
4. Open a Command Prompt and verify:
   ```cmd
   java -jar %ANTLR4_HOME%antlr-4.12.0-complete.jar
   ```
   If it prints the ANTLR help message, the installation was successful.

### Installing Python 3

#### On Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### On Windows
1. Download the Python 3 installer from https://www.python.org/downloads/windows/.  
2. Run the installer and check “Add Python to PATH” before finishing.  
3. Verify in a Command Prompt:
   ```cmd
   python --version
   ```
   You should see something like:
   ```
   Python 3.10.4
   ```

---

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/rboxvelasco/g-mini-j.git
   cd g-mini-j
   ```

2. Generate the parser and lexer files with ANTLR4 (make sure you’re in the project root where `G.g4` is located):
   ```bash
   antlr4 -Dlanguage=Python3 G.g4 -o gen
   ```
   This will create a `gen/` directory containing the ANTLR4-generated modules (`GParser.py`, `GLexer.py`, `GListener.py`, etc.).

3. (Optional) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scriptsctivate
   ```

4. Install the required Python packages (if there are additional dependencies, list them in `requirements.txt` and run):
   ```bash
   pip install -r requirements.txt
   ```
   For this project, you primarily need the ANTLR4 runtime:
   ```bash
   pip install antlr4-python3-runtime
   ```

---

## How to Run the Project

The main interpreter script is `g.py`. Below are the ways to use it.

### Interactive Mode

To start the interpreter in interactive mode (reading line by line from the console):

```bash
python3 g.py
```

- The prompt will display:
  ```
  >
  ```
- You can type G expressions directly and results will be shown, for example:
  ```text
  > 1 2 3 + 4 5 6
  5 7 9
  > x =: 10
  > x * 2
  20
  ```
- To exit interactive mode, press `Ctrl+D` or `Ctrl+C`.

### Evaluating a Code File

If you have a file with extension `.j` containing G code, you can pass it as an argument:

```bash
python3 g.py program.j
```

- The interpreter will read and execute each statement in the file, printing results as needed.
- Example `program.j`:
  ```j
  x =: 1 2 3 4 5
  y =: 5 + x
  y
  ```
  Running:
  ```bash
  python3 g.py program.j
  ```
  Output:
  ```
  6 7 8 9 10
  ```
You can easily redirect your output to a file `file.out` executing:
```bash
python3 g.py program.j > file.out
```

### Running Automated Tests

`tests/` directory contains sample `.j` files with their corresponding `.out` files. To run all tests automatically. To test them all automatically, you can run:

```bash
python3 tests.py
```

- `tests.py` will iterate over each `.j` file in `tests/`, run `g.py` internally, and compare the output to the `.out` file.
- The script will inform you if the test successes or fails and, in case it fails, where has failed.

---

## Detailed Description

The **G** language is a reduced subset of **J** that focuses on:

- **Basic types**: lists of integers (`1 2 3 4`) and scalar integers (signed).
- **Arithemetic and relational operations**: similar to J but with simpler syntax.  
- **Functional paradigm**: there are no traditional mutable assignments; variables bind to values (lists, scalars, or functions).  

This project covers the essential elements to allow evaluating expressions, defining anonymous functions, and applying basic operators on lists.

---

## Implementation Decisions

Below are the main design decisions made during the development of the interpreter:

1. **Memory Representation**  
   - **Context**: In J (and therefore in G), there is no global mutable state in the imperative sense. Users can bind names to values or functions.  
   - **Decision**: Use a **Python dictionary (`dict`)** where:
     - **Key**: variable or function name (string).
     - **Value**: the associated content—an integer, a list of integers, or a structure representing a function.  
   - **Rationale**:  
     - Fast lookups and updates (`O(1)` average).
     - No need for a stack of scopes since G does not support nested scopes for function definitions.

2. **Mapping Operators to Python Actions**  
   - **Context**: J defines operators which apply element-wise to lists (broadcasting).  
   - **Decision**: Create a Python dictionary (`op_map`) where:
     - **Key**: operator symbol (e.g., `'+', '-', '*'`).
     - **Value**: a Python function (lambda or named function) that takes processed operands and returns the result (list or scalar).  
   - **Rationale**:  
     - Makes adding new operators straightforward—just register a new key-value pair.
     - Using callables avoids long `if-elif` chains.

3. **Representing Functions Defined by the User**  
   - **Context**: In J, functions are first-class; they can be assigned to names, passed as arguments, etc.  
   - **Decision**: When the user defines a function (e.g., `f =: { x . x * x }`), store a **tuple of three elements** in the dictionary:
     1. A string tag (e.g., `"function"`) to identify the value as a function.
     2. The **Python object** implementing the function’s behavior (e.g., a lambda or class instance).
     3. The **original source text** written in G, so that if the user queries the function’s value, the interpreter can show the G code.  
   - **Rationale**:  
     - Storing the source text allows printing the original G definition when requested.
     - The tag string simplifies runtime checks (list vs. scalar vs. function).

4. **Eager vs. Lazy Evaluation**  
   - **Context**: J can support lazy evaluation for certain constructs, but G is simplified.  
   - **Decision**: Implement **eager evaluation** (evaluate every subexpression as soon as it’s parsed).  
   - **Rationale**:  
     - Simplifies the interpreter’s logic.
     - In this educational context, users do not significantly benefit from lazy evaluation.

---

## Implemented Functions and Operators

### Basic Operations

- **Base Type**:  
  - **List of integers**: represented as numpy arrays. Example in G:  
    ```j
    1 2 3 4 5
    ```
  - **Scalar integer**: written as `_2` for –2 (following J’s notation). Example:
      ```j
    _2 + 5 * 6       NB. result: 28
    (_2 + 5) * 6     NB. result: 18
    5 * 6 + _2       NB. result: 4
    ```
- **Element-wise Operators** (all at the same precedence level with right-associative behavior):
  - `+` (addition)
  - `-` (subtraction or negation if unary; context determined by the parser)
  - `*` (multiplication)
  - `%` (division)
  - `|` (remainder)
  - `^` (power)

  The operator applies with broadcasting rules:
  - If both operands are scalars, return a scalar.
  - If one is a list and the other is a scalar, apply the scalar to each element of the list.
  - If both are lists, they must be of the same length; apply element-wise.

  **Examples**:
  ```j
  3 + 4               NB. 7
  1 2 3 + 4           NB. 5 6 7
  1 2 3 + 4 5 6       NB. 5 7 9
  1 2 3 + 4 5         NB. length error
  ```

### Relational Operators

- `>`   (greater than)
- `<`   (less than)
- `>=`  (greater than or equal)
- `<=`  (less than or equal)
- `<>`  (not equal)
- `=`   (equal)

The output of a relational operator on scalars is `1` (true) or `0` (false). When applied to lists, it returns a list of `1` and `0` for each element-wise comparison.

**Example**:
```j
1 2 3 > 2     NB. 0 0 1
4 < 5 3 2     NB. 1 0 0 0
3 = 3 4 3     NB. 1 0 1
```

---

## Additional Features

In addition to basic and relational operators, the following J-inspired functions/operators are implemented in **G**:

1. **Boolean Operators**  
   - `*.` (logical AND).  
   - `+.` (logical OR).  
   These operate on lists of `0`/`1` of the same length or between scalars `0`/`1`.  
   **Example**:
   ```j
   0 +. 1            NB. 1
   1 0 1 *. 1 1 0    NB. 1 0 0
   ```

2. **Take (`{.`) and Drop (`}.`)**  
   - `{.` (take) returns the first `n` elements of a list.  
   - `}.` (drop) discards the first `n` elements and returns the remainder.  
   - **Syntax**: `n {. L` or `n }. L`.  
   **Examples**:
   ```j
   3 {. 1 2 3 4 5     NB. 1 2 3
   2 }. 10 20 30 40   NB. 30 40
   ```

3. **Membership (`e.`)**  
   - The operator `e.` checks whether each element of the left-hand list belongs to the right-hand list, returning a list of `1`/`0` (boolean) for each element on the left.  
   **Example**:
   ```j
   1 3 6 e. 1 2 3 4 5   NB. 1 1 0
   ```

4. **Function Assignment**  
   - You can assign an anonymous function to a name using the syntax:  
     ```j
     f =: { x . EXPRESSION using x }
     ```
   - Once assigned, `f` can be applied as:
     ```j
     f 10   NB. result of EXPRESSION with x=10
     ```

---

## Project Structure

```
g-mini-j/
├── g.g4                # ANTLR4 grammar for G
├── gen/                # ANTLR4-generated code (parser, lexer, listener)
│   ├── gParser.py
│   ├── gLexer.py
│   ├── gListener.py
│   └── ...
├── g.py                # Main interpreter script
├── tests.py            # Script to run automated tests
├── requirements.txt    # Python dependencies (e.g., antlr4-python3-runtime)
├── README.md           # This document (in English)
└── tests/              # Folder with .j files and their .out reference outputs
    ├── case1.j
    ├── case1.out
    ├── case2.j
    ├── case2.out
    └── ...
```

- **`g.g4`**: Defines the complete grammar for G (productions for expressions, assignments, functions, operators, etc.).  
- **`gen/`**: Contains the ANTLR4-generated modules from `g.g4`. Do not edit these files manually.  
- **`g.py`**:  
  - Contains the logic for user interaction (console or file input), parser creation, listener/evaluator, and result printing.  
  - Manages the variable dictionary (memory) and resolves functions and operators.  
- **`tests.py`**:  
  - Iterates over each `.j` file in `tests/`, runs `g.py` internally, and compares the output to the corresponding `.out` file.  
  - Prints a report of passed/failed tests.  
- **`tests/`**:  
  - Contains sample test cases for verifying all implemented features. Each `.j` file is paired with a `.out` file.

---

## Usage Examples

Below are practical examples to illustrate the interpreter’s behavior:

1. **Adding Two Lists of Equal Length**  
   ```bash
   $ python3 g.py
   > 1 2 3 + 4 5 6
   5 7 9
   >
   ```
2. **Operations with Negative Scalars**  
   ```bash
   $ python3 g.py
   > _2 + 5 * 6
   28
   > (_2 + 5) * 6
   18
   > 5 * 6 + _2
   4
   ```
3. **Relational and Boolean Operations**  
   ```bash
   $ python3 g.py
   > 1 2 3 > 2
   0 0 1
   > 1 0 1 *. 1 1 0
   1 0 0
   > 3 = 3 4 3
   1 0 1
   ```
4. **Take and Drop**  
   ```bash
   $ python3 g.py
   > 3 {. 10 20 30 40 50
   10 20 30
   > 2 }. 10 20 30 40 50
   30 40 50
   ```
5. **Membership**  
   ```bash
   $ python3 g.py
   > 1 3 5 e. 1 2 3 4 5
   1 0 1 0 1
   ```
6. **Defining and Using a Function**  
   ```bash
   $ python3 g.py
   > square =: { x . x * x }
   > square 5
   25
   > square 1 2 3 4
   1 4 9 16
   ```
7. **Running a File**  
   Suppose `routine.j` contains:
   ```j
   nums = 1 2 3 4 5
   res = 2 * nums + 3
   res
   ```
   Run:
   ```bash
   $ python3 g.py routine.j
   5 7 9 11 13
   ```
8. **Running Automated Tests**  
   ```bash
   $ python3 tests.py
   Test case1.j: OK
   Test case2.j: ERROR (expected "3 4 5", got "3 4 6")
   ...
   ```

---