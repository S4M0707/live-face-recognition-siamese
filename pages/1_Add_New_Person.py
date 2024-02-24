import streamlit as st
import cv2
import os
import datetime
from utils.Identify import AttendanceSystem

class AddNewPerson:
    def __init__(self):
        self.face_detection = AttendanceSystem().face_detected

    def render_page(self):
        """
        Render the Streamlit page for adding a new person.
        """
        st.title("Add a New Person")

        # Container for input fields
        placeholder = st.empty()
        container = placeholder.container(border=True)

        name = container.text_input("Enter Person Name").lower()
        branch = container.text_input("Course Branch").lower()
        sec = container.text_input("Course Section").lower()

        self.database_path = os.path.join('database', branch, sec, name)

        # File uploader for uploading a solo photo
        uploader_container = st.empty()
        uploaded_file = uploader_container.file_uploader(
            "Upload Person Solo Photo", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        # Handle file upload
        if uploaded_file is not None:
            if not name or not branch or not sec:
                st.error("Each field is required.")
                return
            self.save_uploaded_file(uploaded_file)

        # Button to capture live photo
        st.text("Capture Live Photo")
        if st.button("Use Camera"):
            self.handle_camera(name, branch, sec)
            placeholder.empty()
            uploader_container.empty()

    def save_uploaded_file(self, uploaded_file):
        """
        Save the uploaded file to the appropriate directory.

        Args:
        - uploaded_file: The uploaded file object.
        """
        time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        file_name = f'{time}.{uploaded_file.name.split(".")[-1]}'
        file_path = os.path.join(self.database_path, file_name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())
            st.success(f"Image saved Successfully")
        
    def handle_camera(self, name, branch, sec):
        """
        Handle the live photo capture using the camera.

        Args:
        - name: Person's name.
        - branch: Course branch.
        - sec: Course section.
        """
        if not name or not branch or not sec:
            st.error("Each field is required.")
            return
        self.create_directories()
        self.capture_image()

    def create_directories(self):
        """
        Create directories if they don't exist.
        """
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_path)

    def capture_image(self):
        """
        Capture a live photo using the camera.
        """
        capture = cv2.VideoCapture(0)

        if not capture.isOpened():
            st.error("Unable to access the camera. Please make sure it is connected and not in use by another application.")
            return

        img_contain = st.empty()
        t = 15
        update_frequency = 2
        frame_buffer = []
        
        while t > 0:
            ret, img = capture.read()

            if not ret:
                break

            if self.face_detection(img):
                t -= 1

            frame_buffer.append(img)

            if len(frame_buffer) >= update_frequency:
                latest_frame = frame_buffer[-1]
                img_contain.image(latest_frame, channels="BGR")
                frame_buffer = []

        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_contain.image(img, caption="Captured Image", use_column_width=True)
            self.save_image(img)
        else:
            st.warning("No Image Captured")

        capture.release()
        cv2.destroyAllWindows()

    def save_image(self, image):
        """
        Save the captured image to the appropriate directory.

        Args:
        - image: The captured image.
        """
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        image_path = os.path.join(self.database_path, f"{time}.jpg")
        cv2.imwrite(image_path, image)
        st.success(f"Image saved Successfully")

# Instantiate and render the AddNewPerson class
person = AddNewPerson()
person.render_page()
