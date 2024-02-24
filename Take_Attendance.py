import streamlit as st
import os
import datetime
import Identify

def giveSuccess(s):
    st.success(s)

def create_file(uploaded_file, save_path):
    time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    file_name = f'{time}.{uploaded_file.name.split(".")[-1]}'

    file_path = os.path.join('captured_images', save_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_path = os.path.join(file_path, file_name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    giveSuccess(f"File '{file_name}' uploaded'")
    return file_path

def take_attendance():
    st.title("ATTENDANCE")

    branch = st.text_input("Course Branch")
    branch = branch.upper()

    sec = st.text_input("Course Section")
    sec = sec.upper()

    uploaded_file = st.file_uploader(
        "Upload Classroom Image", 
        type = ["jpg", "jpeg", "png", "HEIC"]
        )

    if uploaded_file is None or not branch or not sec:
        st.error("Each field is required.")
        return
    
    branch_path = os.path.join(branch, sec)
    file_path = create_file(uploaded_file, branch_path)

    if st.button("Take Attendance"):
        Identify.recognize(branch_path, file_path)

take_attendance()