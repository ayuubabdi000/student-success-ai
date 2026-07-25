import os
import pandas as pd


# ===============================
# CONFIG
# ===============================

INPUT_PATH = "../dataset/Course_Completion_Prediction.csv"
OUTPUT_PATH = "../dataset/clean_Student.csv"


# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv(INPUT_PATH)

print("Original shape:", df.shape)


# ===============================
# REMOVE UNUSED COLUMNS
# ===============================

DROP_COLUMNS = [

    "Student_ID",
    "Name",
    "Gender",
    "Age",
    "Education_Level",
    "Employment_Status",
    "City",
    "Device_Type",
    "Internet_Connection_Quality",

    "Course_ID",
    "Category",
    "Course_Level",
    "CourseName",
    "Course_Duration_Days",

    "Instructor_Rating",

    "Payment_Mode",
    "Payment_Amount",
    "Discount_Used",
    "Fee_Paid",

    "Satisfaction_Rating",
    "Support_Tickets_Raised",

    "Enrollment_Date",
    "Progress_Percentage"

]


df = df.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)


# ===============================
# TARGET ENCODING
# ===============================

df["Completed"] = df["Completed"].map(
    {
        "Not Completed":0,
        "Completed":1
    }
)







# ===============================
# SAVE
# ===============================

# os.makedirs(
#     "./dataset",
#     exist_ok=True
# )


# df.to_csv(
#     OUTPUT_PATH,
#     index=False
# )



# print("\nClean dataset saved")
# print("Final shape:", df.shape)

# print("\nColumns:")
# print(df.columns.tolist())