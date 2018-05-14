# Technical Test Insideboard: Tax-computation

### Version

| Version | Description | Author |
| ------- | ----------- | ------ |
| 1.0.0     | Tax computation from a given file | Brice Leclercq |


## Project Structure

### Root Folder

Folders:

* `tax-computation` - The program implementation is here
* `tests` - [Pytest](https://docs.pytest.org/en/latest/) test for program

Files:

* `README.md` - The project's README
* `requirements.txt` - Module needed by python in order to get this program works

### Program Structure
```
tax_computation/
|--- __init__.py => source file
|--- files       => folder where you need to put your test files
     |--- test1.txt
     |--- test2.txt
     |--- test3.txt
     |--- test4.txt
     |--- test_specials.txt
|--- specials    => 
     |--- book.txt
     |--- food.txt
     |--- medication.txt
```

### Tests Structure
```
tests/
|--- __init__.py
|--- test_inputs.py
|--- files
     |--- test1.txt
     |--- test2.txt
     |--- test3.txt
     |--- test4.txt
     |--- test_specials.txt
|--- specials
     |--- book.txt
     |--- food.txt
     |--- medication.txt
```

## Dependencies

### Project Dependencies 

* [Python](https://www.python.org/downloads/) 3.5 >=
* [Pytest](https://docs.pytest.org/en/latest/) 3.0.7 >=

## Installation

##### Clone the project
`$ git clone https://ladresse_sur_github.com`

##### Setting up the environment

`cd [your_folder_name]/tax_computation`

You really SHOULD use a virtual environment using python3.5

(virtualenv MUST be installed)[french guide for it's installation](http://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html)

`virtualenv --python=/usr/bin/python3.5 .venv`

And

`source .venv/bin/activate`

Then

`pip install -r requirements.txt`

## Usage

### Launch tax_computation

`cd [your_folder_name]/tax_computation`

`(.venv)$ python3 __init__.py files/[file_name].txt` (Will launch the program with the given file parameter)

### Launch tests

`cd [your_folder_name]/tests`

`(.venv)$ python3 -m pytest` (Will launch all the tests)
