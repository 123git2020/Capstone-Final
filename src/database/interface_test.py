from DBInterface import DBInterface

if __name__ == 'main':
    # PASSWORD can be found from important.txt, eventually use dotenv
    inter = DBInterface("classification_db", "postgres", PASSWORD, 5433)
    inter.insert_entry("test_interface1", "test_interface3")
    print(inter.retrieve_by_filename("test_interface1"))
    print(inter.retrieve_by_filename("test1"))
    inter.remove_entry("test_interface1")