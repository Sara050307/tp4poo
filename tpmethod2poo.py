class Patient:
    def __init__(self, nom, poids, taille):
        self.nom = nom
        self.poids = float(poids)
        self.taille = float(taille)

    def imc(self):
        return round(self.poids / (self.taille ** 2), 2)

    def est_en_corpulence_normale(self):
        return 18.5 <= self.imc() <= 25

class Cabinet:
    def __init__(self, nom_fichier):
        self.patients = self.importer_patients(nom_fichier)

    def importer_patients(self, nom_fichier):
        patients = []
        try:
            with open(nom_fichier, 'r') as fichier:
                lignes = fichier.readlines()
                for ligne in lignes:
                    nom, poids, taille = ligne.strip().split()
                    patient = Patient(nom, poids, taille)
                    patients.append(patient)
        except FileNotFoundError:
            print(f"Le fichier '{nom_fichier}' est introuvable.")
        return patients

    def imc_moyen(self):
        total_imc = sum(patient.imc() for patient in self.patients)
        return round(total_imc / len(self.patients), 2) if self.patients else 0

    def patients_en_corpulence_normale(self):
        return [patient.nom for patient in self.patients if patient.est_en_corpulence_normale()]

    def produire_chaine_patient(self, patient):
        return f"{patient.nom} {patient.imc()}\n"

    def ecrire_resultats(self, nom_fichier_sortie):
        with open(nom_fichier_sortie, 'w') as fichier:
            for patient in self.patients:
                fichier.write(self.produire_chaine_patient(patient))
            fichier.write(f"IMC Moyen : {self.imc_moyen()}\n")
            fichier.write("Noms des patients en corpulence normale :\n")
            for nom in self.patients_en_corpulence_normale():
                fichier.write(f"{nom}\n")

def traitement_complet_donnees(fichier_entrant, fichier_sortant):
    cabinet = Cabinet(fichier_entrant)
    cabinet.ecrire_resultats(fichier_sortant)

cabinet = Cabinet("donnee_md.txt")
for patient in cabinet.patients:
    print(f"Patient: {patient.nom}, IMC: {patient.imc()}")

print(f"IMC Moyen: {cabinet.imc_moyen()}")


print(f"Patients en corpulence normale: {cabinet.patients_en_corpulence_normale()}")

cabinet.ecrire_resultats("resultatsdonnees.txt")
traitement_complet_donnees("donnee_md.txt", "resultatsdonnees.txt")
