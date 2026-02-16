# All CS50x Projects
A collection of programming projects developed during [CS50x: Introduction to Computer Science](https://www.edx.org/learn/computer-science/harvard-university-cs50-s-introduction-to-computer-science)

## Description
This repository contains the projects developed during Harvard University's CS50x: Introduction to Computer Science. The projects cover core computer science concepts, including algorithms, data structures, memory management, and web development, using languages such as C and Python.

**Note:** Some C programs rely on the CS50 Library, which is provided in the CS50 development environment and is not available by default on other systems. If so, they will not run properly.

## Technologies Used Across Projects
- ![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
- ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## Dependencies
- Flask
- Flask-Session
- cs50
- Werkzeug
- requests

## How to Run
> The following commands assume a Unix-like environment (Bash).

### C Programs
**Note:** Some C programs rely on the CS50 Library (`cs50.h`). These programs require either the CS50 development environment or a manual installation of the library to run properly.

1. Make sure you have a C compiler installed (e.g., gcc).

2. Install the CS50 Library, if the program requires it.
   (Ubuntu guide — Installation instructions for other systems are available [here](https://cs50.readthedocs.io/libraries/cs50/c/)):
   ```bash
   curl -s https://packagecloud.io/install/repositories/cs50/repo/script.deb.sh | sudo bash
   sudo apt install libcs50
   ```

4. Clone this repository and navigate to the project folder.

5. Compile the C program:
   ```bash
   gcc program_name.c -lcs50 -o program_name
   ```
   
6. Run the C program:
   ```bash
   ./program_name
   ```

### Python Programs
1. Make sure you have Python 3 installed.

2. Clone this repository and navigate to the project folder.

3. Run the program:
   ```bash
   python3 program_name.py
   ```

### Flask Programs
1. Make sure you have Python 3 installed.

2. Clone this repository and navigate to the project folder.
   
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   
4. Install the dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
   
5. Run the development server:
   ```bash
   flask run
   ```
   
6. Open your browser and go to:
   ```bash
   http://127.0.0.1:5000
   ```
   
