import copy as cp


class automate:
    """
    classe de manipulation des automates
    l'alphabet est l'ensemble des caractères alphabétiques minuscules et "E" pour epsilon, 
    et "O" pour l'automate vide
    """
    
    def __init__(self, expr="O"):
        """
        construit un automate élémentaire pour une expression régulière expr 
            réduite à un caractère de l'alphabet, ou automate vide si "O"
        identifiant des états = entier de 0 à n-1 pour automate à n états
        état initial = état 0
        """
        
        # alphabet
        self.alphabet = list("abc")
        # l'expression doit contenir un et un seul caractère de l'alphabet
        if expr not in (self.alphabet + ["O", "E"]):
            raise ValueError("l'expression doit contenir un et un seul\
                           caractère de l'alphabet " + str(self.alphabet))
        # nombre d'états
        if expr == "O":
            # langage vide
            self.n = 1
        elif expr == "E":
            self.n = 1
        else:
            self.n = 2
        # états finals: liste d'états (entiers de 0 à n-1)
        if expr == "O":
            self.final = []
        elif expr == "E":
            self.final = [0]
        else:
            self.final = [1]
        # transitions: dico indicé par (état, caractère) qui donne la liste des états d'arrivée
        self.transition =  {} if (expr in ["O", "E"]) else {(0,expr): [1]}
        # nom de l'automate: obtenu par application des règles de construction
        self.name = "" if expr == "O" else "(" + expr + ")" 

    def __str__(self):
        # Affichage lisible de l'automate
        res = "Automate " + self.name + "\n"
        res += "Nombre d'états " + str(self.n) + "\n"
        res += "Etats finals " + str(self.final) + "\n"
        res += "Transitions:\n"

        # On liste toutes les transitions du dictionnaire
        for k, v in self.transition.items():
            res += str(k) + ": " + str(v) + "\n"

        res += "*********************************"
        return res

    def ajoute_transition(self, q0, a, qlist):
        #on veut une liste d'états à ajouter
        if not isinstance(qlist, list):
            raise TypeError(
                "Erreur de type: ajoute_transition requiert une liste à ajouter"
            )

        # Si une transition (q0,a) existe déjà : on concatène les destinations
        if (q0, a) in self.transition:
            self.transition[(q0, a)] = self.transition[(q0, a)] + qlist
        else:
            # Sinon on crée la transition
            self.transition.update({(q0, a): qlist})


def decaler_automate(a, decalage):
    """Copie de a avec tous les états +decalage."""
    # On copie l'automate pour ne pas modifier l'original
    b = cp.deepcopy(a)

    # On décale les états finaux
    b.final = [q + decalage for q in b.final]

    # On reconstruit le dictionnaire des transitions avec états décalés
    b.transition = {
        # clé : (source + decalage, symbole)
        (q + decalage, symb): [
            # destinations : chaque d devient d + decalage
            d + decalage for d in dests
        ]
        # on parcourt chaque transition de l'automate original
        for (q, symb), dests in b.transition.items()
    }

    # On renvoie l'automate décalé
    return b


# construit l'automate correspondant de deux automates a1.a2.
# on relie chaque état final de a1 à l'état initial de a2.
def concatenation(a1, a2):
    # On copie a1 (pour éviter de le modifier par accident)
    a1b = cp.deepcopy(a1)

    # On décale a2 de a1.n pour que ses états commencent après ceux de a1
    a2b = decaler_automate(a2, a1.n)

    # Automate résultat (initialisé vide)
    a = automate("O")

    # Même alphabet
    a.alphabet = a1.alphabet

    # Nombre d'états total = n(a1) + n(a2)
    a.n = a1.n + a2.n

    # On fusionne les transitions de a1 et de a2 décalé
    a.transition = {}
    a.transition.update(a1b.transition)
    a.transition.update(a2b.transition)

    # Dans a2 décalé, l'état initial vaut exactement a1.n
    init_a2 = a1.n

    # Pour concaténer : depuis chaque final de a1, on va vers init_a2 avec epsilon
    for f in a1b.final:
        a.ajoute_transition(f, "E", [init_a2])

    # Les états finaux du résultat sont ceux de a2 (décalés)
    a.final = a2b.final

    # Nom lisible
    a.name = f"({a1.name}.{a2.name})"

    return a


