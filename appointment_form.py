import streamlit as st
import re
from dateutil import parser
import csv
import os

def extract_date_from_text(text):
    try:
        date = parser.parse(text, fuzzy=True)
        return date.strftime("%Y-%m-%d")
    except:
        return None

def is_valid_email(email):
    return re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)

def is_valid_phone(phone):
    return re.match(r"^\+?[0-9]{7,15}$", phone)

def save_appointment(name, email, phone, date):
    csv_file = "appointments.csv"
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Email", "Phone", "Date"])
        writer.writerow([name, email, phone, date])

def show_appointment_form():
    st.subheader(" Book an Appointment")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    appointment_date_input = st.text_input("Preferred Date (e.g. Next Monday, June 25)")

    extracted_date = extract_date_from_text(appointment_date_input)

    if st.button("Submit Appointment Request"):
        if not name or not email or not phone or not appointment_date_input:
            st.error("Please fill in all fields.")
        elif not is_valid_email(email):
            st.error("Invalid email address.")
        elif not is_valid_phone(phone):
            st.error("Invalid phone number.")
        elif not extracted_date:
            st.error("Couldn't extract a valid date. Try something like 'June 25, 2025'")
        else:
            save_appointment(name, email, phone, extracted_date)
            st.success(f"Appointment booked for {name} on {extracted_date}")
            st.info(f"Contact Info: {email}, {phone}")
