# Wiretaps class

import sys
import getopt
import unittest
from prime_handler import PrimeHandler
from min_weight_bipartite_match import MinWeightBipartiteMatch

vowels = ['a', 'i', 'u', 'e', 'o']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q',
              'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

__all__ = ['Wiretaps','solve_problem','get_total_cost',
           'print_solution']

class Wiretaps(object):
    """Tasks team of programmers to wiretap victims in a way that minimizes
       the total time necessary to crack all the wiretaps. The detail can be
       found at: http://www.facebook.com/jobs_puzzles/index.php?puzzle_id=11"""

    def __init__(self):
        self.phand = PrimeHandler()
        self.cost_table = None
        self.list_vnames = []
        self.solution = None

    def _set_cost_table(self, list_victim_names):
        """set cost table based on list of victim names"""
        
        self.list_vnames = list_victim_names
        num_victim = len(list_victim_names)
        self.cost_table = []
        for vname in list_victim_names:
            len_vname = len(vname)
            num_vow   = Wiretaps._get_num_vowel(vname)
            num_cons  = Wiretaps._get_num_consonant(vname)

            even_weight = 1.5 * num_vow
            odd_weight  = num_cons

            row = []
            flag_even_prog_id = False
            for id_prog in range(1, num_victim + 1):
                if flag_even_prog_id:
                    weight = even_weight
                else:
                    weight = odd_weight
                weight += ( len_vname + 2 *
                    self.phand.num_shared_prime_factor(id_prog, len_vname) )
                flag_even_prog_id = not flag_even_prog_id
                row.append(weight)
            self.cost_table.append(row)

    @staticmethod
    def _get_num_vowel(word):
        """Return the number of vowel in input string. Assume the input string
           contains lower case characters and does not contain any non-alphabet"""
        counter = 0
        for letter in word:
            if vowels.count(letter) > 0:
                counter += 1
        return counter

    @staticmethod
    def _get_num_consonant(word):
        """Return the number of consonant in input string. Assume the input
           string contains lower case characters and does not contain any
           non-alphabet"""
        counter = 0
        for letter in word:
            if consonants.count(letter) > 0:
                counter += 1
        return counter

    
    def solve_problem(self, list_victim_name):
        """solve a wiretaps problem"""

        self._set_cost_table(list_victim_name)
        mwb_match = MinWeightBipartiteMatch(self.cost_table)
        self.solution = mwb_match.find_match()
        return self.solution

    
    def get_total_cost(self):
        """get total cost of the solution"""
        assert self.solution != None, "solve_problem() not called yet."
        
        total_cost = 0
        for i in range( 0, len(self.solution) ):
            total_cost += self.cost_table[i][self.solution[i]]
        return total_cost


    def print_solution(self):
        """print the solution"""
        assert self.solution != None, "solve_problem() not called yet."
        
        print "total cost: %f\n" % self.get_total_cost()
        
        for i in range( 0, len(self.solution) ):
            print "%s => %s(%s)" % (self.list_vnames[i], self.solution[i] + 1, \
                                    self.cost_table[i][self.solution[i]])

    def print_cost_table(self):
        assert self.cost_table != None, "cost table not constructed yet."

        str = ""
        for row in self.cost_table:
            for cost in row:
                str += "%s, " % cost
            str += "\n"
        print(str)
    



# this part is unit test of Wiretaps class
class TestWiretaps (unittest.TestCase):
    """Test Wiretaps class."""

    def setUp(self):
        self.wiretaps = Wiretaps()

    def test_01_get_num_vowel(self):
        """test get_num_vowel function."""
        result = Wiretaps.get_num_vowel("chair")
        self.failUnless (result == 2,
                         'get_num_vowel("chair") fail. result = %s'
                         % (result) )

        result = Wiretaps.get_num_vowel("box")
        self.failUnless (result == 1,
                         'get_num_vowel(" box ") fail. result = %s'
                         % (result) )

    def test_02_get_num_consonant(self):
        """test get_num_consonant function."""
        result = Wiretaps.get_num_consonant("chair")
        self.failUnless (result == 3,
                         'get_num_consonant("chair") fail. result = %s'
                         % (result) )

        result = Wiretaps.get_num_consonant("box")
        self.failUnless (result == 2,
                         'get_num_consonant(" box ") fail. result = %s'
                         % (result) )

    def test_03_set_cost_table(self):
        """test set_cost_table function."""

        self.wiretaps._set_cost_table(['john'])
        self.failUnless (self.wiretaps.cost_table ==
                         [[4 + Wiretaps.get_num_consonant('john') + 0]],
                         "set_cost_table(['john'] fail. result = %s"
                         % (self.wiretaps.cost_table) )


        self.wiretaps._set_cost_table(['john', 'kelly'])
        expected = [[4 + Wiretaps.get_num_consonant('john') + 0,
                     4 + 1.5 * Wiretaps.get_num_vowel('john') +
                     2 * self.wiretaps.phand.num_shared_prime_factor(2,4)],
                    [5 + Wiretaps.get_num_consonant('kelly') + 0,
                     5 + 1.5 * Wiretaps.get_num_vowel('kelly') +
                     2 * self.wiretaps.phand.num_shared_prime_factor(2,5)]
                    ]
        self.failUnless (self.wiretaps.cost_table == expected,
                         "set_cost_table(['john'] fail. result = %s \nexpected = %s"
                         % (self.wiretaps.cost_table, expected) )

    def test_04_solve_problem(self):
        """test solve_problem function."""

        result = self.wiretaps.solve_problem(['john','kelly'])
        self.failUnless (result == [0,1],
                         "solve_problem(['john','kelly'] fail. result = %s"
                         % (result) )
        
    def tearDown(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
    

                                   
