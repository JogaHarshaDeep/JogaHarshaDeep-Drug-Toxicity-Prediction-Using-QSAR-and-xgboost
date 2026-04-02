import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

df_qed = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\qed.csv")
df_topo = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\topological-descriptors.csv")
df_lip = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\Lipinski-descriptors.csv")
df_alert = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\alerts-descriptors.csv")
tox21 = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\tox21.csv")

merge_df = pd.merge(df_qed,df_topo,on = "smiles",how="inner")
merge_df = pd.merge(merge_df,df_lip,on = "smiles",how="inner")
merge_df = pd.merge(merge_df,df_alert,on="smiles",how="inner")
final_df = pd.merge(merge_df,tox21,how="inner",on="smiles")

data = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\tox21.csv")

nr_cols = [c for c in final_df.columns if "NR" in c]
sr_cols = [c for c in final_df.columns if "SR" in c]

final_df["tox"] = final_df[nr_cols + sr_cols].max(axis=1)
final_df = final_df.copy()

x = final_df.drop(columns=["tox", "smiles"] + nr_cols + sr_cols)
x = x.select_dtypes(include=["int64", "float64", "bool"])
y = final_df["tox"]
x = x.dropna(axis=1)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,random_state=42)
model = XGBClassifier(n_estimators=1300, max_depth=6, learning_rate=0.02,subsample=0.8,colsample_bytree=0.8,eval_metric="auc")
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
y_prob = model.predict_proba(x_test)[:, 1]
print(accuracy_score(y_test, y_pred))
print("AUC:", roc_auc_score(y_test, y_prob))

def get_level(pred, qed):
    pred = int(pred)  
    if pred == 0:
        return "Non-toxic"
    if qed < 0.3:
        return "High Toxic"
    elif qed < 0.6:
        return "Medium Toxic"
    else:
        return "Low Toxic"

results = []
for i in range(len(x_test)):
    pred = y_pred[i]
    qed = x_test.iloc[i]["QED"]

    level = get_level(pred, qed)
    results.append(level)

x_test = x_test.copy()
x_test["Predicted_Toxic"] = y_pred
x_test["Toxicity_Level"] = results
print(x_test[["QED", "Predicted_Toxic", "Toxicity_Level"]].head(20))