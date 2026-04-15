import sqlite3

DB_NAME = "books.db"

# Sample data
books = [
    # 20 programming books
    (1, "The Pragmatic Programmer", "Andrew Hunt", None, 352, "9780201616224", "https://covers.openlibrary.org/b/isbn/9780201616224-M.jpg"),
    (2, "Clean Code", "Robert C. Martin", None, 464, "9780132350884", "https://covers.openlibrary.org/b/isbn/9780132350884-M.jpg"),
    (3, "Automate the Boring Stuff with Python", "Al Sweigart", None, 504, "9781593275990", "https://covers.openlibrary.org/b/isbn/9781593275990-M.jpg"),
    (4, "Python Crash Course", "Eric Matthes", None, 544, "9781593279288", "https://covers.openlibrary.org/b/isbn/9781593279288-M.jpg"),
    (5, "Fluent Python", "Luciano Ramalho", None, 792, "9781491946008", "https://covers.openlibrary.org/b/isbn/9781491946008-M.jpg"),
    (6, "Effective Python", "Brett Slatkin", None, 480, "9780134034287", "https://covers.openlibrary.org/b/isbn/9780134034287-M.jpg"),
    (7, "Head First Design Patterns", "Eric Freeman", None, 694, "9780596007126", "https://covers.openlibrary.org/b/isbn/9780596007126-M.jpg"),
    (8, "Structure and Interpretation of Computer Programs", "Harold Abelson", None, 657, "9780262510875", "https://covers.openlibrary.org/b/isbn/9780262510875-M.jpg"),
    (9, "Introduction to Algorithms", "Thomas H. Cormen", None, 1312, "9780262033848", "https://covers.openlibrary.org/b/isbn/9780262033848-M.jpg"),
    (10, "Operating System Concepts", "Abraham Silberschatz", None, 992, "9781118063330", "https://covers.openlibrary.org/b/isbn/9781118063330-M.jpg"),
    (11, "Database System Concepts", "Abraham Silberschatz", None, 1376, "9780073523323", "https://covers.openlibrary.org/b/isbn/9780073523323-M.jpg"),
    (12, "Learning SQL", "Alan Beaulieu", None, 338, "9780596520830", "https://covers.openlibrary.org/b/isbn/9780596520830-M.jpg"),
    (13, "The C Programming Language", "Brian W. Kernighan", None, 288, "9780131103627", "https://covers.openlibrary.org/b/isbn/9780131103627-M.jpg"),
    (14, "C Programming: A Modern Approach", "K. N. King", None, 832, "9780393979503", "https://covers.openlibrary.org/b/isbn/9780393979503-M.jpg"),
    (15, "Effective C", "Robert C. Seacord", None, 256, "9781718501041", "https://covers.openlibrary.org/b/isbn/9781718501041-M.jpg"),
    (16, "Programming Rust", "Jim Blandy", None, 624, "9781492052593", "https://covers.openlibrary.org/b/isbn/9781492052593-M.jpg"),
    (17, "The Rust Programming Language", "Steve Klabnik", None, 552, "9781593278281", "https://covers.openlibrary.org/b/isbn/9781593278281-M.jpg"),
    (18, "Eloquent JavaScript", "Marijn Haverbeke", None, 472, "9781593279509", "https://covers.openlibrary.org/b/isbn/9781593279509-M.jpg"),
    (19, "Pro Git", "Scott Chacon", None, 458, "9781484200773", "https://covers.openlibrary.org/b/isbn/9781484200773-M.jpg"),
    (20, "Refactoring", "Martin Fowler", None, 448, "9780201485677", "https://covers.openlibrary.org/b/isbn/9780201485677-M.jpg"),

    # 60 novels
    (21, "The Alchemist", "Paulo Coelho", None, 208, "9780062315007", "https://covers.openlibrary.org/b/isbn/9780062315007-M.jpg"),
    (22, "1984", "George Orwell", None, 328, "9780451524935", "https://covers.openlibrary.org/b/isbn/9780451524935-M.jpg"),
    (23, "Animal Farm", "George Orwell", None, 112, "9780451526342", "https://covers.openlibrary.org/b/isbn/9780451526342-M.jpg"),
    (24, "To Kill a Mockingbird", "Harper Lee", None, 336, "9780061120084", "https://covers.openlibrary.org/b/isbn/9780061120084-M.jpg"),
    (25, "The Great Gatsby", "F. Scott Fitzgerald", None, 180, "9780743273565", "https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg"),
    (26, "Pride and Prejudice", "Jane Austen", None, 279, "9780141439518", "https://covers.openlibrary.org/b/isbn/9780141439518-M.jpg"),
    (27, "Frankenstein", "Mary Shelley", None, 280, "9780486282114", "https://covers.openlibrary.org/b/isbn/9780486282114-M.jpg"),
    (28, "Moby-Dick", "Herman Melville", None, 635, "9781503280786", "https://covers.openlibrary.org/b/isbn/9781503280786-M.jpg"),
    (29, "Jane Eyre", "Charlotte Brontë", None, 500, "9780141441146", "https://covers.openlibrary.org/b/isbn/9780141441146-M.jpg"),
    (30, "Wuthering Heights", "Emily Brontë", None, 464, "9780141439556", "https://covers.openlibrary.org/b/isbn/9780141439556-M.jpg"),
    (31, "The Catcher in the Rye", "J. D. Salinger", None, 277, "9780316769488", "https://covers.openlibrary.org/b/isbn/9780316769488-M.jpg"),
    (32, "Brave New World", "Aldous Huxley", None, 311, "9780060850524", "https://covers.openlibrary.org/b/isbn/9780060850524-M.jpg"),
    (33, "Lord of the Flies", "William Golding", None, 224, "9780399501487", "https://covers.openlibrary.org/b/isbn/9780399501487-M.jpg"),
    (34, "The Little Prince", "Antoine de Saint-Exupéry", None, 96, "9780156012195", "https://covers.openlibrary.org/b/isbn/9780156012195-M.jpg"),
    (35, "The Kite Runner", "Khaled Hosseini", None, 371, "9781594631931", "https://covers.openlibrary.org/b/isbn/9781594631931-M.jpg"),
    (36, "A Thousand Splendid Suns", "Khaled Hosseini", None, 384, "9781594489501", "https://covers.openlibrary.org/b/isbn/9781594489501-M.jpg"),
    (37, "The Book Thief", "Markus Zusak", None, 584, "9780375842207", "https://covers.openlibrary.org/b/isbn/9780375842207-M.jpg"),
    (38, "The Fault in Our Stars", "John Green", None, 313, "9780525478812", "https://covers.openlibrary.org/b/isbn/9780525478812-M.jpg"),
    (39, "Dune", "Frank Herbert", None, 896, "9780441172719", "https://covers.openlibrary.org/b/isbn/9780441172719-M.jpg"),
    (40, "The Hobbit", "J. R. R. Tolkien", None, 310, "9780547928227", "https://covers.openlibrary.org/b/isbn/9780547928227-M.jpg"),
    (41, "Harry Potter and the Sorcerer's Stone", "J. K. Rowling", None, 309, "9780590353427", "https://covers.openlibrary.org/b/isbn/9780590353427-M.jpg"),
    (42, "Harry Potter and the Chamber of Secrets", "J. K. Rowling", None, 341, "9780439064873", "https://covers.openlibrary.org/b/isbn/9780439064873-M.jpg"),
    (43, "Harry Potter and the Prisoner of Azkaban", "J. K. Rowling", None, 435, "9780439136365", "https://covers.openlibrary.org/b/isbn/9780439136365-M.jpg"),
    (44, "Harry Potter and the Goblet of Fire", "J. K. Rowling", None, 734, "9780439139601", "https://covers.openlibrary.org/b/isbn/9780439139601-M.jpg"),
    (45, "Harry Potter and the Order of the Phoenix", "J. K. Rowling", None, 870, "9780439358071", "https://covers.openlibrary.org/b/isbn/9780439358071-M.jpg"),
    (46, "Harry Potter and the Half-Blood Prince", "J. K. Rowling", None, 652, "9780439785969", "https://covers.openlibrary.org/b/isbn/9780439785969-M.jpg"),
    (47, "Harry Potter and the Deathly Hallows", "J. K. Rowling", None, 759, "9780545139700", "https://covers.openlibrary.org/b/isbn/9780545139700-M.jpg"),
    (48, "The Da Vinci Code", "Dan Brown", None, 454, "9780307474278", "https://covers.openlibrary.org/b/isbn/9780307474278-M.jpg"),
    (49, "Angels & Demons", "Dan Brown", None, 616, "9780743493468", "https://covers.openlibrary.org/b/isbn/9780743493468-M.jpg"),
    (50, "The Girl on the Train", "Paula Hawkins", None, 395, "9781594634024", "https://covers.openlibrary.org/b/isbn/9781594634024-M.jpg"),
    (51, "Gone Girl", "Gillian Flynn", None, 415, "9780307588371", "https://covers.openlibrary.org/b/isbn/9780307588371-M.jpg"),
    (52, "The Silent Patient", "Alex Michaelides", None, 336, "9781250301697", "https://covers.openlibrary.org/b/isbn/9781250301697-M.jpg"),
    (53, "Verity", "Colleen Hoover", None, 336, "9781791392796", "https://covers.openlibrary.org/b/isbn/9781791392796-M.jpg"),
    (54, "It Ends with Us", "Colleen Hoover", None, 376, "9781501110368", "https://covers.openlibrary.org/b/isbn/9781501110368-M.jpg"),
    (55, "The Midnight Library", "Matt Haig", None, 304, "9780525559474", "https://covers.openlibrary.org/b/isbn/9780525559474-M.jpg"),
    (56, "Normal People", "Sally Rooney", None, 304, "9781984822178", "https://covers.openlibrary.org/b/isbn/9781984822178-M.jpg"),
    (57, "Where the Crawdads Sing", "Delia Owens", None, 384, "9780735219106", "https://covers.openlibrary.org/b/isbn/9780735219106-M.jpg"),
    (58, "The Road", "Cormac McCarthy", None, 287, "9780307387899", "https://covers.openlibrary.org/b/isbn/9780307387899-M.jpg"),
    (59, "The Giver", "Lois Lowry", None, 240, "9780544336261", "https://covers.openlibrary.org/b/isbn/9780544336261-M.jpg"),
    (60, "The Name of the Wind", "Patrick Rothfuss", None, 662, "9780756404741", "https://covers.openlibrary.org/b/isbn/9780756404741-M.jpg"),
    (61, "The Wise Man's Fear", "Patrick Rothfuss", None, 1192, "9780756407919", "https://covers.openlibrary.org/b/isbn/9780756407919-M.jpg"),
    (62, "The Poppy War", "R. F. Kuang", None, 544, "9780062662563", "https://covers.openlibrary.org/b/isbn/9780062662563-M.jpg"),
    (63, "Babel", "R. F. Kuang", None, 544, "9780063021426", "https://covers.openlibrary.org/b/isbn/9780063021426-M.jpg"),
    (64, "Project Hail Mary", "Andy Weir", None, 496, "9780593135204", "https://covers.openlibrary.org/b/isbn/9780593135204-M.jpg"),
    (65, "The Martian", "Andy Weir", None, 369, "9780804139021", "https://covers.openlibrary.org/b/isbn/9780804139021-M.jpg"),
    (66, "Ready Player One", "Ernest Cline", None, 374, "9780307887443", "https://covers.openlibrary.org/b/isbn/9780307887443-M.jpg"),
    (67, "Ender's Game", "Orson Scott Card", None, 324, "9780812550702", "https://covers.openlibrary.org/b/isbn/9780812550702-M.jpg"),
    (68, "Neuromancer", "William Gibson", None, 271, "9780441569595", "https://covers.openlibrary.org/b/isbn/9780441569595-M.jpg"),
    (69, "Snow Crash", "Neal Stephenson", None, 480, "9780553380958", "https://covers.openlibrary.org/b/isbn/9780553380958-M.jpg"),
    (70, "The Handmaid's Tale", "Margaret Atwood", None, 311, "9780385490818", "https://covers.openlibrary.org/b/isbn/9780385490818-M.jpg"),
    (71, "The Hunger Games", "Suzanne Collins", None, 374, "9780439023528", "https://covers.openlibrary.org/b/isbn/9780439023528-M.jpg"),
    (72, "Catching Fire", "Suzanne Collins", None, 391, "9780439023498", "https://covers.openlibrary.org/b/isbn/9780439023498-M.jpg"),
    (73, "Mockingjay", "Suzanne Collins", None, 390, "9780439023511", "https://covers.openlibrary.org/b/isbn/9780439023511-M.jpg"),
    (74, "The Girl with the Dragon Tattoo", "Stieg Larsson", None, 465, "9780307454546", "https://covers.openlibrary.org/b/isbn/9780307454546-M.jpg"),
    (75, "The Shadow of the Wind", "Carlos Ruiz Zafón", None, 565, "9780143034902", "https://covers.openlibrary.org/b/isbn/9780143034902-M.jpg"),
    (76, "Beloved", "Toni Morrison", None, 324, "9781400033416", "https://covers.openlibrary.org/b/isbn/9781400033416-M.jpg"),
    (77, "Things Fall Apart", "Chinua Achebe", None, 209, "9780385474542", "https://covers.openlibrary.org/b/isbn/9780385474542-M.jpg"),
    (78, "The God of Small Things", "Arundhati Roy", None, 340, "9780679457313", "https://covers.openlibrary.org/b/isbn/9780679457313-M.jpg"),
    (79, "The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", None, 400, "9781501161933", "https://covers.openlibrary.org/b/isbn/9781501161933-M.jpg"),
    (80, "Tuesdays with Morrie", "Mitch Albom", None, 192, "9780767905923", "https://covers.openlibrary.org/b/isbn/9780767905923-M.jpg"),

    # 20 self-help books
    (81, "Atomic Habits", "James Clear", None, 320, "9780735211292", "https://covers.openlibrary.org/b/isbn/9780735211292-M.jpg"),
    (82, "Deep Work", "Cal Newport", None, 304, "9781455586691", "https://covers.openlibrary.org/b/isbn/9781455586691-M.jpg"),
    (83, "Thinking, Fast and Slow", "Daniel Kahneman", None, 512, "9780374533557", "https://covers.openlibrary.org/b/isbn/9780374533557-M.jpg"),
    (84, "How to Win Friends and Influence People", "Dale Carnegie", None, 288, "9780671772468", "https://covers.openlibrary.org/b/isbn/9780671772468-M.jpg"),
    (85, "The 7 Habits of Highly Effective People", "Stephen R. Covey", None, 381, "9780743269513", "https://covers.openlibrary.org/b/isbn/9780743269513-M.jpg"),
    (86, "The Subtle Art of Not Giving a F*ck", "Mark Manson", None, 224, "9780062457714", "https://covers.openlibrary.org/b/isbn/9780062457714-M.jpg"),
    (87, "Rich Dad Poor Dad", "Robert T. Kiyosaki", None, 336, "9781612680194", "https://covers.openlibrary.org/b/isbn/9781612680194-M.jpg"),
    (88, "The Psychology of Money", "Morgan Housel", None, 256, "9780857197689", "https://covers.openlibrary.org/b/isbn/9780857197689-M.jpg"),
    (89, "Man's Search for Meaning", "Viktor E. Frankl", None, 224, "9780807014271", "https://covers.openlibrary.org/b/isbn/9780807014271-M.jpg"),
    (90, "Meditations", "Marcus Aurelius", None, 304, "9780812968255", "https://covers.openlibrary.org/b/isbn/9780812968255-M.jpg"),
    (91, "Think and Grow Rich", "Napoleon Hill", None, 238, "9781585424337", "https://covers.openlibrary.org/b/isbn/9781585424337-M.jpg"),
    (92, "The Power of Now", "Eckhart Tolle", None, 236, "9781577314806", "https://covers.openlibrary.org/b/isbn/9781577314806-M.jpg"),
    (93, "The Four Agreements", "Don Miguel Ruiz", None, 160, "9781878424310", "https://covers.openlibrary.org/b/isbn/9781878424310-M.jpg"),
    (94, "Make Your Bed", "William H. McRaven", None, 144, "9781455570249", "https://covers.openlibrary.org/b/isbn/9781455570249-M.jpg"),
    (95, "The War of Art", "Steven Pressfield", None, 192, "9781936891023", "https://covers.openlibrary.org/b/isbn/9781936891023-M.jpg"),
    (96, "Start with Why", "Simon Sinek", None, 256, "9781591846444", "https://covers.openlibrary.org/b/isbn/9781591846444-M.jpg"),
    (97, "Grit", "Angela Duckworth", None, 333, "9781501111105", "https://covers.openlibrary.org/b/isbn/9781501111105-M.jpg"),
    (98, "The Obstacle Is the Way", "Ryan Holiday", None, 224, "9781591846352", "https://covers.openlibrary.org/b/isbn/9781591846352-M.jpg"),
    (99, "Drive", "Daniel H. Pink", None, 272, "9781594484803", "https://covers.openlibrary.org/b/isbn/9781594484803-M.jpg"),
    (100, "Ikigai", "Héctor García", None, 208, "9780143130727", "https://covers.openlibrary.org/b/isbn/9780143130727-M.jpg"),
]
users = [
    (1, "cruzabraham", "La Cruz", "Book lover and developer", "/pics/cruz.jpg", "asdf"),
    (2, "jane_doe", "Jane Doe", "Reads mostly fiction", "/pics/jane.jpg", "asdf"),
]

