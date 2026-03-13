class FileManager:
    def __init__(self):
        self.cd = "/home/user"
        self.files = []
    def create_file(self, filename):
        self.files.append(filename)
        print("Created: ", filename, "in ", self.cd)
    def list_files(self):
        if len(self.files) > 0:
            for i, file in enumerate(self.files):
                print(i, ": ", file)
            return
        print("No files listed")
    def delete_file(self, filename):
        if len(self.files) < 1:
            print("No files listed")
            return
        for i, file in enumerate(self.files):
            if file == filename:
                self.files.remove(filename)
                print("Deleted: ", filename)
                return
        print("No file stored with that name")

temp = FileManager()
temp.create_file("something1.txt")
temp.create_file("something2.txt")
temp.create_file("something3.txt")
temp.list_files()
temp.delete_file("something1.txt")
temp.list_files()