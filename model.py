import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import os

# ── Encoding maps ────────────────────────────────────────────────
CAT_MAP = {"A": 1, "B": 2, "C": 3, "D": 4}
CONF_MAP = {"Not confident at all": 1, "Somewhat confident": 2, "Very confident": 3}

BTECH_FEATURES = [
    "Q2_Confidence", "Q3_ClubChoice", "Q4_DecisionStyle",
    "Q5_CodingReaction", "Q6_DesignReaction", "Q7_HackingReaction",
    "Q8_DataReaction", "Q9_CloudReaction", "Q10_CodeVsDesign",
    "Q11_HackVsBuild", "Q12_BuildVsSecure", "Q13_DataVsDesign",
    "Q14_FeatureVsScale", "Q15_MathsRating", "Q16_CreativeRating"
]

BCOM_FEATURES = [
    "Q2_Confidence", "Q3_ClubChoice", "Q4_DecisionStyle",
    "Q5_MoneyBudgets", "Q6_ConvincingSelling", "Q7_OwnBusiness",
    "Q8_ManagingTeams", "Q9_AnalyzingData", "Q10_StockMarkets",
    "Q11_CampaignsBranding", "Q12_DataOverGut", "Q13_BusinessReaction",
    "Q14_ManageVsAnalyze", "Q15_StartupVsCFO", "Q16_MarketingVsFinance"
]

def encode_df(df, features):
    df = df.copy()
    for col in features:
        if df[col].dtype == object:
            if col == "Q2_Confidence":
                df[col] = df[col].map(CONF_MAP)
            else:
                df[col] = df[col].map(CAT_MAP)
    return df[features]

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "KNN":           KNeighborsClassifier(n_neighbors=5),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    trained = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        results[name] = round(acc * 100, 2)
        trained[name] = model

    best_name = max(results, key=results.get)
    return trained, results, best_name, trained[best_name]

def load_and_train():
    data_path = os.path.join(os.path.dirname(__file__), "Career_Prediction_Dataset.xlsx")
    df_btech = pd.read_excel(data_path, sheet_name="BTech_Data")
    df_bcom  = pd.read_excel(data_path, sheet_name="BCom_Data")

    # BTech
    X_bt = encode_df(df_btech, BTECH_FEATURES)
    y_bt = df_btech["Specialization"]
    bt_models, bt_results, bt_best_name, bt_best = train_models(X_bt, y_bt)

    # BCom
    X_bc = encode_df(df_bcom, BCOM_FEATURES)
    y_bc = df_bcom["Specialization"]
    bc_models, bc_results, bc_best_name, bc_best = train_models(X_bc, y_bc)

    # Save best models
    with open(os.path.join(os.path.dirname(__file__), "btech_model.pkl"), "wb") as f:
        pickle.dump(bt_best, f)
    with open(os.path.join(os.path.dirname(__file__), "bcom_model.pkl"), "wb") as f:
        pickle.dump(bc_best, f)

    return {
        "btech": {"results": bt_results, "best": bt_best_name},
        "bcom":  {"results": bc_results, "best": bc_best_name},
    }

def predict_btech(answers: dict):
    """answers = {feature_name: encoded_int, ...}"""
    with open(os.path.join(os.path.dirname(__file__), "btech_model.pkl"), "rb") as f:
        model = pickle.load(f)
    row = pd.DataFrame([answers])[BTECH_FEATURES]
    return model.predict(row)[0], model.predict_proba(row)[0].max() * 100

def predict_bcom(answers: dict):
    with open(os.path.join(os.path.dirname(__file__), "bcom_model.pkl"), "rb") as f:
        model = pickle.load(f)
    row = pd.DataFrame([answers])[BCOM_FEATURES]
    return model.predict(row)[0], model.predict_proba(row)[0].max() * 100

if __name__ == "__main__":
    print("Training models...")
    info = load_and_train()
    print("\n── BTech Results ──")
    for m, acc in info["btech"]["results"].items():
        star = " ✓ BEST" if m == info["btech"]["best"] else ""
        print(f"  {m}: {acc}%{star}")
    print("\n── BCom Results ──")
    for m, acc in info["bcom"]["results"].items():
        star = " ✓ BEST" if m == info["bcom"]["best"] else ""
        print(f"  {m}: {acc}%{star}")
    print("\nModels saved successfully!")