user_books = [
    (1, 1, 25.0, "reading"),
    (1, 2, 100.0, "read"),
    (1, 3, 0.0, "plan"),
    (1, 4, 60.0, "reading"),
    (1, 5, 10.0, "reading"),
    (1, 6, 100.0, "read"),
    (1, 7, 0.0, "plan"),
    (1, 8, 45.0, "reading"),

    (2, 1, 100.0, "read"),
    (2, 2, 0.0, "plan"),
    (2, 3, 30.0, "reading"),
    (2, 4, 0.0, "plan"),
    (2, 5, 80.0, "reading"),
    (2, 6, 100.0, "read"),
    (2, 7, 15.0, "reading"),
    (2, 8, 0.0, "plan"),

    (3, 9, 5.0, "reading"),
    (3, 10, 100.0, "read"),
    (3, 11, 0.0, "plan"),
    (3, 12, 65.0, "reading"),
    (3, 13, 100.0, "read"),
    (3, 14, 0.0, "plan"),
    (3, 15, 20.0, "reading"),

    (4, 16, 100.0, "read"),
    (4, 17, 40.0, "reading"),
    (4, 18, 0.0, "plan"),
    (4, 19, 100.0, "read"),
    (4, 20, 75.0, "reading"),
    (4, 21, 0.0, "plan"),

    (5, 22, 100.0, "read"),
    (5, 23, 35.0, "reading"),
    (5, 24, 0.0, "plan"),
    (5, 25, 100.0, "read"),
    (5, 26, 50.0, "reading"),
    (5, 27, 0.0, "plan"),

    (6, 28, 100.0, "read"),
    (6, 29, 15.0, "reading"),
    (6, 30, 0.0, "plan"),
    (6, 31, 100.0, "read"),
    (6, 32, 70.0, "reading"),
    (6, 33, 0.0, "plan"),

    (7, 34, 100.0, "read"),
    (7, 35, 20.0, "reading"),
    (7, 36, 0.0, "plan"),
    (7, 37, 100.0, "read"),
    (7, 38, 55.0, "reading"),
    (7, 39, 0.0, "plan"),

    (8, 40, 100.0, "read"),
    (8, 1, 10.0, "reading"),
    (8, 2, 0.0, "plan"),
    (8, 3, 100.0, "read"),
    (8, 4, 33.0, "reading"),
    (8, 5, 0.0, "plan"),
]

