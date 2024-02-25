import streamlit as st
import os
from utils.ImageHandeling import ImageHandle

class AddNewPerson:
    def __init__(self):
        self.image_handle = ImageHandle(os.path.join('database'))

    def check_db_name_path(self):
        if not self.branch or not self.sec or not self.name:
            return False
        return True

    def render_page(self):
        """
        Render the Streamlit page for adding a new person.
        """
        st.title("Add a New Person")

        # Container for input fields
        placeholder = st.empty()
        container = placeholder.container(border=True)

        self.name = container.text_input("Enter Person Name").lower()
        self.branch = container.text_input("Course Branch").lower()
        self.sec = container.text_input("Course Section").lower()

        self.image_handle.set_branch_sec_path(self.branch, self.sec)
        self.image_handle.set_db_name_path(self.name)

        # File uploader for uploading a solo photo
        uploader_container = st.empty()
        uploaded_file = uploader_container.file_uploader(
            "Upload Person Solo Photo", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        # Handle file upload
        if uploaded_file is not None:
            if self.check_db_name_path():
                self.image_handle.save_uploaded_file(uploaded_file)
                st.success(f"Image saved Successfully")
            else:
                st.error("Each field is required.")

        # Button to capture live photo
        st.text("Capture Live Photo")
        if st.button("Use Camera"):
            if self.check_db_name_path():
                placeholder.empty()
                uploader_container.empty()
                self.image_handle.handle_camera()
                st.success(f"Image saved Successfully")
            else:
                st.error("Each field is required.")
                return
        
person = AddNewPerson()
person.render_page()