# construit l'automate correspondant de l'union a1+a2.
def union(a1, a2):
    # On crée un nouvel état initial 0
    # on décale a1 de +1 (son initial devient 1)
    a1b = decaler_automate(a1, 1)

    # a2 doit commencer après a1 (décalé)
    # on décale a2 de (1 + a1.n)
    a2b = decaler_automate(a2, 1 + a1.n)

    # Automate résultat (vide au départ)
    a = automate("O")

    # Même alphabet
    a.alphabet = a1.alphabet

    # Nombre d'états = 1 (nouvel initial) + n(a1) + n(a2)
    a.n = 1 + a1.n + a2.n

    # On copie toutes les transitions des deux automates décalés
    a.transition = {}
    a.transition.update(a1b.transition)
    a.transition.update(a2b.transition)

    # Depuis le nouvel initial 0, epsilon vers les deux initiaux :
    # - initial de a1b = 1
    # - initial de a2b = 1 + a1.n
    a.ajoute_transition(0, "E", [1, 1 + a1.n])

    # États finaux = finaux de a1b + finaux de a2b
    a.final = a1b.final + a2b.final

    # Nom lisible
    a.name = f"({a1.name}+{a2.name})"

    return a


# construit l'automate correspondant de l'expression a1*
def etoile(a1):
    # On crée un nouvel état initial 0
    # on décale l'automate a1 de +1
    a1b = decaler_automate(a1, 1)

    # Automate résultat
    a = automate("O")

    # Même alphabet
    a.alphabet = a1.alphabet

    # Nombre d'états = 1 (nouvel initial) + n(a1)
    a.n = a1.n + 1

    # On copie les transitions de a1 décalé
    a.transition = {}
    a.transition.update(a1b.transition)

    # L'étoile accepte epsilon :
    # donc 0 est un état final
    # on garde aussi les anciens finals
    a.final = [0] + a1b.final

    # Pour faire au moins une itération : epsilon de 0 vers l'initial de a1b (=1)
    a.ajoute_transition(0, "E", [1])

    # Pour répéter : depuis chaque final de a1b, epsilon vers :
    # - 1 (pour recommencer)
    # - 0 (pour s'arrêter et accepter)
    for f in a1b.final:
        a.ajoute_transition(f, "E", [1, 0])

    a.name = f"({a1.name})*"
    return a


def acces_epsilon(a):
    """
    Calcule la fermeture epsilon de chaque état :
    res[i] = liste des états atteignables depuis i en suivant seulement des 'E'.
    """
    # res[i] contient au départ i lui-même
    res = [[i] for i in range(a.n)]

    # Pour chaque état de départ i
    for i in range(a.n):
        # candidats = états pas encore ajoutés dans la fermeture epsilon de i
        candidats = list(range(i)) + list(range(i + 1, a.n))

        # new = "frontière" : états ajoutés récemment
        new = [i]

        while True:
            # On collecte tous les voisins atteignables par epsilon depuis new
            voisins_epsilon = []
            for e in new:
                # Si e a une transition epsilon
                if (e, "E") in a.transition.keys():
                    # alors on ajoute toutes ses destinations epsilon
                    voisins_epsilon += [j for j in a.transition[(e, "E")]]

            # Nouveaux états = ceux qui sont encore candidats
            new = [e for e in voisins_epsilon if e in candidats]

            # Si rien de nouveau, fermeture stable donc stop
            if not new:
                break

            # On retire les nouveaux de la liste des candidats
            candidats = list(set(candidats) - set(new))

            # Et on les ajoute à la fermeture epsilon
            res[i] += new

    return res


def supression_epsilon_transitions(a):
    # le but est de construire un automate équivalent sans transitions epsilon

    # On travaille sur une copie
    a = cp.deepcopy(a)

    # Automate résultat (sans epsilon)
    res = automate("O")
    res.name = a.name
    res.n = a.n
    res.alphabet = a.alphabet

    # 1) Fermetures epsilon
    acces = acces_epsilon(a)

    # 2) Nouveaux états finaux :
    # i est final si sa fermeture epsilon contient au moins un ancien final
    res.final = []
    finals = set(a.final)
    for i in range(a.n):
        if set(acces[i]) & finals:
            res.final.append(i)

    # 3) Nouvelles transitions (sans 'E') :
    # On veut une transition sans ε : i --x--> dest
    # 1) on liste tous les états p accessibles depuis i en ne prenant que des ε (acces[i])
    # 2) depuis chacun de ces p, on suit les transitions étiquetées x : p --x--> q
    # 3) une fois arrivé en q, on ajoute tous les états atteignables depuis q par ε (acces[q])
    res.transition = {}
    for i in range(a.n):
        for x in a.alphabet:
            dest = set()

            for p in acces[i]:
                if (p, x) in a.transition:
                    for q in a.transition[(p, x)]:
                        dest.update(acces[q])

            if dest:
                res.transition[(i, x)] = sorted(dest)

    return res