genres = [
    (1, "Programming"),
    (2, "Software Engineering"),
    (3, "Computer Science"),
    (4, "Algorithms"),
    (5, "Databases"),
    (6, "Operating Systems"),
    (7, "Systems Programming"),
    (8, "Web Development"),
    (9, "Version Control"),
    (10, "Fiction"),
    (11, "Classic"),
    (12, "Dystopian"),
    (13, "Romance"),
    (14, "Horror"),
    (15, "Adventure"),
    (16, "Fantasy"),
    (17, "Science Fiction"),
    (18, "Thriller"),
    (19, "Mystery"),
    (20, "Historical Fiction"),
    (21, "Literary Fiction"),
    (22, "Coming-of-Age"),
    (23, "Young Adult"),
    (24, "African Literature"),
    (25, "Self-Help"),
    (26, "Productivity"),
    (27, "Psychology"),
    (28, "Finance"),
    (29, "Stoicism"),
    (30, "Personal Development"),
    (31, "Leadership"),
    (32, "Philosophy"),
    (33, "Nonfiction"),
    (34, "Memoir"),
]

genre_id = {name: gid for gid, name in genres}

book_genres = []

def add_genres(book_id, *genre_names):
    for genre_name in genre_names:
        book_genres.append((book_id, genre_id[genre_name]))

