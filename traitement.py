import pandas as pd

def read_ds(ds_name: str):
    """
    Charge un fichier CSV de traces utilisateur (train ou test)
    et le convertit en DataFrame Pandas, en gérant les longueurs de lignes variables.
    """

    # Fichier à ouvrir (en minuscules)
    file_path = f"{ds_name.lower()}.csv"

    # Lecture manuelle du fichier (plus robuste que read_csv)
    with open(file_path, "r", encoding="utf-8") as f:
        lignes = f.readlines()

    data = []

    for ligne in lignes:
        ligne = ligne.strip()
        champs = ligne.split(",")  # délimiteur = virgule
        data.append(champs)

    if ds_name.lower() == "train":
        # TRAIN → contient l'utilisateur en 1re colonne
        df = pd.DataFrame(data)
        df.rename(columns={0: "util", 1: "navigateur"}, inplace=True)
        df["trace"] = df.iloc[:, 2:].apply(lambda x: ",".join(x.dropna().astype(str)), axis=1)
        df = df[["util", "navigateur", "trace"]]

    else:
        # TEST → ne contient pas la colonne utilisateur
        df = pd.DataFrame(data)
        df.rename(columns={0: "navigateur"}, inplace=True)
        df["trace"] = df.iloc[:, 1:].apply(lambda x: ",".join(x.dropna().astype(str)), axis=1)
        df = df[["navigateur", "trace"]]

    return df

if __name__ == "__main__":
    features_train = read_ds("train")
    features_test = read_ds("test")

    # Quelques vérifications
    print(features_train.shape, features_test.shape)
    print(features_train.head())