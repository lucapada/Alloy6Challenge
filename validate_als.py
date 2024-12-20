import requests
import json
import questionary
import pandas as pd
import os

def validate(code):
    """
    Function to validate an Alloy model. This will call the Alloy API (webService).

    :param code: the Alloy code to validate
    :type code: str
    :returns: a JSON file with {success [, errorMessage, errorLocation]}
    :rtype: dict
    """
    payload = {
        "model": code
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{API_URL}/validate", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "errorMessage": str(e)}

# 0. chiedo all'utente l'endpoint delle api di Alloy4Fun
DEFAULT_API_URL = "http://localhost:8080"
API_URL = questionary.text(f"Please provide the URL of the Alloy4Fun API (default is {DEFAULT_API_URL}):").ask() or DEFAULT_API_URL

# 1. chiedo all'utente dove è il mapping file
mapping_file_path = questionary.path("Please provide the (relative) path of the student_mapping.csv file created by the other script:").ask()

# 2. chiedo all'utente se vuole salvare i risultati del check
keep_check = questionary.confirm("Would you like to save the results of the validation of all the .als files you provided into a file?").ask()

# 3. se l'utente vuole salvare i risultati del check, chiedo dove
if keep_check:
    check_path = questionary.path("Please provide the (relative) path where you want to save the validation results:").ask()
    os.makedirs(check_path, exist_ok=True)
    with open(f"{check_path}/syntax_check_results.txt", "a") as f:
        f.write(f"ID\tPerson Code\tTeacher\t.als File\tCheck\n")

# 4. leggo il .csv e itero tutte le righe per fare il check
df = pd.read_csv(mapping_file_path)
for i, r in df.iterrows():
    student_id = r.iloc[0]
    student_personcode = r.iloc[1]
    teacher = r.iloc[2]
    als_file = r.iloc[3]

    print(f"Checking Student {student_id}...", end="\r")

    # 3.2 apro il file .als e leggo tutto il codice
    with open(als_file, "r") as f:
        code = f.read()
        result = validate(code)
        if result["success"]:
            print(f"\033[92m[✓] Student {student_id} .als model validated successfully.\033[0m")
        else:
            print(f"\033[91m[X] Student {student_id} .als model validation failed: {result['errorMessage']}\033[0m")

        if keep_check:
            with open(f"{check_path}/syntax_check_results.txt", "a") as f:
                f.write(f"{student_id}\t{student_personcode}\t{teacher}\t{als_file}\t{"OK" if result["success"] else "KO"}\n")

print("All students checked successfully.\n")

# 5. chiedo all'utente se vuole aprire la cartella con i risultati
open_folder = questionary.confirm("Would you like to open the folder with the validation results?").ask()
if open_folder:
    os.system(f"open {check_path}")