def determinisation(a):
    # le but est de transformer un NFA (sans epsilon) en DFA (construction des sous-ensembles)

    # Copie pour éviter effets de bord
    a_entree = cp.deepcopy(a)

    # Automate déterministe résultat
    dfa = automate("O")
    dfa.alphabet = a_entree.alphabet
    dfa.transition = {}
    dfa.name = a_entree.name

    # ensembles = liste des ensembles d'états NFA (chaque ensemble = 1 état DFA)
    ensembles = [frozenset([0])]

    # file de traitement (BFS)
    a_traiter = [frozenset([0])]

    while a_traiter:
        # Ensemble courant S
        S = a_traiter.pop(0)

        # Identifiant de S dans le DFA
        id_S = ensembles.index(S)

        # Pour chaque symbole de l'alphabet
        for c in a_entree.alphabet:
            arrivee = set()

            # On unionne toutes les destinations depuis les états de S
            for q in S:
                if (q, c) in a_entree.transition:
                    arrivee.update(a_entree.transition[(q, c)])

            # Si aucune destination : pas de transition (complétion gérera plus tard)
            if not arrivee:
                continue

            # Ensemble destination T
            T = frozenset(arrivee)

            # Si T est nouveau, on le mémorise et on le met dans la file
            if T not in ensembles:
                ensembles.append(T)
                a_traiter.append(T)

            # Transition DFA : id_S --c--> id_T
            id_T = ensembles.index(T)
            dfa.transition[(id_S, c)] = [id_T]

    # Nombre d'états du DFA
    dfa.n = len(ensembles)

    # États finaux : ensemble qui contient au moins un final du NFA
    dfa.final = []
    finals = set(a_entree.final)
    for i, S in enumerate(ensembles):
        if set(S) & finals:
            dfa.final.append(i)

    return dfa


def completion(a):
    # le but est de rendre un DFA complet en ajoutant un état poubelle si nécessaire

    a = cp.deepcopy(a)

    # On crée l'état poubelle seulement si on détecte une transition manquante
    etat_poubelle = None

    for q in range(a.n):
        for c in a.alphabet:
            if (q, c) not in a.transition:
                # Création du poubelle au premier manque
                if etat_poubelle is None:
                    etat_poubelle = a.n
                    a.n += 1

                # Transition manquante vers poubelle
                a.transition[(q, c)] = [etat_poubelle]

    # Si poubelle créé, il boucle sur lui-même pour tous les symboles
    if etat_poubelle is not None:
        for c in a.alphabet:
            a.transition[(etat_poubelle, c)] = [etat_poubelle]

    return a


def minimisation(a):
    """ retourne l'automate minimum
        a doit être déterministe complet
        algo par raffinement de partition (algo de Moore)
    """
    # On copie pour éviter de modifier l'original
    a = cp.deepcopy(a)

    # Automate résultat
    res = automate()
    res.name = a.name

    # Partition initiale : finals / non-finals
    part = [set(a.final), set(range(a.n)) - set(a.final)]
    part = [e for e in part if e != set()]  # on enlève les classes vides

    # On raffine tant que ça change
    modif = True
    while modif:
        modif = False
        new_part = []

        # On raffine chaque bloc e
        for e in part:
            classes = {}

            for q in e:
                # signature = classes d'arrivée pour chaque symbole
                signature = []
                for c in a.alphabet:
                    dest = a.transition[(q, c)][0]

                    # on cherche l'indice du bloc qui contient dest
                    for i, bloc in enumerate(part):
                        if dest in bloc:
                            signature.append(i)
                            break

                # On regroupe par signature
                classes.setdefault(tuple(signature), set()).add(q)

            # Si on a découpé en plusieurs blocs il y a modification
            if len(classes) > 1:
                modif = True
                new_part.extend(classes.values())
            else:
                new_part.append(e)

        part = new_part

    # mapping : état ancien -> id de sa classe
    mapping = {}
    for i, bloc in enumerate(part):
        for q in bloc:
            mapping[q] = i

    # Construction du DFA minimal
    res.n = len(part)
    res.alphabet = a.alphabet
    res.transition = {}

    # Finals : classes contenant au moins un final
    res.final = []
    for i, bloc in enumerate(part):
        if bloc & set(a.final):
            res.final.append(i)

    # Transitions : on prend un représentant par classe
    for i, bloc in enumerate(part):
        rep = next(iter(bloc))
        for c in a.alphabet:
            dest = a.transition[(rep, c)][0]
            res.transition[(i, c)] = [mapping[dest]]

    return res


