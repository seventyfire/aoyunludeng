class Material:
    def __init__(self, file_obj, filename, upload_folder, type=0, filesize=0):
        self.file_obj = file_obj
        self.filename = filename
        self.upload_folder = upload_folder
        self.type = type
        self.filesize = filesize

    def save(self):
        import os
        self.file_obj.save(os.path.join(self.upload_folder, self.filename))
