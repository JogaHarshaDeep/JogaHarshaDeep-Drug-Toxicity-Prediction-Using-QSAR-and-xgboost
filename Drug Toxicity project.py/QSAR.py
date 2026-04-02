import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Chem import QED

data = pd.read_csv(r"D:\.vscode\.venv\Drug Toxicity project.py\tox21.csv")
data = data.dropna(subset=["smiles"])
Smilesl = data["smiles"]

#tological descriptors
def topological_descriptors(Smiles):
    mol = Chem.MolFromSmiles(Smiles)
    if mol is None:
        return None
    return{
        "TPSA" : Descriptors.TPSA(mol),
        "ROTB" : Descriptors.NumRotatableBonds(mol),
        "AROM" : Descriptors.NumAromaticRings(mol)
    }

desc_data = []
valid_index1 = []
valid_smiles = []
for i, s in enumerate(Smilesl):
    d = topological_descriptors(s)
    if d is not None:
        desc_data.append(d)
        valid_index1.append(i)
        valid_smiles.append(s)

df_topo = pd.DataFrame(desc_data)
df_topo.insert(0, "smiles", valid_smiles)
df_topo.to_csv("topological-descriptors.csv", index=False)
print(df_topo.head())

#lipinski descriptors
def lipinski_Descriptors(Smiles):
    mol = Chem.MolFromSmiles(Smiles)
    if mol is None:
        return None
    return {
        "MOLw" : Descriptors.MolWt(mol),
        "HBA"  : Descriptors.NumHAcceptors(mol),
        "HBD"  : Descriptors.NumHDonors(mol),
        "logp" : Descriptors.MolLogP(mol)
    }

df_data = []
valid_index2 = []
valid_smiles = []
for i, s in enumerate(Smilesl):
    d = lipinski_Descriptors(s)
    if d is not None:
        df_data.append(d)
        valid_index2.append(i)
        valid_smiles.append(s)

df_lipi = pd.DataFrame(df_data)
df_lipi.insert(0, "smiles", valid_smiles)
df_lipi.to_csv("Lipinski-descriptors.csv", index=False)
print(df_lipi.head())

#Alert Descriptors
params = FilterCatalogParams()
params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
params.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
catalog = FilterCatalog(params)
alerts_list = [catalog.GetEntry(i).GetDescription() for i in range(catalog.GetNumEntries())]

def cal_alerts(Smiles):
    mol = Chem.MolFromSmiles(Smiles)
    if mol is None:
        return None
    result = {name:0 for name in alerts_list}
    matches = catalog.GetMatches(mol)

    for k in matches:
        result[k.GetDescription()] = 1
    
    return result

alert_data = []
valid_index3 = []
valid_smiles = []
for i, s in enumerate(Smilesl):
    d = cal_alerts(s)
    if d is not None:
        alert_data.append(d)
        valid_index3.append(i)
        valid_smiles.append(s)

df_alerts = pd.DataFrame(alert_data)
df_alerts.insert(0, "smiles", valid_smiles)
df_alerts.to_csv("alerts-descriptors.csv", index=False)
print(df_alerts.head())

qed_values = []

for sm in Smilesl:
    mol = Chem.MolFromSmiles(sm)
    if mol:
        qed_values.append(QED.qed(mol))
    else:
        qed_values.append(None)

data['QED'] = qed_values
qed_df = data[['smiles', 'QED']]
qed_df.to_csv("qed.csv", index=False)
