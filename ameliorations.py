# VERSION specifique à MonMaster
from itertools import product
coeffs= [1, 1, 1, 1, 1] #calcul de la Moyenne
seuils = [12, 12, 12] # Calcul du status d'éligibilité (logique, BDD, PS)
thresholds = [12, 14] # prendre la décision
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
    return m,e,d
def AC2_beta_minChanges(N_candidat, X, decision, df=None):
    candidat=df[df.id==N_candidat].copy()
    if (len(candidat)==0):
        return False

    variable_domains = {
          "S1": range(0, 21),
          "S2": range(0, 21),
          "S3": range(0, 21),
          "S4": range(0, 21),
          "S5": range(0, 21),
          "BDD": [0, 1],
          "Logique": [0, 1],
          "PS": [0, 1],
          "Moyenne":[0,1,2],
          "Eligible":[True,False]
      }

    variables_X=list(X.keys())
    valeurs_X=list(X.values())

    def getDecision_MoyElig(m,e):
      if e and m==2:
          d= 'A'
      elif e and m==1:
          d='L'
      else:
          d='R'
      return d

    if(decision == 'A'):
      variable_domains = {
          "S1": range(0, candidat.loc[:,['S1']].iloc[0,0])[::-1],
          "S2": range(0,  candidat.loc[:,['S2']].iloc[0,0])[::-1],
          "S3": range(0,  candidat.loc[:,['S3']].iloc[0,0])[::-1],
          "S4": range(0,  candidat.loc[:,['S4']].iloc[0,0])[::-1],
          "S5": range(0,  candidat.loc[:,['S5']].iloc[0,0])[::-1],
          "BDD": [0, 1],
          "Logique": [0, 1],
          "PS": [0, 1],
          "Moyenne":[0,1,2],
          "Eligible":[True,False]
      }
    elif(decision == 'R'):
      variable_domains = {
          "S1": range(candidat.loc[:,['S1']].iloc[0,0]+1, 21),
          "S2": range(candidat.loc[:,['S2']].iloc[0,0]+1, 21),
          "S3": range(candidat.loc[:,['S3']].iloc[0,0]+1,21),
          "S4": range(candidat.loc[:,['S4']].iloc[0,0]+1,21),
          "S5": range(candidat.loc[:,['S5']].iloc[0,0]+1,21),
          "BDD": [0, 1],
          "Logique": [0, 1],
          "PS": [0, 1],
          "Moyenne":[0,1,2],
          "Eligible":[True,False]
      }
    elif(decision == 'L'):
      variable_domains = {
          "S1": list(range(candidat.loc[:,['S1']].iloc[0,0]+1, 21))+list(range(0, candidat.loc[:,['S1']].iloc[0,0])[::-1]),
          "S2": list(range(candidat.loc[:,['S2']].iloc[0,0]+1, 21))+list(range(0, candidat.loc[:,['S2']].iloc[0,0])[::-1]),
          "S3": list(range(candidat.loc[:,['S3']].iloc[0,0]+1, 21))+list(range(0, candidat.loc[:,['S3']].iloc[0,0])[::-1]),
          "S4": list(range(candidat.loc[:,['S4']].iloc[0,0]+1, 21))+list(range(0, candidat.loc[:,['S4']].iloc[0,0])[::-1]),
          "S5": list(range(candidat.loc[:,['S5']].iloc[0,0]+1, 21))+list(range(0, candidat.loc[:,['S5']].iloc[0,0])[::-1]),
          "BDD": [0, 1],
          "Logique": [0, 1],
          "PS": [0, 1],
          "Moyenne":[0,1,2],
          "Eligible":[True,False]
      }

    def subdict_combinations(dictionary):
        if not dictionary:
            return [{}]

        key = next(iter(dictionary))
        rest = dictionary.copy()
        del rest[key]

        subcombos = subdict_combinations(rest)
        result = []
        for subcombo in subcombos:
            result.append(subcombo)
            with_key = {key: dictionary[key]}
            result.append({**with_key, **subcombo})
        return result

    def generate_combinations(X, variable_domains):
        # Générer toutes les combinaisons possibles de valeurs pour les clés de X_var
        combinations = product(*[variable_domains[var] for var in X])

        # Exclure la combinaison identique à X
        return [combination for combination in combinations if combination != tuple(X.values())]
    sub=subdict_combinations(X)
    for subX in sub:
        if len(subX): #eviter le cas vide
            X_var=list(subX.keys())
            vals=candidat.iloc[0].to_dict()
            combinations = generate_combinations(subX, variable_domains)
            # Vérifier chaque combinaison
            for combination in combinations:
                x_prime = dict(zip(X_var, combination))
                for k in x_prime.keys():
                    vals[k]=x_prime[k]
                m,e,d=med(**{k: v for k, v in vals.items() if k in ['S1', 'S2', 'S3', 'S4', 'S5', 'Logique', 'BDD', 'PS']})
                if (set(['Logique', 'BDD', 'PS']) & x_prime.keys() and 'Eligible' in x_prime and x_prime['Eligible']!=e) or (set(['S1', 'S2', 'S3', 'S4', 'S5']) & x_prime.keys() and 'Moyenne' in x_prime and x_prime['Moyenne']!=m) :
                    continue
                elif (not set(['Logique', 'BDD', 'PS']) & x_prime.keys() and 'Eligible' in x_prime) or (not set(['S1', 'S2', 'S3', 'S4', 'S5']) & x_prime.keys() and 'Moyenne' in x_prime):
                  if not set(['Logique', 'BDD', 'PS']) & x_prime.keys() and 'Eligible' in x_prime:
                    e=x_prime['Eligible']
                  if not set(['S1', 'S2', 'S3', 'S4', 'S5']) & x_prime.keys() and 'Moyenne' in x_prime:
                    m=x_prime['Moyenne']
                  d=getDecision_MoyElig(m,e)
                if d!=decision and len(x_prime)==len(X):
                    print("AC2 et AC3 est vérifié pour une affectation x_prime:",x_prime, " la decision est :", d)
                    return True
                elif d!=decision:
                    print("Erreur : AC2 et AC3 est vérifié pour une affectation x_prime :", x_prime, " la decision est :", d)
                    return False
    print("Erreur : AC2 n'est pas vérifiée, veuillez saisir un superset de l'ensemble des variables sélectionnées")
    return False
#ca ameliore les cas où AC3 n'est pas vérifié tout en ayant une meme complexité dans le cas où AC2 et AC3 sont verifiés
