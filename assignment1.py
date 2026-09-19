"""
Assignment 2 Solution Key
Course: Introduction to Python
"""

# ==========================================
# Question 1: GET vs POST Requests
# ==========================================
"""
Explanation:
- GET Request: Used to retrieve or request data from a server. It does not 
  modify any data on the server. Parameters are sent directly inside the URL 
  (e.g., https://example.com/search?q=python).
  
- POST Request: Used to send data to a server to create or update resources 
  (like submitting a form or uploading a file). The data is sent securely 
  inside the body of the request, not visible in the URL.
"""

import requests

# Example of making a POST request using the requests library
url = "https://httpbin.org/post"  # A free API testing endpoint

# Data we want to send to the server
student_data = {
    "name": "Alice",
    "course": "Computer Science",
    "year": 1
}

# Sending the POST request with JSON data
response = requests.post(url, json=student_data)

# Checking the response from the server
if response.status_code == 200:
    print("Question 1 Output:")
    print("Data successfully sent!")
    print("Server Response:", response.json()["json"])
    print("-" * 40)


# ==========================================
# Question 2: Working with SQLite in Python
# ==========================================
"""
Key Steps Explained:

1. sqlite3.connect('database_name.db'):
   This connects Python to a database file. If the database file does not exist,
   SQLite will automatically create a new one.

2. Cursor Object (conn.cursor()):
   The cursor acts like a pointer or control tool that lets us run SQL queries, 
   execute commands, and fetch results back into Python.

3. commit() Method (conn.commit()):
   This saves (commits) all changes made to the database permanently. Without 
   calling commit(), any changes made during the session (like inserting or 
   updating data) will be lost when the program closes.
"""


# ==========================================
# Question 3: List Comprehensions
# ==========================================
"""
Explanation:
List comprehensions provide a shorter, cleaner syntax to create a new list 
based on the values of an existing iterable (like a range or another list).

Syntax:
[expression for item in iterable if condition]
"""

# Task: Odd numbers between 1 and 50 that are divisible by 3
# Step-by-step logic:
# 1. Range is from 1 to 50: range(1, 51)
# 2. Odd number check: num % 2 != 0
# 3. Divisible by 3 check: num % 3 == 0

odd_div_by_three = [num for num in range(1, 51) if num % 2 != 0 and num % 3 == 0]

print("Question 3 Output:")
print("Odd numbers between 1 and 50 divisible by 3:")
print(odd_div_by_three)
print("-" * 40)


# ==========================================
# Question 4: Memory-Efficient File Generator
# ==========================================

def chunked_file_reader(file_path, chunk_size_bytes=1024 * 1024):
    """
    Reads a large file lazily in chunks to prevent OutOfMemory errors.
    Handles incomplete lines at chunk boundaries to yield unbroken lines.
    """
    buffer = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            # Read a specific chunk size from the file
            chunk = file.read(chunk_size_bytes)

            # If chunk is empty, we reached the end of the file
            if not chunk:
                break

            # Add the new chunk to our existing leftover buffer
            buffer += chunk

            # Split lines by newline character
            lines = buffer.split('\n')

            # The last item in 'lines' might be an incomplete line,
            # so we keep it in the buffer for the next iteration
            buffer = lines.pop()

            # Yield all complete lines
            for line in lines:
                yield line

        # Yield any remaining text left in the buffer after reading the entire file
        if buffer:
            yield buffer


# Example usage test for Question 4
if __name__ == "__main__":
    # Quick demonstration using a temporary sample file
    sample_filename = "sample_test.txt"

    with open(sample_filename, "w", encoding="utf-8") as f:
        f.write("Line 1: Introduction to Python\n")
        f.write("Line 2: Working with Generators\n")
        f.write("Line 3: Memory Efficient Operations\n")

    print("Question 4 Output:")
    # Using a small chunk size (e.g., 10 bytes) to demonstrate boundary handling
    for line in chunked_file_reader(sample_filename, chunk_size_bytes=10):
        print("Yielded line:", line)

    print("-" * 40)


# ==========================================
# Question 5: Object-Oriented Programming (OOP)
# ==========================================

class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def get_description(self):
        return f"{self.year} {self.make} {self.model}"


class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size):
        # Call the parent class constructor using super()
        super().__init__(make, model, year)
        self.battery_size = battery_size  # Battery size in kWh

    # Overriding the parent method to include battery info
    def get_description(self):
        base_desc = super().get_description()
        return f"{base_desc} with a {self.battery_size}kWh battery"

    # Specific method for battery details
    def get_battery_info(self):
        # Estimating simple range based on battery capacity (approx 5 km per kWh)
        estimated_range = self.battery_size * 5
        return (f"Battery Capacity: {self.battery_size} kWh\n"
                f"Estimated Range: ~{estimated_range} km\n"
                f"Standard Charge Time: 6 to 8 hours (AC Fast Charger)")


# Testing Question 5
print("Question 5 Output:")
my_tesla = ElectricCar("Tesla", "Model 3", 2024, 75)

# Testing overridden description
print(my_tesla.get_description())
print()
# Testing detailed battery info
print(my_tesla.get_battery_info())