def tout_faire(a):
    # Pipeline complet :
    # ε-suppression -> déterminisation -> complétion -> minimisation

    a = supression_epsilon_transitions(a)
    a = determinisation(a)
    a = completion(a)
    a = minimisation(a)

    return a


def egal(a1, a2):
    # le but est de tester l'égalité des langages reconnus par a1 et a2
    # On compare les DFA minimaux (unicité à isomorphisme près)

    a1 = tout_faire(a1)
    a2 = tout_faire(a2)

    # Si alphabets ou tailles différentes => pas isomorphes
    if a1.alphabet != a2.alphabet or a1.n != a2.n:
        return False

    # mapping a1->a2, on commence par l'initial
    m = {0: 0}
    file = [0]

    while file:
        q1 = file.pop(0)
        q2 = m[q1]

        # Statut final doit correspondre
        if (q1 in a1.final) != (q2 in a2.final):
            return False

        # Toutes les transitions doivent être compatibles avec le mapping
        for c in a1.alphabet:
            r1 = a1.transition[(q1, c)][0]
            r2 = a2.transition[(q2, c)][0]

            if r1 in m:
                if m[r1] != r2:
                    return False
            else:
                m[r1] = r2
                file.append(r1)

    return True

# TESTS

if __name__ == "__main__":

    def assert_dfa(d):
        for (q, c), dests in d.transition.items():
            assert c != "E"
            assert len(dests) == 1

    def assert_complet(d):
        for q in range(d.n):
            for c in d.alphabet:
                assert (q, c) in d.transition
                assert len(d.transition[(q, c)]) == 1

    print("TEST 1 : decaler_automate")
    a = automate("a")
    b = decaler_automate(a, 3)
    assert a.transition == {(0, "a"): [1]}
    assert b.transition == {(3, "a"): [4]}
    print("OK")

    print("TEST 2 : union (structure)")
    A = automate("a")
    B = automate("b")
    U = union(A, B)
    assert (0, "E") in U.transition
    assert set(U.transition[(0, "E")]) == {1, 1 + A.n}
    assert len(U.final) == 2
    print("OK")

    print("TEST 3 : concatenation (epsilon de raccord)")
    C = concatenation(automate("a"), automate("b"))
    assert (1, "E") in C.transition
    assert 2 in C.transition[(1, "E")]
    print("OK")

    print("TEST 4 : etoile (accepte epsilon)")
    S = etoile(automate("c"))
    assert 0 in S.final
    assert (0, "E") in S.transition
    print("OK")

    print("TEST 5 : suppression epsilon => plus de 'E'")
    X = concatenation(union(automate("a"), automate("b")), automate("c"))
    Y = supression_epsilon_transitions(X)
    for (q, c) in Y.transition.keys():
        assert c != "E"
    print("OK")

    print("TEST 6 : determinisation => DFA")
    nfa = automate("O")
    nfa.alphabet = list("abc")
    nfa.n = 3
    nfa.final = [2]
    nfa.transition = {}
    nfa.ajoute_transition(0, "a", [1, 2])
    nfa.ajoute_transition(1, "b", [2])
    dfa = determinisation(nfa)
    assert_dfa(dfa)
    print("OK")

    print("TEST 7 : completion => complet")
    dfa_c = completion(dfa)
    assert_dfa(dfa_c)
    assert_complet(dfa_c)
    print("OK")

    print("TEST 8 : egal (1 vrai, 1 faux)")

    # VRAI : automate vide vs automate vide
    left = automate("O")
    right = automate("O")
    assert egal(left, right) is True

    # FAUX : vide vs epsilon
    left2 = automate("O")
    right2 = automate("E")
    assert egal(left2, right2) is False

    print("OK")
