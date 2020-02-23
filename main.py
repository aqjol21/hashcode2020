def get_input(file):
    f = open(file, "r")
    lines = f.readlines()
    books_total = int(lines[0].split()[0])
    libraries_total = int(lines[0].split()[1])
    days_total = int(lines[0].split()[2])
    scores_books = list(map(int, lines[1].split()))

    inp_libraries = {}
    lib_id = 0
    for i in range(2, len(lines)):
        if i % 2 == 0:  # even lines contain library description
            lib = {}
            line = lines[i].split()
            if len(line) == 0:
                break
            lib["lib_id"] = lib_id
            lib["total_books"] = int(line[0])
            lib["signup_days"] = int(line[1])
            lib["per_day"] = int(line[2])
            lib["priority"] = 0.00
            lib["books"] = lines[i+1].split()
            lib["scanned_books"] = list()
            inp_libraries[str(lib_id)] = lib
            lib_id += 1
    f.close()
    return books_total, libraries_total, days_total, scores_books, inp_libraries


def write_output(file):
    f = open(file, "w+")
    scanned_libraries = len(library_order)
    f.write(str(scanned_libraries) + "\n")
    for lib in library_order:
        f.write(str(lib["lib_id"]) + " " + str(len(lib["scanned_books"])) + "\n")
        for x in lib["scanned_books"]:
            f.write(str(x + " "))
        f.write("\n")
    f.close()


def update_priorities(libs):
    for k in libs:
        s = 0
        r = (remaining_days - libs[k]["signup_days"])* libs[k]["per_day"]
        for book in libs[k]["books"]:
            if book not in scanned_books:  # unique books
                s = s + books_scores[int(book)]
                r-=1
            if (r==0):
                break
        if (remaining_days - libs[k]["signup_days"]>0):
            libs[k]["priority"] = s *(remaining_days - libs[k]["signup_days"])

def find_max_priority():
    max_priority = 0
    m=0
    for k in libraries:
        if libraries[k]["priority"] > max_priority:
            max_priority = libraries[k]["priority"]
            m = k
    return m


total_books, total_libraries, total_days, books_scores, libraries = get_input("/home/akzhol/Documents/hashcode2020/e_so_many_books.txt")
library_order = []
scanned_books = set()  # just a set
remaining_days = total_days

for i in range(total_libraries):
    libraries[str(i)]["books"].sort(key=lambda x: books_scores[int(x)], reverse=True)

while remaining_days > 0 and not len(libraries) == 0:
    update_priorities(libraries)
    max_index = str(find_max_priority())
    remaining_days -= libraries[max_index]["signup_days"]
    n = remaining_days * libraries[max_index]["per_day"]
    index = 0
    empty = True
    while n > 0 and index < len(libraries[max_index]["books"]):
        book = libraries[max_index]["books"][index]
        if book not in scanned_books:
            scanned_books.add(book)
            libraries[max_index]["scanned_books"].append(book)
            empty = False
            n -= 1
        index += 1
    if not empty:
        library_order.append(libraries[max_index].copy())
        #print(max_index)
        #print("-", libraries[max_index]["signup_days"], "cap is ", libraries[max_index]["per_day"], "Remained ", remaining_days, " days")
    libraries.pop(max_index)

write_output("/home/akzhol/Documents/hashcode2020/e_out.txt")