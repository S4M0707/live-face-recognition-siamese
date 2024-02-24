from deepface import DeepFace
import os
import pandas as pd
import streamlit as st

def save_to_db(person_list, file_path):
    file_path = os.path.split(file_path)[-1]
    time = file_path.split('.')[0]
    date = time.split('-')[0]
    time = time.split('-')[1]

    df_new = pd.DataFrame({'Person' : person_list, 'date' : date, 'time' : time})
    df = pd.read_csv('attendance.csv')
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_csv('attendance.csv', index=False)

    return df

def show_attendance(data):
    st.text("Students Present:\n")
    st.write(data)

def recognize(branch_path, file_path):
    reference_path = os.path.join('database', branch_path)

    recognition = DeepFace.find(file_path, reference_path, detector_backend='retinaface')

    person_list = []
    for person in recognition:
        person_path = person.identity[0]
        person_path = os.path.split(person_path)[0]
        person_path = os.path.split(person_path)[-1]
        person_list.append(person_path)
    
    data = save_to_db(person_list, file_path)
    show_attendance(data)