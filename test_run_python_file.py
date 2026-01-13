from functions.run_python_file import run_python_file


content = run_python_file("calculator", "main.py")
print(content)
content = run_python_file("calculator", "main.py", ["3 + 5"])
print(content)
content = run_python_file("calculator", "tests.py")
print(content)
content = run_python_file("calculator", "../main.py")
print(content)
content = run_python_file("calculator", "nonexistent.py")
print(content)
content = run_python_file("calculator", "lorem.txt")
print(content)