# G (Mini-J)

## Table of Contents

1. [Description](#description)  
2. [Setup Instructions](#setup-instructions)  
3. [How to Run the Project](#how-to-run-the-project)  
   1. [Interactive Mode](#interactive-mode)  
   2. [Evaluating a File](#evaluating-a-file)  
   3. [Running Automated Tests](#running-automated-tests)  
4. [Implementation Decisions](#implementation-decisions)  
5. [Implemented Functions and Operators](#implemented-functions-and-operators)  
   1. [Basic Features](#basic-features)  
   2. [Mandatory Features](#mandatory-features)  
   3. [Additional Features](#additional-features)
6. [Project Files](#project-files)  
7. [Test Coverage](#test-coverage)

---

## Description

This project implements an interpreter for **G**, a minimal subset of the **J** programming language. G retains the functional and array-oriented nature of J, with a focus on high-level list operations. Its key features are:

- **Basic types**:
  - Scalar signed integers (e.g., `42`, `_7`)
  - Lists of integers (e.g., `1 2 3 4`)
- **Functional paradigm**:
  - No mutable variables: values are bound immutably to names.
  - Functions are first-class citizens.
  - Expressions are evaluated using functional composition and list-based operations.

This interpreter covers the essential elements to allow evaluating expressions, defining functions and applying basic operators on lists.

In this `README`, you will find design decisions, descriptions of available features, and practical examples. Since this was developed as an assignment of a university subjetct, it mentiones "mandatory" and "additional" features, according to the work's original requirements.

---

## Setup Instructions

### 1. Prerequisites

To run the **G** interpreter, make sure you have the following installed:

- **Python 3** (version 3.6 or higher)
- **ANTLR4** (for generating the parser and lexer)

<details>
<summary><strong>Installing Python 3</strong></summary>

#### On Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### On Windows
1. Download Python from https://www.python.org/downloads/windows/
2. Check "Add Python to PATH" during installation.
3. Verify:
```cmd
python --version
```
</details>

<details>
<summary><strong>Installing ANTLR4</strong></summary>

#### On Linux (Ubuntu/Debian)
1. Ensure Java is installed:
```bash
sudo apt update
sudo apt install default-jdk
```
2. Download and set up ANTLR:
```bash
wget https://www.antlr.org/download/antlr-4.12.0-complete.jar -O antlr-4.12.0-complete.jar
sudo mv antlr-4.12.0-complete.jar /usr/local/lib/
echo 'export CLASSPATH=".:/usr/local/lib/antlr-4.12.0-complete.jar:$CLASSPATH"' >> ~/.bashrc
echo 'alias antlr4="java -jar /usr/local/lib/antlr-4.12.0-complete.jar"' >> ~/.bashrc
echo 'alias grun="java org.antlr.v4.gui.TestRig"' >> ~/.bashrc
source ~/.bashrc
```
3. Verify:
```bash
antlr4 --version
```

#### On Windows
See: https://github.com/antlr/antlr4-tools
</details>

### 2. Install Python Dependencies

```bash
pip install antlr4-python3-runtime
```

### 3. Generate Parser and Lexer

```bash
make
```
Or alternatively:

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor g.g4
```
---

## How to Run the Project

The main interpreter script is `g.py`. Below are the ways to use it.

### Interactive Mode

To start the interpreter in interactive mode (reading line by line from the console):

```bash
python3 g.py
```

The prompt will display:

```
>
```

### Evaluating a Code File

If you have a file with extension `.j` containing G code, you can pass it as an argument:

```bash
python3 g.py program.j
```
You can easily redirect your output to a file `file.out` executing:

```bash
python3 g.py program.j > file.out
```

### Running Automated Tests

`tests/` directory contains sample `.j` files with their corresponding `.out` files. To run them all automatically, you can run:

```bash
python3 tests.py
```

`tests.py` will iterate over each `.j` file in `tests/`, run `g.py` internally, and compare the output to the `.out` file. The script will inform you if the test successes or fails and, in case it fails, where has failed.

---

## Implementation Decisions

Below are the main design decisions made during the development of the interpreter:

1. **Memory Representation**  
   - **Context**: since it is a functional language, in J (and therefore in G) there is no global mutable state. Users can bind names to values or functions.  
   - **Decision**: Use a **Python dictionary (**`dict`**)** where:
     - **Key**: variable or function name (string).
     - **Value**: the associated content — an integer, a list of integers, or a structure representing a function.  
   - **Rationale**:  
     - Fast lookups and updates (`O(1)` average).
     - No need for a stack of scopes since G does not support nested scopes for function definitions.

2. **Mapping Operators to Python Actions**  
   - **Context**: J defines operators which apply element-wise to lists (broadcasting).  
   - **Decision**: Create Python dictionaries (`bin_op_map` and `un_op_map`) where:
     - **Key**: operator symbol (e.g., `'+', '-', '*'`).
     - **Value**: a Python function (lambda or named function) that takes processed operands and returns the result.  
   - **Rationale**:  
     - Makes adding new operators straightforward — just register a new key-value pair.
     - Using callables avoids long `if-elif` chains.

3. **Representing Functions Defined by the User**  
   - **Context**: In J, functions are first-class; they can be assigned to names, passed as arguments, etc.  
   - **Decision**: When the user defines a function, store a **tuple of three elements** in the dictionary:
     1. A string tag (`"function"`) to identify the value as a function.
     2. The **Python object** implementing the function’s behavior (e.g. a lambda function).
     3. The **original source text** written in G, so that if the user queries the function’s value, the interpreter can show the G code.  
   - **Rationale**:  
     - Storing the source text allows printing the original G definition when requested.
     - The tag string simplifies runtime checks (list vs. scalar vs. function).

4. **Using NumPy for List Operations**
   - **Context**: since G's main type are lists, the interpreter will have to internally treat them constantly. This element-wise behavior is fundamental to the language’s design.
   - **Decision**: Internally represent lists as NumPy arrays instead of plain Python lists.
   - **Rationale**:
     - NumPy naturally supports broadcasting of operations between arrays and scalars (or between arrays of the same shape), aligning perfectly with G's semantics.
     - Leveraging NumPy allows most arithmetic and comparison operations to be written as direct expressions, without the need for custom iteration logic, boosting code simplicity and conciseness.
     - NumPy operations are implemented in C and are significantly faster than looping manually over Python lists.

---

## Implemented Functions and Operators

### Basic Features

- **Base Type**:  
  - **List of integers**: represented as numpy arrays. Example in G:  
    ```j
    1 2 3 4 5
    ```
  - **Scalar integer**: written as `_2` for –2 (following J’s notation).

- **Arithmetic Operators** (all at the same precedence level with right-associative behavior):
  - `+` (addition)
  - `-` (subtraction)
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
  5 * 6 + _2          NB. 20 (not 28)
  1 2 3 + 4           NB. 5 6 7
  1 2 3 + 4 5 6       NB. 5 7 9
  1 2 3 + 4 5         NB. length error
  ```

- **Relational Operators** 
  - `>`   (greater than)
  - `<`   (less than)
  - `>=`  (greater than or equal)
  - `<=`  (less than or equal)
  - `<>`  (not equal)
  - `=`   (equal)

  The output of a relational operator is `1` (true) or `0` (false).

  **Examples**:
  ```j
  1 2 3 > 2     NB. 0 0 1
  4 < 5 3 2     NB. 1 0 0
  3 = 3 4 3     NB. 1 0 1
  ```

### Mandatory Features

1. **Assignment of Scalars and Lists to Variables**  
   - Use `=:` to assign scalar values or lists to variables. Scalars are internally treated as single-element lists.  
     **Examples**:  
     ```
     a =: 5
     b =: 1 2 3
     ```

2. **Function Declaration and Calling**  
   - Declare functions by assigning operators to variables:  
     ```
     square =: *:
     ```  
   - Once declared, functions can be called by applying them to arguments.  
     **Example**:  
     ```
     square 3     NB. 9
     ```

3. **Printing Variables**  
   - Variables can be printed to display their values (scalars and lists) or definitions (functions).  
     **Example**:  
     ```
     a            NB. 5
     square       NB. *:
     ```

4. **List Generation**  
   - `i. n`: Generates a list from `0` to `n-1`.  
     **Example**:  
     ```
     i. 5         NB. 0 1 2 3 4
     ```

5. **Fold (**`/`**)**  
   - The `fold` operator (`/`) applies a **binary operator** accumulatively to the elements of a list, from left to right.  
     **Example**:  
     ```
     +/ 1 2 3 4   NB. 10
     ```

6. **Operators**  
   - **Binary Operators**:  
     - Arithmetic: `+`, `-`, `*`, `%`, `|`, `^`  
     - Relational: `>`, `<`, `<>`, `=`, `<=`, `>=`  
     - Concatenation: `,`  
     - Indexing: `{`  
   - **Unary Operators**:  
     - Identity: `]`  
   - **Modifiers**:  
     - `:` : Transforms a binary operator into a unary one.  
     - `~` : Reverses the operand order of a binary operator.  

     **Examples**:  
     ```
     +: 4              NB. 8 (equivalent to 4 + 4)
     3 -~ 4            NB. 1 (equivalent to 4 - 3)
     ```

    - **Special Operator**:  
       - `#` : Can be unary or binary depending on context.
         + If unary: returns the length of a list
         + If binary: replicates the right operand attending the left operand.
         + If unary and followed by `~`, it becomes binary generating the missing operand refexively (copies the existing one).

      **Examples**:  
      ```
       # 1 2 3         NB. 3 (unary, returns length of list)
       1 0 1 # 1 2 3   NB. 1 3 (binary, selects elements where left argument is 1)
       1 0 2 # 1 2 3   NB. 1 3 3 (binary, replicates elements)
       #~ 1 2 3        NB. 1 2 2 3 3 3 (unary to binary)
       ```

7. **Function Composition (**`@:`**)**  
   - The operator `@:` composes two functions, applying the right function first, then the left one.  
     **Example**:  
     ```
     double =: +:
     square =: *:
     f =: double @: square

     f 3    NB. 18
     ```

### Additional Features

In addition to all the mandatory features, the following J-inspired features are implemented in **G**:

1. **Boolean Operators**  
   - `+.` (logical OR)  
   - `*.` (logical AND)  
   - `-.` (logical NOT)

   These operate element-wise on lists of `0`/`1` or between scalars `0`/`1`.  
   **Example**:
     ```
     0 +. 1            NB. 1
     1 0 1 *. 1 1 0    NB. 1 0 0
     -. 0 0 1 0        NB. 1 1 0 1
     ```

2. **Take (**`{.`**) and Drop (**`}.`**)**  
   - `{.` (take) returns the first `n` elements of a list (if `n` is larger than its length, it completes with `0`'s).  
   - `}.` (drop) discards the first `n` elements and returns the remainder.  
   
   **Examples**:  
     ```
     3 {. 1 2 3 4 5     NB. 1 2 3
     2 }. 10 20 30 40   NB. 30 40
     ```

3. **Membership (**`e.`**)**  
   - The operator `e.` checks whether each element of the left-hand list belongs to the right-hand list, returning a list of `1`/`0` (boolean) for each element on the left.  
   
   **Example**:  
     ```
     1 3 6 e. 1 2 3 4 5   NB. 1 1 0
     ```

4. **Symmetric List Generation (**`i: n`**)**  
   - `i: n`: Generates a list from `-n` to `n`.  
   
   **Example**:  
     ```
     i: 2             NB. _2 _1 0 1 2
     ```

5. **Absolute value (**`|`**)**
    - Unary operator `|` operates element-wise on lists or on scalars generating their absolute value.

    **Example**:
    ```
    | 0 _1 1 _2 2    NB. 0 1 1 2 2
    ```

6. **Reverse (**`|.`**)**
    - `|.` returns its reversed argument.

    **Example**:
    ```
    |. 30 20 10      NB. 10 20 30
    ```

7. **Increment (**`>:`**) and Decrement (**`<:`**)**
   - `>:` (increment) increases element-wise in one unit its argument.  
   - `<:` (decrement) decreases element-wise in one unit its argument.   
   
   **Examples**:  
     ```
     >: 1 2 3         NB. 2 3 4
     <: 1 2 3         NB. 0 1 2
     ```

8. **Scan (**`\`**)**

   - `\` receives an operator and executes it along all the list returning another list woth the accumulated intermediate results.

    **Examples**:  
     ```
     +\ 1 2 3 4       NB. 1 3 6 10
     *\ 1 2 3 4       NB. 1 2 6 24
     ```

---

## Project Files

- `g.g4`: Defines the complete grammar for G.  

- `g.py`: main script that manages console or file input and calls `ExecVisitor.py` delegating the work.

- `ExecVisitor.py`: gVisitor extension that executes the G statements.

- `tests.py`: iterates over each `.j` file in `tests/`, runs `g.py` internally, and compares the output to the corresponding `.out` file. Prints a report of passed/failed tests.  

- `tests/`: contains sample test cases for verifying all implemented features. Each `.j` file is paired with a `.out` file.

---

## Test Coverage

The project includes a suite of tests to the above mentioned features. The tests are organized into the files:

- `0-dummy.j`: covers basic expressions and syntax including:  
  - Arithmetic operators: `+`, `-`, `*`, `%`, `|`, `^`  
  - Relational operators: `<`, `>`, `<=`, `>=`, `<>`, `=`  
  - Identity operator: `]`  
  - Variable assignment and access  
  - Function declaration, access, and invocation  

- `1-operators.j`: focuses on mandatory operators and modifiers:  
  - Flip: `~`  
  - Binary to unary modifier: `:`  
  - Indexed access: `{`  
  - Concatenation: `,`  
  - Generator: `i.`  
  - Fold: `/`  
  - Binary and unary usage of `#`  
  - Function composition: `@:`  

- `2-extra.j`: tests additional features and utilities:  
  - Boolean operators: `*.`, `+.` , `-.`  
  - Membership: `e.`  
  - Take and drop: `}.`, `{.`  
  - Scan: `\`
  - Increment and decrement: `<:`, `>:`  
  - Reverse: `|.`  
  - Absolute value: `|`  
  - Integer generator: `i:`

- `3-lists.j`: tests multiple operations on lists.

-  `4-financial.j`: computes useful data about financial transactions.

- `5-physics.j`: computes the acceleration, velocity and position of a moving body in a certain moment in time.
