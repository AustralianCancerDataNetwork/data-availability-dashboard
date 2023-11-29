"""
Tasks to be run by celery
"""
import numpy as np
import pandas as pd

from .models import Centre, Patient
from .components.constants import data_availability_COLUMNS


def insert_data_availability_data():
    """
    Task to insert spreadsheet data into sqlite3 database
    """
    centres = pd.DataFrame(list(Centre.objects.all().values()))
    excel_file = pd.ExcelFile("data_availability_data.xlsx")
    for centre in list(centres["name"]):
        df_centre = excel_file.parse(centre)
        df_centre = df_centre.filter(items=data_availability_COLUMNS)
        centre_pats = []
        df_centre = df_centre.iloc[1:, :]
        for patient_row in df_centre.iterrows():
            # missing values for HPV status
            patient_row = list(patient_row[1])
            if isinstance(patient_row[7], float):
                patient_row[7] = None
            # convert hpv status to boolean
            elif isinstance(patient_row[7], str):
                patient_row[7] = patient_row[7] == "+"
            # missing values for age
            if np.isnan(patient_row[2]):
                patient_row[2] = None
            # cast age to int
            else:
                patient_row[2] = int(patient_row[2])
            patient = Patient(
                patient_id=patient_row[0],
                sex=patient_row[1],
                age=patient_row[2],
                primary_site=patient_row[3],
                t_stage=patient_row[4],
                n_stage=patient_row[5],
                m_stage=patient_row[6],
                hpv_status=patient_row[7],
            )
            patient.centre_name = Centre.objects.filter(name=centre).first()
            centre_pats = pd.concat([centre_pats, patient])
        Patient.objects.bulk_create(centre_pats)
