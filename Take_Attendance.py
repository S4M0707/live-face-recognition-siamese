import streamlit as st
import os
import datetime
from utils.Identify import AttendanceSystem
from utils.ImageHandeling import ImageHandle

class AttendanceTaker:
    def __init__(self):
        self.image_handle = ImageHandle(os.path.join('captured_images'))
        self.recognize = AttendanceSystem()

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
        if not self.branch or not self.sec:
            return False
        return True

    def take_attendance(self):
        """
        Main function for taking attendance.

        Returns:
        - None
        """
        st.title("ATTENDANCE")

        placeholder = st.empty()
        container = placeholder.container(border=True)

        self.branch = container.text_input("Course Branch").lower()
        self.sec = container.text_input("Course Section").lower()

        uploaded_file = container.file_uploader(
            "Upload Classroom Image", 
            type=["jpg", "jpeg", "png", "HEIC"]
        )

        if uploaded_file is not None:
            if self.check_db_path():
                self.image_handle.set_branch_sec_path(self.branch, self.sec)
                self.file_path = self.image_handle.save_uploaded_file(uploaded_file)
                container.success(f"Image saved Successfully")
            else:
                container.error("Each field is required.")
        
        if st.button("Take Attendance"):
            if uploaded_file is not None and self.check_db_path():
                placeholder.empty()
                self.recognize_and_update_attendance(self.file_path)
            else:
                st.error("Each field is required.")

    def recognize_and_update_attendance(self, file_path):
        branch_path = os.path.join(self.branch, self.sec)
        person_list, face_rect_list = self.recognize.recognize_faces(branch_path, file_path)
        self.recognize.update_attendance(person_list, face_rect_list, file_path)

attendance_taker = AttendanceTaker()
attendance_taker.take_attendance()