add_genres(1, "Programming", "Software Engineering")
add_genres(2, "Programming", "Software Engineering")
add_genres(3, "Programming", "Software Engineering")
add_genres(4, "Programming")
add_genres(5, "Programming")
add_genres(6, "Programming")
add_genres(7, "Programming", "Software Engineering")
add_genres(8, "Programming", "Computer Science")
add_genres(9, "Algorithms", "Computer Science")
add_genres(10, "Operating Systems", "Computer Science")
add_genres(11, "Databases", "Computer Science")
add_genres(12, "Databases")
add_genres(13, "Programming", "Systems Programming")
add_genres(14, "Programming", "Systems Programming")
add_genres(15, "Programming", "Systems Programming")
add_genres(16, "Programming", "Systems Programming")
add_genres(17, "Programming", "Systems Programming")
add_genres(18, "Programming", "Web Development")
add_genres(19, "Version Control", "Software Engineering")
add_genres(20, "Programming", "Software Engineering")

add_genres(21, "Fiction", "Literary Fiction")
add_genres(22, "Fiction", "Dystopian", "Classic")
add_genres(23, "Fiction", "Dystopian", "Classic")
add_genres(24, "Fiction", "Classic", "Literary Fiction")
add_genres(25, "Fiction", "Classic", "Literary Fiction")
add_genres(26, "Fiction", "Classic", "Romance")
add_genres(27, "Fiction", "Classic", "Horror")
add_genres(28, "Fiction", "Classic", "Adventure")
add_genres(29, "Fiction", "Classic", "Romance")
add_genres(30, "Fiction", "Classic", "Romance")
add_genres(31, "Fiction", "Classic", "Coming-of-Age")
add_genres(32, "Fiction", "Dystopian", "Classic")
add_genres(33, "Fiction", "Classic", "Coming-of-Age")
add_genres(34, "Fiction", "Classic")
add_genres(35, "Fiction", "Historical Fiction", "Literary Fiction")
add_genres(36, "Fiction", "Historical Fiction", "Literary Fiction")
add_genres(37, "Fiction", "Historical Fiction", "Literary Fiction")
add_genres(38, "Fiction", "Young Adult", "Romance", "Coming-of-Age")
add_genres(39, "Fiction", "Science Fiction", "Adventure")
add_genres(40, "Fiction", "Fantasy", "Adventure")
for book_id in range(41, 48):
    add_genres(book_id, "Fiction", "Fantasy", "Adventure", "Young Adult")
