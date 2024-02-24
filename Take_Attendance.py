import streamlit as st
import os
import datetime
from utils.Identify import AttendanceSystem

class AttendanceTaker:
    def __init__(self):
        pass

    def give_success(self, s):
        """
        Display a success message.

        Args:
        - s: Success message to be displayed.

        Returns:
        - None
        """
        st.success(s)

    def create_file(self, uploaded_file, save_path):
        """
        Create a file from the uploaded file buffer and save it to the specified path.

        Args:
        - uploaded_file: Uploaded file object.
        - save_path: Path where the file should be saved.

        Returns:
        - File path of the saved file.
        """
        time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        file_name = f'{time}.{uploaded_file.name.split(".")[-1]}'

        file_path = os.path.join('captured_images', save_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_path = os.path.join(file_path, file_name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        self.give_success(f"File '{file_name}' uploaded'")
        return file_path

    def take_attendance(self):
        """
        Main function for taking attendance.

        Returns:
        - None
        """
        st.title("ATTENDANCE")
        branch = st.text_input("Course Branch").lower()
        sec = st.text_input("Course Section").lower()
        uploaded_file = st.file_uploader(
            "Upload Classroom Image", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        if uploaded_file is None or not branch or not sec:
            st.error("Each field is required.")
            return
        
        branch_path = os.path.join(branch, sec)
        file_path = self.create_file(uploaded_file, branch_path)

        if st.button("Take Attendance"):
            self.recognize_and_update_attendance(branch_path, file_path)

    def recognize_and_update_attendance(self, branch_path, file_path):
        recognize = AttendanceSystem()
        person_list = recognize.recognize_faces(branch_path, file_path)
        recognize.update_attendance(person_list, file_path)

attendance_taker = AttendanceTaker()
attendance_taker.take_attendance()
