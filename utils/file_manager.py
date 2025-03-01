import os

class FileManager:
    
    def read_file(file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception:
            return False
        
    def write_file(file_path, data):
        try:
            with open(file_path, "w") as file:
                file.write(data)
                return True
        except Exception as e:
            return e
        
    def append_file(file_path, data):
        try:
            with open(file_path, "a") as file:
                file.write("\n" + data) # Add a newline to it
                return True
        except Exception as e:
            return e
        
    def is_file_existed(file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False