add_genres(48, "Fiction", "Mystery", "Thriller")
add_genres(49, "Fiction", "Mystery", "Thriller")
add_genres(50, "Fiction", "Thriller", "Mystery")
add_genres(51, "Fiction", "Thriller", "Mystery")
add_genres(52, "Fiction", "Thriller", "Mystery")
add_genres(53, "Fiction", "Thriller", "Mystery")
add_genres(54, "Fiction", "Romance", "Young Adult")
add_genres(55, "Fiction", "Literary Fiction")
add_genres(56, "Fiction", "Literary Fiction", "Romance")
add_genres(57, "Fiction", "Mystery", "Literary Fiction")
add_genres(58, "Fiction", "Science Fiction", "Literary Fiction")
add_genres(59, "Fiction", "Dystopian", "Young Adult")
add_genres(60, "Fiction", "Fantasy", "Adventure")
add_genres(61, "Fiction", "Fantasy", "Adventure")
add_genres(62, "Fiction", "Fantasy", "Historical Fiction")
add_genres(63, "Fiction", "Fantasy", "Historical Fiction")
add_genres(64, "Fiction", "Science Fiction", "Adventure")
add_genres(65, "Fiction", "Science Fiction", "Adventure")
add_genres(66, "Fiction", "Science Fiction", "Adventure")
add_genres(67, "Fiction", "Science Fiction", "Young Adult")
add_genres(68, "Fiction", "Science Fiction")
add_genres(69, "Fiction", "Science Fiction")
add_genres(70, "Fiction", "Dystopian", "Classic")
add_genres(71, "Fiction", "Dystopian", "Young Adult")
add_genres(72, "Fiction", "Dystopian", "Young Adult")
add_genres(73, "Fiction", "Dystopian", "Young Adult")
add_genres(74, "Fiction", "Thriller", "Mystery")
add_genres(75, "Fiction", "Mystery", "Historical Fiction")
add_genres(76, "Fiction", "Literary Fiction", "Historical Fiction")
add_genres(77, "Fiction", "African Literature", "Classic")
add_genres(78, "Fiction", "Literary Fiction", "Historical Fiction")
add_genres(79, "Fiction", "Romance", "Historical Fiction")
add_genres(80, "Nonfiction", "Memoir", "Personal Development")

