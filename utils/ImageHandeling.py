import os
import datetime
import cv2
import streamlit as st
from utils.Identify import IdentificationSystem

class ImageHandle:
    def __init__(self, output_path) -> None:
        """
        Initialize ImageHandle object.

        Args:
        - output_path: Path to the output directory.

        Returns:
        - None
        """
        self.face_detection = IdentificationSystem().face_detected
        self.database_path = output_path
    
    def set_branch_sec_path(self, branch, sec):
        """
        Set the path for the branch and section.

        Args:
        - branch: Branch name.
        - sec: Section name.

        Returns:
        - None
        """
        if branch is None or sec is None:
            return
        self.branch_sec_path = os.path.join(self.database_path, branch, sec)
    
    def set_db_name_path(self, name):
        """
        Set the path for the database name.

        Args:
        - name: Database name.

        Returns:
        - None
        """
        if name is None:
            return
        self.db_name_path = os.path.join(self.branch_sec_path, name)
    
    def save_uploaded_file(self, uploaded_file):
        """
        Save the uploaded file to the output directory.

        Args:
        - uploaded_file: Uploaded file object.

        Returns:
        - File path of the saved file.
        """
        time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        file_name = f'{time}.{uploaded_file.name.split(".")[-1]}'

        self.create_directories()
        file_path = os.path.join(
            self.db_name_path if self.database_path == 'database' else self.branch_sec_path, 
            file_name
            )
        
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())
        return file_path
    
    def handle_camera(self):
        """
        Capture image from camera and save it to the output directory.

        Returns:
        - None
        """
        self.create_directories()
        self.capture_image()
    
    def create_directories(self):
        """
        Create directories for storing images.

        Returns:
        - None
        """
        curr_pth = self.db_name_path if self.database_path == 'database' else self.branch_sec_path
        if not os.path.exists(curr_pth):
            os.makedirs(curr_pth)

    def capture_image(self):
        """
        Capture image from camera.

        Returns:
        - None
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
        Save captured image to the output directory.

        Args:
        - image: Captured image as a numpy array.

        Returns:
        - None
        """
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        image_path = os.path.join(
            self.db_name_path if self.database_path == 'database' else self.branch_sec_path, 
            f"{time}.jpg"
            )
        cv2.imwrite(image_path, image)