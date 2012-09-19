# Prime Handler

import unittest
from math import sqrt

__all__ = ['PrimeHandler', 'num_shared_prime_factor']

class PrimeHandler(object):
    """This class compute the number of shared prime factors between two
       numbers. The process of finding it is as follows:
        - first generates list of prime numbers (default 20).
        - check if each prime number in the list is factor of two numbers
        - if prime numbers in the list is not large enough, expand the list
          with larger prime numbers

       Warning: This method of computing the shared prime factors is time
                efficient but may become inefficient in terms of space
                complexity. Suppose one problem instance of two numbers are
                very large numbers and the rest of the instances are small
                numbers. Due to the first instance, the list of prime numbers
                holds large number of prime numbers. However, the rest of
                problem instances do not use all the prime numbers in the list.
    """


    def __init__(self, max_num = 20):
        self.max_prime_num = 0
        self.list_prime_num = []
        self.generate_list_prime_numbers(max_num)

        
    def generate_list_prime_numbers(self, num):
        """genearte list of prime numbers using Sieve of Eratosthenes algorithm"""

        if self.max_prime_num >= num:
            return [x for x in self.list_prime_num if x <= num]

        self.max_prime_num *= 2
        if self.max_prime_num < num:
            self.max_prime_num = num

        list_is_prime = [True] * self.max_prime_num
        
        # Sieve of Eratosthenes
        for i in range( 2, int(sqrt(self.max_prime_num) ) ):
            if list_is_prime[i]:
                for j in range(0, int( self.max_prime_num / i) ):
                    if ( (i * i + j * i) < self.max_prime_num ):
                        list_is_prime[(i * i + j * i)] = False

        if len(self.list_prime_num) == 0:
            range_start = 2
        else:
            range_start = self.list_prime_num[-1] + 1

        for i in range(range_start, self.max_prime_num):
            if list_is_prime[i]:
                self.list_prime_num.append(i)
        return [x for x in self.list_prime_num if x <= num]

        
    def num_shared_prime_factor(self, x, y):
        counter = 0
        min_num = min([x, y])
        self.generate_list_prime_numbers(min_num)

        for prime_num in self.list_prime_num:
            if x % prime_num == 0 and y % prime_num == 0:
                counter += 1
            if min_num < prime_num:
                break
        return counter





# this part is for unit testing of PrimeHandler class
class TestPrimeHandler (unittest.TestCase):
    """Test PrimeHandler class."""

    def setUp(self):
        self.phandler = PrimeHandler()

    def test_01_generate_list_prime_numbers(self):
        """test generate_list_prime_numbers function."""

        result = self.phandler.generate_list_prime_numbers(-1)
        self.failUnless (result == [],
                         'generate_list_prime_numbers(-1) fail. result = %s'
                         % (result) )
        
        result = self.phandler.generate_list_prime_numbers(0)
        self.failUnless (result == [],
                         'generate_list_prime_numbers(0) fail. result = %s'
                         % (result) )
        
        result = self.phandler.generate_list_prime_numbers(5)
        self.failUnless (result == [2,3,5],
                         'generate_list_prime_numbers(5) fail. result = %s'
                         % (result) )

        result = self.phandler.generate_list_prime_numbers(20)
        self.failUnless (result == [2,3,5,7,11,13,17,19],
                         'generate_list_prime_numbers(20) fail. result = %s'
                         % (result) )

        result = self.phandler.generate_list_prime_numbers(30)
        self.failUnless (result == [2,3,5,7,11,13,17,19,23,29],
                         'generate_list_prime_numbers(30) fail. result = %s'
                         % (result) )

        result = self.phandler.generate_list_prime_numbers(40)
        self.failUnless (result == [2,3,5,7,11,13,17,19,23,29,31,37],
                         'generate_list_prime_numbers(30) fail. result = %s'
                         % (result) )
        

    def test_02_num_shared_prime_factor(self):
        """test num_shared_prime_factor function."""

        result = self.phandler.num_shared_prime_factor(2,3)
        self.failUnless (result == 0,
                         'num_shared_prime_factor(2,3) fail. result = %s list = %s'
                         % (result, self.phandler.list_prime_num) )

        result = self.phandler.num_shared_prime_factor(6,3)
        self.failUnless (result == 1,
                         'num_shared_prime_factor(6,3) fail. result = %s list = %s'
                         % (result, self.phandler.list_prime_num) )

        result = self.phandler.num_shared_prime_factor(0,3)
        self.failUnless (result == 0,
                         'num_shared_prime_factor(0,3) fail. result = %s list = %s'
                         % (result, self.phandler.list_prime_num) )

        result = self.phandler.num_shared_prime_factor(5,34444445)
        self.failUnless (result == 1,
                         'num_shared_prime_factor(5,34444445) fail. result = %s list = %s'
                         % (result, self.phandler.list_prime_num) )

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    
            
        

    
