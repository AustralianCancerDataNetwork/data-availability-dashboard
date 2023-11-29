""" Constant values for the dashboard
"""

# list of features we are interested in for the Head and Neck dashboard
data_availability_COLUMNS = [
    "Patient #",
    "Sex",
    "Age",
    "Primary Site",
    "T-stage",
    "N-stage",
    "M-stage",
    "HPV status",
]

QUERY_MEDICAL_TABLE = "SELECT * FROM Medical"
QUERY_MEDICAL_TABLE_CATEGORIES = "SELECT DISTINCT Category FROM Medical"

FEATURE_TYPES = (
    ("continuous", "CONTINUOUS"),
    ("categorical", "CATEGORICAL"),
)
