import pathlib
print(pathlib.Path(__file__).parent.parent.resolve().__str__() + '/database')