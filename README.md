# Fashion-studio-data-pipeline
Menggunakan virtual environment sebelum menjalankan program, namun ketika submission ini diunggah folder .env dihapus karena pada kriteria tidak terdaftar.

# Menjalankan Skrip
main.py 
Di main.py memuat extract.py, transform.py, dan load.py
(saya menggunakan command prompt(terminal))

# URL google sheet
https://docs.google.com/spreadsheets/d/1a20oW2CHLPMPpFtIJGZk5Y-ERt63aCXymBOhZ6xBb6g/edit?gid=0#gid=0

# Melihat database di postgreSQL
psql --username developer --dbname productsdb -> \dt -> SELECT * FROM productstoscrape;
pass : meicha15 
(Saya menjalankannya di Terminal)

# Menjalankan unit test pada folder test
coverage run -m pytest test

# Menjalankan test coverage pada folder tests (coverage report)
coverage report

Hasil coverage report:
(.env) E:\submission-pemda>coverage report
Name                     Stmts   Miss  Cover
--------------------------------------------
test\test_extract.py        45      1    98%
test\test_load.py           15      0   100%
test\test_transform.py      13      1    92%
utils\extract.py            58      8    86%
utils\load.py               28     14    50%
utils\transform.py          35      5    86%
--------------------------------------------
TOTAL                      194     29    85%
