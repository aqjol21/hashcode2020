def get_input(file):
    f = open(file, "r")
    lines = f.readlines()
    numberOfBooks = int(lines[0].split()[0])
    numberOfLibraries = int(lines[0].split()[1])
    numberOfDays = int(lines[0].split()[2])
    bookScores = list(map(int, lines[1].split()))

    inp_books = []
    book_id = 0
    for b in range(len(bookScores)):
        bookk = {"book_id": book_id, "score": bookScores[b]}
        inp_books.append(bookk)
        book_id += 1

    inp_libraries = []
    lib_id = 0
    for i in range(2, len(lines)):
        if i % 2 == 0:  # it is a library description
            lib = {}
            line = lines[i].split()
            if len(line) == 0:
                break
            lib["lib_id"] = lib_id
            lib["total_books"] = int(line[0])
            lib["signup_days"] = int(line[1])
            lib["per_day"] = int(line[2])
            line = lines[i+1].split()
            lib_books = []
            for b in line:
                bookk = {"book_id": int(b), "score": bookScores[int(b)]}
                lib_books.append(bookk)
            lib["books"] = lib_books
            inp_libraries.append(lib)
            lib_id += 1
    f.close()

    inp_books = sorted(inp_books, key=lambda x: x["score"], reverse=True)
    for l in range(len(inp_libraries)):
        bs = sorted(inp_libraries[l]["books"], key=lambda x: x["score"], reverse=True)
        inp_libraries[l]["books"] = bs

    return numberOfBooks, numberOfLibraries, numberOfDays, inp_books, inp_libraries


def write_output(file):
    f = open(file, "w+")
    scanned_libraries = len(library_order)
    f.write(str(scanned_libraries) + "\n")
    for lib in library_order:
        books_total = len(lib["scanned_books"])
        f.write(str(lib["lib_id"]) + " " + str(books_total) + "\n")
        for x in lib["scanned_books"]:
            f.write(str(x["book_id"]) + " ")
        f.write("\n")
    f.close()


def calculate_priority(lib):
    s = 0
    for book in lib["books"]:
        if book not in scanned_books:  # unique books
            s = s + book["score"]
        lib["priority"] = s * (remaining_days - lib["signup_days"]) / lib["per_day"]


total_books, total_libraries, total_days, books, libraries = get_input("c.txt")
library_order = []
scanned_books = []
remaining_days = total_days

while remaining_days > 0 and not len(libraries) == 0:
    for library in libraries:
        calculate_priority(library)

    max_priority_library = libraries[0]
    max_priority_library_index = 0
    for ind in range(len(libraries)):
        if libraries[ind]["priority"] > max_priority_library["priority"]:
            max_priority_library_index = ind
    
    remaining_days = remaining_days - libraries[max_priority_library_index]["signup_days"]
    n = remaining_days * libraries[max_priority_library_index]["per_day"]
    libraries[max_priority_library_index]["scanned_books"] = []
    index = 0
    while n > 0 and index < len(libraries[max_priority_library_index]["books"]):
        book = libraries[max_priority_library_index]["books"][index]
        if book not in scanned_books:
            scanned_books.append(book)
            libraries[max_priority_library_index]["scanned_books"].append(book)
            n -= 1
        index += 1
    library_order.append(libraries[max_priority_library_index].copy())
    print(libraries[max_priority_library_index]["lib_id"])
    libraries.pop(max_priority_library_index)

write_output("c_out.txt")