add_genres(81, "Self-Help", "Productivity", "Personal Development")
add_genres(82, "Self-Help", "Productivity", "Personal Development")
add_genres(83, "Psychology", "Self-Help", "Nonfiction")
add_genres(84, "Self-Help", "Leadership", "Personal Development")
add_genres(85, "Self-Help", "Leadership", "Personal Development")
add_genres(86, "Self-Help", "Personal Development")
add_genres(87, "Finance", "Self-Help", "Personal Development")
add_genres(88, "Finance", "Psychology", "Self-Help")
add_genres(89, "Philosophy", "Self-Help", "Nonfiction")
add_genres(90, "Philosophy", "Stoicism", "Self-Help")
add_genres(91, "Finance", "Self-Help", "Personal Development")
add_genres(92, "Philosophy", "Self-Help", "Personal Development")
add_genres(93, "Philosophy", "Self-Help", "Personal Development")
add_genres(94, "Self-Help", "Leadership", "Personal Development")
add_genres(95, "Self-Help", "Personal Development")
add_genres(96, "Leadership", "Self-Help", "Personal Development")
add_genres(97, "Psychology", "Self-Help", "Personal Development")
add_genres(98, "Philosophy", "Stoicism", "Self-Help")
add_genres(99, "Psychology", "Self-Help", "Personal Development")
add_genres(100, "Self-Help", "Philosophy", "Personal Development")

