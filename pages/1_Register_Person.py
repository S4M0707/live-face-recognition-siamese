import streamlit as st
import os
from utils.ImageHandeling import ImageHandle

class AddNewPerson:
    def __init__(self):
        # Initialize ImageHandle instance
        self.image_handle = ImageHandle(os.path.join('database'))

    def check_db_name_path(self):
        """
        Check if branch, section, and person name inputs are provided.

        Returns:
        - Boolean indicating whether all required fields are provided.
        """
        if not self.branch or not self.sec or not self.name:
            return False
        return True

    def render_page(self):
        """
        Render the registration page for adding a new person.

        Returns:
        - None
        """
        st.title("REGISTER PERSON")

        # Create a container to organize inputs and messages
        placeholder = st.empty()
        container = placeholder.container(border=True)

        # Input fields for person name, state (branch), and city (section)
        self.name = container.text_input("Person Name").lower()
        self.branch = container.text_input("State").lower()
        self.sec = container.text_input("City").lower()

        # Set branch/section path and person name path for saving images
        self.image_handle.set_branch_sec_path(self.branch, self.sec)
        self.image_handle.set_db_name_path(self.name)

        # File uploader for uploading a photo
        uploader_container = st.empty()
        uploaded_file = uploader_container.file_uploader(
            "Upload Person Solo Photo", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        # Check if file is uploaded and all required fields are provided
        if uploaded_file is not None:
            if self.check_db_name_path():
                # Save uploaded file and display success message
                self.image_handle.save_uploaded_file(uploaded_file)
                st.success(f"Image saved Successfully")
            else:
                st.error("Each field is required.")

        # Button for capturing live photo
        st.text("Capture Live Photo")
        if st.button("Use Camera"):
            # Clear placeholders, handle camera, and display success message
            if self.check_db_name_path():
                placeholder.empty()
                uploader_container.empty()
                self.image_handle.handle_camera()
                st.success(f"Image saved Successfully")
            else:
                st.error("Each field is required.")
                return

# Create an instance of AddNewPerson and render the registration page
person = AddNewPerson()
person.render_page()
