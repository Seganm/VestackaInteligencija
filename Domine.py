import collections

# Simbolička reprezentacija domina kao tuple (a, b)
SVE_DOMINE = [
    (0,0), (0,1), (0,2), (0,3), (0,4),
    (1,1), (1,2), (1,3), (1,4),
    (2,2), (2,3), (2,4),
    (3,3), (3,4),
    (4,4)
]

# Funkcija koja proverava da li je dostignuto ciljno stanje
# Cilj: svih 15 domina je iskorišćeno i prva cifra prve domine odgovara poslednjoj cifri poslednje
def is_goal(chain):
    if len(chain) == 15:
        return chain[0][0] == chain[-1][1]
    return False

# Operator promene stanja - Dinamički određuje sledeće moguće domine
def nova_stanja(current_chain, remaining_dominoes):
    successors = []
    if not current_chain:
        # Ako je lanac prazan, možemo početi sa bilo kojom dominom
        for d in remaining_dominoes:
            successors.append(([d], [x for x in remaining_dominoes if x != d]))
    else:
        last_val = current_chain[-1][1]
        for d in remaining_dominoes:
            # Provera obe strane domine (može se okretati)
            if d[0] == last_val:
                new_chain = current_chain + [d]
                new_rem = [x for x in remaining_dominoes if x != d]
                successors.append((new_chain, new_rem))
            elif d[1] == last_val:
                flipped = (d[1], d[0])
                new_chain = current_chain + [flipped]
                new_rem = [x for x in remaining_dominoes if x != d]
                successors.append((new_chain, new_rem))
    return successors

# Implementacija DFS algoritma (Traženje po dubini) prema slajdu 4 i 23
def solve_dominoes():
    # Početno stanje: (prazan_lanac, sve_domine)
    # Koristimo (4,4) kao početnu dominu da smanjimo prostor pretrage, 
    # jer kod ciklusa nije bitno odakle počinjemo.
    start_domino = (4,4)
    initial_chain = [start_domino]
    remaining = [d for d in SVE_DOMINE if d != start_domino]
    
    # Stack za DFS: sadrži tuple (trenutni_lanac, preostale_domine)
    stack = [(initial_chain, remaining)]
    visited_states = set()

    while stack:
        current_chain, current_rem = stack.pop()
        
        # Provera cilja
        if is_goal(current_chain):
            return current_chain

        # Generisanje sledbenika
        for next_chain, next_rem in nova_stanja(current_chain, current_rem):
            # Stanje definišemo kao string lanca radi lakšeg praćenja posećenih grana
            state_id = str(next_chain)
            if state_id not in visited_states:
                visited_states.add(state_id)
                stack.append((next_chain, next_rem))
                
    return None

# Pokretanje i ispis rešenja
resenje = solve_dominoes()
if resenje:
    print("Uspešno poređane sve domine u ciklus:")
    for step, domino in enumerate(resenje):
        print(f"Korak {step+1}: Dodata domina {domino}")
    print(f"\nProvera ciklusa: Početak {resenje[0][0]} == Kraj {resenje[-1][1]}")
else:
    print("Nije pronađeno rešenje.")
