import copy

coeffs= [1, 1, 1, 1, 1] #calcul de la Moyenne
seuils = [12, 12, 12] # Calcul du status d'éligibilité (logique, BDD, PS)
thresholds = [12, 14] # prendre la décision

def Vars(df):
    #retourne les noms des variables d'un DataFrame
    return list(df.columns)[1:-1]

def med(S1, S2, S3, S4, S5, Logique, BDD, PS, coeffs=coeffs, seuils=seuils, thresholds2=thresholds):
    #la fonction qui calcule M E D pour un candidat (valeurs discrétisées)
    moyenne = (S1 * coeffs[0] + S2 * coeffs[1] + S3 * coeffs[2] + S4 * coeffs[3] + S5 * coeffs[4]) / sum(coeffs)
    e = (Logique*BDD*PS==1)
    m = (moyenne>thresholds2[1])*2 + (thresholds2[0] <= moyenne <= thresholds2[1])
    if e and m==2:
        d= 'A'
    elif e and m==1:
        d='L'
    else:
        d='R'
    return d

def generate_supersets(N, X, V, df):
    # generate les combinations possibles de variables dans V, 
    # de leur valeur dans df pour un identifiant N, à partir de la cardinalité de X
	candidat = df[df['N_candidat']==N]
	supersets = [X]
	for var in V:
		valeur = candidat[var].iloc[0]
		copie = copy.deepcopy(supersets)
		for dictio in copie:
			dictio[var]= valeur
		supersets =supersets + copie
	sort =sorted(supersets, key=lambda x:len(x))
	return [dictio for dictio in sort if len(dictio)>=len(X)]