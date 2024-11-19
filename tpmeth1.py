def import_lignes(nom_fichier):
    lignes = []
    try:
        with open(nom_fichier, 'r') as f:
            lignes = f.readlines()
    except FileNotFoundError:
        print(f"Le fichier '{nom_fichier}' est introuvable.")
    return lignes

def cree_patient(ligne_patient, nom_fichier):
    toutes_lignes = import_lignes(nom_fichier)
    for ligne in toutes_lignes:
        if ligne_patient in ligne:
            valeurs = ligne.strip().split()
            if len(valeurs) == 3:
                d = {
                    "nom": valeurs[0],
                    "poids": float(valeurs[1]),
                    "taille": float(valeurs[2]),
                }
                return d

def liste_patients_par_fichier(nom_fichier):
    toutes_lignes = import_lignes(nom_fichier)
    patients = {}
    for ligne in toutes_lignes:
        patient = cree_patient(ligne.strip(), nom_fichier)
        if patient:  # patient valide
            patients[patient["nom"]] = patient
    return patients

def calculer_imc(patient):
    poids = patient["poids"]
    taille = patient["taille"]
    imc_val = poids / (taille ** 2)
    return round(imc_val, 2)

def calculer_imc_moyen(patients):
    imc_moy = 0
    total_imc = 0
    for patient in patients.values():
        total_imc += calculer_imc(patient)
    imc_moy = total_imc / len(patients)
    return round(imc_moy, 2)

def lister_patients_en_corpulence_normale(patients):
    noms = []
    for patient in patients.values():
        imc_val = calculer_imc(patient)
        if 18.5 <= imc_val <= 25:
            noms.append(patient["nom"])
    return noms

def produire_chaine_patient(patient):
    chaine = ""
    nom = patient["nom"]
    imc = calculer_imc(patient)
    chaine += f"{nom}, {imc}\n"
    return chaine

def ecrire_imc_dans_fichier(patients, nom_fichier):
    with open(nom_fichier, 'w') as fichier:
        for patient in patients.values():
            res = produire_chaine_patient(patient)
            fichier.write(res)
        imc_moy = round(calculer_imc_moyen(patients), 2)
        fichier.write(f"\"IMC Moyen :\" {imc_moy} \n")
        fichier.write("\n")
        corpulence = lister_patients_en_corpulence_normale(patients)
        fichier.write("\"Noms des patients en corpulence normale :\"\n")
        for nom in corpulence:
            fichier.write(f"{nom}\n")
    print(f"Données IMC écrites dans {nom_fichier}")

def traiter_donnees_completes(fichier_entrant, fichier_sortant):
    patients = liste_patients_par_fichier(fichier_entrant)
    ecrire_imc_dans_fichier(patients, fichier_sortant)

### Appel des fonctions modifiées
lignes_importees = import_lignes("donnee_md.txt")
print(lignes_importees)
print("\n")

patient_specifique = cree_patient("Robert", "donnee_md.txt")
print(patient_specifique)
print("\n")

patients_total = liste_patients_par_fichier("donnee_md.txt")
print(patients_total)
print("\n")

for nom, patient in patients_total.items():
    resultat_imc = calculer_imc(patient)
    print(f"L'IMC de {nom} est : {resultat_imc}")

somme_imc = calculer_imc_moyen(patients_total)
print(f"Le total IMC de tous les patients est : {somme_imc}")

noms_corpulence_normale = lister_patients_en_corpulence_normale(patients_total)
print(f"Les noms des patients ayant l'IMC compris entre 18,5 et 25 inclus sont : {noms_corpulence_normale}")

chaine_patient = produire_chaine_patient(patient_specifique)
print(chaine_patient)

ecrire_imc_dans_fichier(patients_total, "resultatsdonnees.txt")
traiter_donnees_completes("donnee_md.txt", "resultatsdonnees.txt")
