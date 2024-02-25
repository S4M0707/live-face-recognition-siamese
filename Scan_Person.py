import streamlit as st
import os
from utils.Identify import IdentificationSystem
from utils.ImageHandeling import ImageHandle

class ScanPerson:
    def __init__(self):
        # Initialize ImageHandle and IdentificationSystem instances
        self.image_handle = ImageHandle(os.path.join('captured_images'))
        self.recognize = IdentificationSystem()

    def give_success(self, s):
        """
        Display a success message.

        Args:
        - s: Success message to be displayed.

        Returns:
        - None
        """
        st.success(s)

    def check_db_path(self):
        """
        Check if branch and section inputs are provided.

        Returns:
        - Boolean indicating whether branch and section are provided.
        """
        if not self.branch or not self.sec:
            return False
        return True

    def main_scanning(self):
        """
        Main function for scanning persons.

        Returns:
        - None
        """
        st.title("SCAN PERSONS")

        # Create a container to organize inputs and messages
        placeholder = st.empty()
        container = placeholder.container(border=True)

        # Input fields for state (branch) and city (section)
        self.branch = container.text_input("State").lower()
        self.sec = container.text_input("City").lower()

        # File uploader for uploading a photo
        uploaded_file = container.file_uploader(
            "Upload Photo", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        # Check if file is uploaded and branch and section are provided
        if uploaded_file is not None:
            if self.check_db_path():
                # Set branch and section paths, save uploaded file, and display success message
                self.image_handle.set_branch_sec_path(self.branch, self.sec)
                self.file_path = self.image_handle.save_uploaded_file(uploaded_file)
                container.success(f"Image saved Successfully")
            else:
                container.error("Each field is required.")
        
        # Button for database search
        if st.button("Database Search"):
            if uploaded_file is not None and self.check_db_path():
                placeholder.empty()
                self.recognize_update(self.file_path)
            else:
                st.error("Each field is required.")

    def recognize_update(self, file_path):
        """
        Recognize faces in the uploaded image and update the database.

        Args:
        - file_path: Path of the uploaded file.

        Returns:
        - None
        """
        branch_path = os.path.join(self.branch, self.sec)
        person_list, face_rect_list = self.recognize.recognize_faces(branch_path, file_path)
        self.recognize.update_database(person_list, face_rect_list, file_path)

scan_person = ScanPerson()
scan_person.main_scanning()
