from functions.write_file import write_file

content = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(content)
content = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(content)
content = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(content)