def main():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(id INTERGER PRIMARY KEY UNIQUE, 
                   title TEXT, 
                   author TEXT, 
                   file_path TEXT, 
                   page_count INTERGER,
                   isbn TEXT,
                   cover_path TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS user_books(user_id INTERGE, 
                    book_id INTERGER, 
                    progress DECIMAL, 
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    FOREIGN KEY (book_id) REFERENCES books(id))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(id INTERGER UNIQUE, 
                    username TEXT, 
                    name TEXT,
                    bio TEXT,
                    pic_path TEXT,
                    password TEXT)""")

    #  New genre tables
    cursor.execute("""CREATE TABLE IF NOT EXISTS genres (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS book_genres (
                    book_id INTEGER,
                    genre_id INTEGER,
                    PRIMARY KEY (book_id, genre_id),
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (genre_id) REFERENCES genres(id)
    )""")



    cursor.executemany("""
        INSERT OR REPLACE INTO books
        (id, title, author, file_path, page_count,isbn, cover_path)
        VALUES (?, ?, ?, ?, ?,?, ?)
    """, books)

    cursor.executemany("""
        INSERT OR REPLACE INTO users
        (id, username, name, bio, pic_path, password)
        VALUES (?, ?, ?, ?, ?, ?)
    """, users)

    cursor.executemany("""
        INSERT INTO user_books
        (user_id, book_id, progress, status)
        VALUES (?, ?, ?, ?)
    """, user_books)

    cursor.executemany("""
        INSERT OR REPLACE INTO genres
        (id, name)
        VALUES (?, ?)
    """, genres)

    cursor.executemany("""
        INSERT OR REPLACE INTO book_genres
        (book_id, genre_id)
        VALUES (?, ?)
    """, book_genres)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
