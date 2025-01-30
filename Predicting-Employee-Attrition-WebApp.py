import numpy as np
import pandas as pd
import pickle
import streamlit as st

# Load the trained model
load_model = pickle.load(open('employee-predict-model.sav', 'rb'))

# Define categorical mappings (adjust based on your dataset's encoding)
gender_map = {'Male': 0, 'Female': 1, 'Other': 2}
relevent_experience_map = {'No': 0, 'Yes': 1}
enrolled_university_map = {'no_enrollment': 0, 'Full time course': 1, 'Part time course': 2}
education_level_map = {'Primary School': 0, 'High School': 1, 'Graduate': 2, 'Masters': 3, 'PhD': 4}
company_size_map = {'<10': 0, '10-50': 1, '50-100': 2, '100-500': 3, '500-1000': 4, '1000-5000': 5, '5000+': 6}
company_type_map = {'Private': 0, 'Public': 1, 'Government': 2, 'NGO': 3, 'Other': 4}
last_new_job_map = {'never': 0, '1': 1, '2': 2, '3': 3, '4': 4, '>4': 5}

# Prediction function
def predict_new_data(input_data):
    try:
        # Convert inputs to correct types
        input_data = [
            float(input_data[0]),  # city_development_index
            gender_map.get(input_data[1], -1),  # gender
            relevent_experience_map.get(input_data[2], -1),  # relevent_experience
            enrolled_university_map.get(input_data[3], -1),  # enrolled_university
            education_level_map.get(input_data[4], -1),  # education_level
            float(input_data[5]) if input_data[5] else -1,  # experience (handle empty)
            company_size_map.get(input_data[6], -1),  # company_size
            company_type_map.get(input_data[7], -1),  # company_type
            last_new_job_map.get(input_data[8], -1),  # last_new_job
            float(input_data[9]) if input_data[9] else -1  # training_hours
        ]

        # Convert to DataFrame
        input_df = pd.DataFrame([input_data], columns=[
            'city_development_index', 'gender', 'relevent_experience', 'enrolled_university',
            'education_level', 'experience', 'company_size', 'company_type',
            'last_new_job', 'training_hours'
        ])

        # Make the prediction
        prediction = load_model.predict(input_df)
        result = prediction[0]

        return 'He/she Will Stay' if result == 0 else 'He/She will Leave'
    
    except Exception as e:
        return f"Error: {e}"


# Streamlit UI
def main():
    st.title('Prashanth Pvt ltds - Predicting Employee Attrition')

    city_development_index = st.text_input('City Development Index (float)')
    gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
    relevent_experience = st.selectbox('Relevant Experience', ['No', 'Yes'])
    enrolled_university = st.selectbox('Enrolled University', ['no_enrollment', 'Full time course', 'Part time course'])
    education_level = st.selectbox('Education Level', ['Primary School', 'High School', 'Graduate', 'Masters', 'PhD'])
    experience = st.text_input('Years of Experience (float)')
    company_size = st.selectbox('Company Size', ['<10', '10-50', '50-100', '100-500', '500-1000', '1000-5000', '5000+'])
    company_type = st.selectbox('Company Type', ['Private', 'Public', 'Government', 'NGO', 'Other'])
    last_new_job = st.selectbox('Years Since Last Job Change', ['never', '1', '2', '3', '4', '>4'])
    training_hours = st.text_input('Training Hours (float)')

    Analysisresults = ''

    if st.button('Analyze Employee Details'):
        Analysisresults = predict_new_data([
            city_development_index, gender, relevent_experience, enrolled_university, 
            education_level, experience, company_size, company_type, last_new_job, training_hours
        ])

    st.success(Analysisresults)


if __name__ == '__main__':
    main()
