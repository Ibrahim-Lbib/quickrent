import os
import uuid
from flask import current_app

class StorageService:
    def __init__(self, upload_folder=None):
        self._upload_folder = upload_folder

    @property
    def upload_folder(self):
        if self._upload_folder:
            return self._upload_folder
        
        # Use current_app only when accessed, ensuring we're inside an app context
        folder = os.path.join(
            current_app.root_path, 'static', 'uploads', 'listings'
        )
        os.makedirs(folder, exist_ok=True)
        return folder

    def save_image(self, file):
        """
        Saves an image file with a unique name.
        Returns the filename.
        """
        if not file or not file.filename:
            return None
            
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(self.upload_folder, unique_name)
        
        file.save(filepath)
        return unique_name

    def delete_image(self, filename):
        """
        Deletes an image file from storage.
        """
        if not filename:
            return
            
        filepath = os.path.join(self.upload_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
