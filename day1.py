print("Hello, World!")

name = "RAM"
faculty = "Computer Science"
dob = "01/01/2000"

# string concatenation
print("Hello, " + name + "!" + " You are a student of " + faculty + " and your date of birth is " + dob + "." )

print(f"Hello, {name}!" + f" You are a student of {faculty} and your date of birth is {dob}.")
print(f"Hello, {name}! You are a student of {faculty} and your date of birth is {dob}.")
# print("Hello, {}! You are a student of {} and your date of birth is {}.".format(name, faculty, dob))

age = 24
is_student = True
gpa = 3.8

# Check data types
print(f"Type of name: {type(name)}")  # str
print(f"Type of faculty: {type(faculty)}")  # str
print(f"Type of dob: {type(dob)}")  # str
print(f"Type of age: {type(age)}")  # int
print(f"Type of is_student: {type(is_student)}")  # bool
print(f"Type of gpa : {type(gpa)}")  # float

# multiple assignment
name, faculty, dob, age, is_student, gpa = "Hari", "BCA", "01/01/2000", 25, True, 3.98

print(f"Hello, {name}! You are a student of {faculty} and your date of birth is {dob}. You are {age} years old, student status: {is_student}, and your GPA is {gpa}.")


# Swap variables easily
x, y = 10, 20
print("Before swap: x=", x, "y=", y)
x, y = y, x  # Swap without temporary variable
print("After swap: x=", x, "y=", y)

# Unpack lists
student_info = ["Charlie", 21, 88.0]
name, age, score = student_info
print("Unpacked:", name, age, score)

name1, *others = student_info
print("Name:", name1)
print("Others:", others)  # This will be a list containing age and score

# Creating lists
student_names = ["Alice", "Bob", "Charlie", "Diana"]
student_scores = [85, 92, 78, 95]

print("Student Names:", student_names)
print("Student Scores:", student_scores)

# Accessing elements (indexing starts at 0)
print("\nFirst student:", student_names[0])
print("Last student:", student_names[-1])
print("First three:", student_names[0:3])
# all students from index 1 to end
print("Students from index 1 to end:", student_names[:])
print("Every second student:", student_names[::2])


# List operations
student_names.append("Eve")      # Add to end
print("\nAfter adding Eve:", student_names)

student_names.insert(1, "Frank") # Insert at position
print("After inserting Frank:", student_names)

student_names.remove("Bob")      # Remove by value
print("After removing Bob:", student_names)

# List comprehension (powerful feature!)
passing_scores = [score for score in student_scores if score >= 80]
print("\nPassing scores (>=80):", passing_scores)

# Common methods
print("Number of students:", len(student_names))
print("Highest score:", max(student_scores))
print("Lowest score:", min(student_scores))


# Tuples are similar to lists but are immutable (cannot be changed after creation)

# Tuples cannot be changed after creation
student_record = ("Alice", 20, 85.5, "Computer Science")
print("Student Record Tuple:", student_record)

# Accessing tuple elements
print("Name:", student_record[0])
print("Age:", student_record[1])

# Tuple unpacking
name, age, score, department = student_record
print("\nUnpacked:", name, "is", age, "years old, scored", score, "in", department)

# When to use tuples?
# - Fixed data that shouldn't change
# - Dictionary keys (lists can't be keys)
# - Returning multiple values from a function


print("\n--- Sets ---")
print("="*50)
# Sets are unordered collections of unique items (no duplicates allowed)
# Sets automatically remove duplicates
course_A = {"Alice", "Bob", "Charlie", "Diana"}
course_B = {"Charlie", "Diana", "Eve", "Frank"}

print("Course A students:", course_A)
print("Course B students:", course_B)

# Set operations (great for finding overlaps)
print("\nStudents in both courses:", course_A & course_B)
print("Students in eith`er course:", course_A | course_B)
print("Only in Course A:", course_A - course_B)
print("Only in one course:", course_A ^ course_B)

# Remove duplicates from list using set
scores_with_duplicates = [85, 92, 85, 78, 92, 95, 85]
unique_scores = list(set(scores_with_duplicates))
print("\nOriginal scores:", scores_with_duplicates)
print("Unique scores:", unique_scores)