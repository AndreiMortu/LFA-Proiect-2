def lambda_closure(states, nfa):
    closures = set(states) 
    while True: 
        new_closures = set()
        for position in closures:
            new_closures |= set(nfa.get(position, {}).get('x', [])) 
        new_closures -= closures 
        if not new_closures: 
            break
        closures |= new_closures 
    return sorted(list(closures))  

def nfa_to_dfa(nfa, start_state, alphabet):
    initial = sorted(lambda_closure([start_state], nfa)) 
    queue = [initial] 
    processed = set()
    dfa = {}

    while queue:
        state = queue.pop(0)  
        if tuple(state) in processed: 
            continue
        processed.add(tuple(state)) 
        dfa[tuple(state)] = {}  
        for letter in alphabet:  
            next_states = set()
            for nfa_state in state:
                next_states |= set(nfa.get(nfa_state, {}).get(letter, [])) 
            lambdaclosure = sorted(lambda_closure(next_states, nfa))
            if tuple(lambdaclosure) not in processed: 
                queue.append(lambdaclosure)
            dfa[tuple(state)][letter] = tuple(lambdaclosure) 

    return dfa

def write_dfa(dfa, filename, final_states):
    with open(filename, 'w') as file:
        initial = next(iter(dfa)) 
        file.write(f"Stare initiala: {initial}\n\n")

        final2 = [state for state in dfa if any(x in state for x in final_states)]  
        file.write(f"Stari finale: {', '.join(str(state) for state in final2)}\n\n")

        for state in dfa: 
            if state != ():
                for letter in dfa[state]: 
                    next_state = dfa[state][letter]
                    file.write(f"{state} --({letter})-> {next_state}\n")
                file.write("\n")

nfa = {}
alphabet = ('a', 'b', 'c')
with open('input.txt') as file:
    start_state = file.readline().strip()  
    final_states = file.readline().strip().split() 
    for line in file:   
        line = line.strip().split(' ')
        first, letter, second = line  
        if letter == 'λ': 
            letter = 'x'
        if first not in nfa:
            nfa[first] = {}
        if letter not in nfa[first]:
            nfa[first][letter] = []
        nfa[first][letter].append(second)

dfa = nfa_to_dfa(nfa, start_state, alphabet)
write_dfa(dfa, 'output.txt', final_states)
