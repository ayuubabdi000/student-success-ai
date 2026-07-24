import os
import joblib
import pandas as pd


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score
)



# ===============================
# CONFIG
# ===============================

DATA_PATH = "../dataset/clean_Student.csv"

MODEL_DIR = "../models"

RANDOM_STATE = 42

FINAL_K = 5



os.makedirs(
    MODEL_DIR,
    exist_ok=True
)



# ===============================
# FEATURES FOR CLUSTERING
# ===============================

FEATURES = [

    "Login_Frequency",

    "Average_Session_Duration_Min",

    "Video_Completion_Rate",

    "Discussion_Participation",

    "Time_Spent_Hours",

    "Days_Since_Last_Login",

    "Notifications_Checked",

    "Peer_Interaction_Score",

    "Assignments_Submitted",

    "Assignments_Missed",

    "Quiz_Attempts",

    "Quiz_Score_Avg",

    "Project_Grade",

    "Rewatch_Count",

    "App_Usage_Percentage",

    "Reminder_Emails_Clicked",


]



# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv(
    DATA_PATH
)


print(
    "Dataset:",
    df.shape
)



X = df[FEATURES].copy()



# ===============================
# OUTLIER CAPPING
# ===============================

def iqr_cap(data):

    data = data.copy()

    for col in data.columns:


        q1 = data[col].quantile(
            0.25
        )

        q3 = data[col].quantile(
            0.75
        )


        iqr = q3 - q1


        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr


        data[col] = data[col].clip(
            lower,
            upper
        )


    return data



X = iqr_cap(X)



# ===============================
# SCALING
# ===============================


scaler = StandardScaler()


X_scaled = scaler.fit_transform(
    X
)



# ===============================
# FIND BEST K
# ===============================


print("\nK SEARCH")


for k in range(2,9):


    model = KMeans(

        n_clusters=k,

        random_state=RANDOM_STATE,

        n_init="auto"

    )


    labels = model.fit_predict(
        X_scaled
    )



    sil = silhouette_score(
        X_scaled,
        labels
    )


    db = davies_bouldin_score(
        X_scaled,
        labels
    )



    print(
        f"K={k} | "
        f"Silhouette={sil:.3f} | "
        f"DB={db:.3f}"
    )



# ===============================
# FINAL MODEL
# ===============================


kmeans = KMeans(

    n_clusters=FINAL_K,

    random_state=RANDOM_STATE,

    n_init="auto"

)



clusters = kmeans.fit_predict(
    X_scaled
)



df["Cluster"] = clusters



# ===============================
# CLUSTER PROFILES
# ===============================


print(
    "\nCluster Profiles"
)


profiles = (

    df.groupby("Cluster")[FEATURES]
    .mean()
    .round(2)

)


print(
    profiles
)



profiles.to_csv(

    f"{MODEL_DIR}/cluster_profiles.csv"

)



# ===============================
# SAVE MODELS
# ===============================


joblib.dump(

    kmeans,

    f"{MODEL_DIR}/student_cluster_model.pkl"

)


joblib.dump(

    scaler,

    f"{MODEL_DIR}/student_scaler.pkl"

)


joblib.dump(

    FEATURES,

    f"{MODEL_DIR}/cluster_features.pkl"

)



# ===============================
# SAVE DATA
# ===============================


df.to_csv(

    "../dataset/student_clustered.csv",

    index=False

)



print(
    "\nClustering completed"
)

print(
    "Models saved"
)