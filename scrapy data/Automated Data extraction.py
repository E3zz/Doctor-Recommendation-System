import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_info(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    data = []
    # selectinng the whole class
    for g in soup.select(".eye-specialist"):
        doctor_name = g.h2.get_text(strip=True)

        # Check if the element exists before calling get_text
        doctor_specialty_element = g.select_one('p.mb-1')
        doctor_specialty = doctor_specialty_element.get_text(strip=True) if doctor_specialty_element else None

        doctor_degree_element = g.select_one('p.text-truncate')
        doctor_degree = doctor_degree_element.get_text(strip=True) if doctor_degree_element else None

        doctor_waiting_element = g.select_one('span.od-wte')
        doctor_waiting = doctor_waiting_element.get_text(strip=True) if doctor_waiting_element else None

        doctor_experience_elements = g.select(".item:not(:-soup-contains('Wait Time')) span")
        doctor_experience_text = ''.join([element.get_text(strip=True) for element in doctor_experience_elements])

        # Extract the whole experience information
        experience_info_match = re.search(r'(\d+ Years)', doctor_experience_text)
        experience_years = experience_info_match.group(1) if experience_info_match else None

        total_patients_element = g.select_one('span.d-inline-block')
        number_of_patients = re.search(r'\((\d+)\)', total_patients_element.get_text(strip=True)).group(
            1) if total_patients_element else None

        satisfaction_elements = g.select('span.od-wte')
        satisfaction_level_match = re.search(r'(\d+)%', ''.join(
            [element.get_text(strip=True) for element in satisfaction_elements]))
        satisfaction_level = satisfaction_level_match.group(1) if satisfaction_level_match else None

        doctor_fee_element = g.select_one(
            '.listing-locations:not(:-soup-contains("Online Video Consultation")) span.doctor-fee')
        fees = doctor_fee_element.get_text(strip=True) if doctor_fee_element else None

        hospitals_elements = g.select(".listing-locations:not(:-soup-contains('Online Video Consultation')) span")
        hospital_name = hospitals_elements[0].text if hospitals_elements else "Not Available"

        data.append({
            "Doctor Name": doctor_name,
            "Specialty": doctor_specialty,
            "Degree": doctor_degree,
            "Experience": experience_years,
            "Number Of Patients": number_of_patients,
            "Satisfaction level": satisfaction_level,
            "Fees": fees,
            "Waiting": doctor_waiting,
            "Hospital Name": hospital_name
        })

    df = pd.DataFrame(data)
    return df


# The inital URl for the web

base_url = "https://oladoc.com/pakistan/lahore/eye-specialist/{}"
combined_info = pd.DataFrame()

# The for loop is for changing the url
for i in range(10, 150, 10):
    current_url = base_url.format(i)
    print(current_url)
    # Calling the the function 
    current_info = get_info(current_url)
    # merging the data to create
    if i == 0:
        combined_info = current_info
    else:
        combined_info = pd.concat([combined_info, current_info], ignore_index=True)
# Now, the combined_info dataframe contains information from all the generated URLs


eye_specialist_data = combined_info.dropna(axis=0).copy()

with pd.ExcelWriter('Location') as writer:
    Dermatologist_data.to_excel(writer, sheet_name='Dermatologist Data')
    gynecologist_data.to_excel(writer, sheet_name='Gynecologist Data')
    pediatrician_data.to_excel(writer, sheet_name='Pediatrician Data')
    orthopedic_data.to_excel(writer, sheet_name='Orthopedic Data')
    ent_data.to_excel(writer, sheet_name='ENT Data')
    diabetologist_data.to_excel(writer, sheet_name='Diabetologist Data')
    eye_specialist_data.to_excel(writer, sheet_name='Eye Specialist Data')
