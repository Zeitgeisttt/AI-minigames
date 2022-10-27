from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        ass_fun = {}
        ass_fun[(10, 10)] = False # Conflict spot
        D_81 = domains
        delta_stack = []
        while True:
            # print("done while")
            self.propagate(ass_fun, D_81)
            # print(ass_fun)
            # print("done propagate")
            if ass_fun[(10, 10)] == False:
                allAssigned = True
                for domain in sd_spots:
                    if domain not in ass_fun.keys():
                        allAssigned = False
                if allAssigned:
                    solution = {}
                    for spot in ass_fun.keys():
                        if spot != (10, 10):
                            solution[spot] = [ass_fun[spot]]
                    return solution
                else:
                    ass_fun, x = self.makeDecision(ass_fun, D_81)
                    delta_stack.append((copy.deepcopy(ass_fun), copy.deepcopy(x), copy.deepcopy(D_81)))
            else:
                if len(delta_stack) == 0:
                    print("No solution!")
                    return
                else:
                    ass_fun, D_81 = self.backtrack(delta_stack)

        # # TODO: delete this block ->
        # # Note that the display and test functions in the main file take domains as inputs. 
        # #   So when returning the final solution, make sure to take your assignment function 
        # #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # # <- TODO: delete this block

    # TODO: add any supporting function you need

    def propagate(self, ass_fun, D_81):
        while True:
            for domain1 in D_81.keys():
                if len(D_81[domain1]) == 1 and domain1 not in ass_fun.keys():
                    ass_fun[domain1] = D_81[domain1][0]
            # print("done domain1")
            for domain2 in ass_fun.keys():
                if domain2 != (10, 10):
                    if len(D_81[domain2]) > 1:
                        D_81[domain2] = [ass_fun[domain2]]
            # print("done domain2")
            for domain3 in D_81.keys():
                if len(D_81[domain3]) == 0:
                    ass_fun[(10, 10)] = True
                    return
            # print("done domain3")
            flag = False
            for domain4i in D_81.keys():
                toRemove = []
                for ai in D_81[domain4i]:
                    consistent = True
                    for domain4j in sd_peers[domain4i]:
                        if domain4j in ass_fun.keys():
                            # print("done 1 if")
                            if ass_fun[domain4j] == ai:
                                # print("done 2 if")
                                consistent = False
                    if consistent == False:
                        toRemove.append(ai)
                for a in toRemove:
                    D_81[domain4i].remove(a)
                    flag = True
                    # print("done remove")
            # print("done domain4")
            if flag == False:
                return
            
    def makeDecision(self, ass_fun, D_81):
        unassignedSet = set(sd_spots) - set(ass_fun.keys())
        maxNum = 10
        minX = list(unassignedSet)[0]
        for x in unassignedSet:
            if len(D_81[x]) > 1 and len(D_81[x]) < maxNum:
                maxNum = len(D_81[x])
                minX = x
        a = D_81[minX][0]
        ass_fun[minX] = a
        return ass_fun, minX

    def backtrack(self, delta_stack):
        ass_fun, x, D_81 = delta_stack.pop()
        a = ass_fun[x]
        del ass_fun[x]
        D_81[x].remove(a)
        return ass_fun, D_81


    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
