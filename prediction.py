import sys
import pandas as pd
import joblib

model = joblib.load("model/attrition_model.joblib")
feature_columns = joblib.load("model/feature_columns.joblib")

THRESHOLD = 0.3


def predict(path):
    df = pd.read_csv(path)
    employee_id = df["EmployeeId"]

    df = df.drop(columns=["EmployeeId", "Attrition", "EmployeeCount", "Over18", "StandardHours"], errors="ignore")

    X = pd.get_dummies(df)
    X = X.reindex(columns=feature_columns, fill_value=0)

    proba = model.predict_proba(X)[:, 1]

    result = pd.DataFrame({
        "EmployeeId": employee_id,
        "attrition_proba": proba.round(3),
        "attrition_pred": (proba >= THRESHOLD).astype(int)
    })

    return result


if __name__ == "__main__":
    path = sys.argv[1]
    result = predict(path)
    result.to_csv("prediction_result.csv", index=False)
    print(result.head(10))
    print()
    print("Karyawan berisiko keluar:", result["attrition_pred"].sum(), "dari", len(result))