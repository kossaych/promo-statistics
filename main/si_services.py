import csv
from collections import defaultdict
import pandas as pd
from functools import reduce
import pickle
import os


def get_exam_name(label) :
    if label[0] == 'm' :
        return 'm'
    else : return label
# Remplace par le chemin de ton fichier Excel
fichier_excel = "moysi.xlsx"
fichier_excel = os.path.join(os.path.dirname(__file__), fichier_excel)

NON_SUBJECT_COLUMNS = ["MGP","RESULTA",'N°','Ident.','Nom','Prenom']
IN_ALL_TABLES_COLUMNS = ['N°','Ident.','Nom','Prenom']


def get_students():
    """
    Returns a list of dictionaries containing student information.
    Each dictionary contains the student's number, name, first name, ID, and average grades.
    """ 
    subjects = []
    feuilles = pd.read_excel(fichier_excel,sheet_name=None) 
    tableaux = []
    for nom, df in feuilles.items() :
            if 'Ident.' in df.columns:
                multi_header = []
                header = df.columns
                sub_header =  [item for item in df.iloc[0:1].values[0] if isinstance(item,str)]
                for item in header : 
                    if item not in NON_SUBJECT_COLUMNS and item[:4] != "Unna" :
                        subjects.append(item)
                        for sub_item in sub_header : 
                            exam = get_exam_name(sub_item)
                            multi_header.append((item,exam))
                            sub_header = sub_header[1:]
                            if sub_item[0] == "m" :
                                break
                    elif item[:4] != "Unna" : 
                        multi_header.append((item,''))
                
                df.columns = pd.MultiIndex.from_tuples(multi_header) 
                df = df.iloc[1:].reset_index(drop=True)
                
                tableaux.append(df)
                
    tab1 = fusion1 = pd.concat(tableaux[:3], ignore_index=True)
    tab2 = fusion1 = pd.concat(tableaux[3:6], ignore_index=True)
    tab3 = fusion1 = pd.concat(tableaux[6:9], ignore_index=True)
    tab4 = fusion1 = pd.concat(tableaux[9:12], ignore_index=True)
    dfs = [tab1, tab2, tab3, tab4]
    tab = reduce(lambda left, right: pd.merge(left, right, on=IN_ALL_TABLES_COLUMNS, how='inner'), dfs)
    ##########################################################################################################
    # 2. File path for storing coefficients
    file_path = "coefficients_si.pkl"
    file_path = os.path.join(os.path.dirname(__file__), file_path)

    # 3. Load existing data or create a new dict
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            coef_dict = pickle.load(f)
    else:
        coef_dict = {}

    #########################################################################################################
    etudiants = [] 
    for index, etudiant in tab.iterrows():
        e = dict() 
        e['num'] = int(etudiant['N°']['']) 
        e['nom'] = etudiant['Nom']['']
        e['prenom'] = etudiant['Prenom']['']
        e['id'] = int(etudiant['Ident.']['']) 
        
        if str(etudiant['Ident.']): 
            somme_coef1 = 0
            somme1 = 0 
            somme_coef2 = 0
            somme2 = 0
            for subject,info in coef_dict.items() :
                coef = info['coef']
                sem = info['sem'] 
                try :
                    moyenne = float(etudiant[subject]['m'])
                except :
                    coef = 0 
                if sem == 1 :
                    somme1 = somme1 + (moyenne*coef)
                    somme_coef1 += coef
                else : 
                    somme2 = somme2 + moyenne*coef
                    somme_coef2 += coef
                e[subject] = moyenne 
            
            moy_gen1 = round(somme1 / somme_coef1,2)
            moy_gen2 = round(somme2 / somme_coef2,2)
            moy_gen = round((moy_gen1 + moy_gen2)/2,2)
            e["moy_gen1"] = moy_gen1
            e["moy_gen2"] = moy_gen2
            e["moy_gen"] = moy_gen
            etudiants.append(e) 
    etudiants = sorted(etudiants, key=lambda d: d['moy_gen'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang'] = i
        i += 1

    for etudiant in etudiants :
        if etudiant['moy_gen'] >= 15 : 
            M = 100
        elif etudiant['moy_gen'] > 10 and etudiant['moy_gen'] < 15 : 
            M = 20*(etudiant['moy_gen'] - 10)
        else :
            M = 0

        ri = (etudiant['rang'] - 1)/91
        if ri > 0.3 : #0.3
            R = 0
        else :
            R  = 100 -(700*ri)/3
        
        B1 = 5
        B2 = 15 
        ML = round((etudiant['Anglais 1'] + etudiant['Tech Com 2'] + etudiant['Tech Com 1'] + etudiant['Anglais 2'])/4,2) #score des langues
        etudiant['ML']  = ML  
        
        etudiant['A'] = round(0.2 * M + 1.4 / 3 * R + 5 / 6 * ML + 2 / 3 * (B1 + B2),2)
        etudiant['E'] = round((etudiant['Analyse 1'] + etudiant['Algèbre 2'] + etudiant['Algèbre 1']  +etudiant['Analyse 2'] )/4 + (etudiant['Algo Struct donnée'] + etudiant['Algo&Struct Donnée 1'])/2 ,2)
        etudiant['S'] = round(0.7*etudiant['A'] + 0.3*etudiant['E'],2)
        
    etudiants = sorted(etudiants, key=lambda d: d['A'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang_A'] = i
        i += 1
    etudiants = sorted(etudiants, key=lambda d: d['E'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang_E'] = i
        i += 1
    etudiants = sorted(etudiants, key=lambda d: d['S'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang_S'] = i
        i += 1
    etudiants = sorted(etudiants, key=lambda d: d['ML'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang_ML'] = i
        i += 1
    
    etudiants = sorted(etudiants, key=lambda d: d['moy_gen1'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang1'] = i
        i += 1

    etudiants = sorted(etudiants, key=lambda d: d['moy_gen2'],reverse = True)
    i = 1
    for etudiant in etudiants :
        etudiant['rang2'] = i
        i += 1
        
 

    return etudiants
def get_subjects():
    # get the subjects from the coefficients file
    file_path = "coefficients_si.pkl"
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            coef_dict = pickle.load(f)
    else:
        coef_dict = {}
    subjects = coef_dict 
    return subjects
 