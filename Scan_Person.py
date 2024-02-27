import streamlit as st
import os
from utils.Identify import IdentificationSystem
from utils.ImageHandeling import ImageHandle
import cv2
from PIL import Image

class ScanPerson:
    def __init__(self):
        # Initialize ImageHandle and IdentificationSystem instances
        self.image_handle = ImageHandle(os.path.join('captured_images'))
        self.recognize = IdentificationSystem()
        self.selected_option = None
        self.options = ["Fastest", "Middle", "Most Accurate"]

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

        selected_option = container.selectbox(
            "Select Processing Model:", 
            self.options,
        )
        self.on_select_change(selected_option)

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
        
        if self.selected_option == 'Fastest':
            # Button for capturing live photo
            st.text("Scan Live Feed")
            if st.button("Use Camera"):
                # Clear placeholders, handle camera, and display success message
                if self.check_db_path():
                    placeholder.empty()
                    self.live_scan()
                else:
                    st.error("Each field is required.")
                    return
        
        # Button for database search
        if st.button("Database Search"):
            if uploaded_file is not None and self.check_db_path():
                placeholder.empty()
                self.recognize_update(self.file_path)
            else:
                st.error("Each field is required.")

    def live_scan(self):
        capture = cv2.VideoCapture(0)

        if not capture.isOpened():
            st.error("Unable to access the camera. Please make sure it is connected and not in use by another application.")
            return

        img_contain = st.empty()
        update_frequency = 4
        frame_buffer = []
        
        while True:
            ret, img = capture.read()

            if not ret:
                break

            frame_buffer.append(img)

            if len(frame_buffer) >= update_frequency:
                latest_frame = frame_buffer[-1]
                frame_buffer = []
            
                img = latest_frame
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                branch_path = os.path.join(self.branch, self.sec)
                person_list, face_rect_list = self.recognize.recognize_faces(branch_path, img = img)
                if len(person_list) <= 0:
                    img_contain.image(img, caption='Face with Rectangle and Name', use_column_width=True)
                    continue
                for idx, rect in enumerate(face_rect_list):
                    x = rect['x']
                    y = rect['y']
                    w = rect['w']
                    h = rect['h']

                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    name = person_list[idx]
                    text_location = (x, y + h + 20)
                    font_scale = 1
                    cv2.putText(img, name, text_location, cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_scale * 2)
                
                image_pil = Image.fromarray(img)

                img_contain.image(image_pil, caption='Face with Rectangle and Name', use_column_width=True)

        capture.release()
        cv2.destroyAllWindows()

    def recognize_update(self, file_path):
        """
        Recognize faces in the uploaded image and update the database.

        Args:
        - file_path: Path of the uploaded file.

        Returns:
        - None
        """
        branch_path = os.path.join(self.branch, self.sec)
        person_list, face_rect_list = self.recognize.recognize_faces(branch_path, file_path = file_path)
        if len(person_list) <= 0:
            st.write('No faces found')
            return
        self.recognize.update_database(person_list, face_rect_list, file_path)

    def on_select_change(self, option):
        self.selected_option = option
        self.recognize.receive_backend(option)


scan_person = ScanPerson()
scan_person.main_scanning()
