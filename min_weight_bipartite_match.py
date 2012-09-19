# MinWeightBipartiteMatch class

# TODO: implement and use fibonacci heap instead of min heap. 
import unittest
import sys
from heapq import heappush, heappop, heapify
from heap_node import HeapNode

__all__ = ['MinWeightBipartiteMatch', 'find_match']

class MinWeightBipartiteMatch(object):
    """This is an implementation of Minimum Weight Bipartite Matching
       using augument path and dijkstra's shortest path.
       The details of how the algorithm works are explained in the following
       link:

       http://valis.cs.uiuc.edu/~sariel/teach/courses/473/notes/27_matchings_notes.pdf

       Python version uses built-in (min) heap. For improvement, fibonacci heap
       can be use.
    """

    def __init__(self, arg_weight_table):
        assert len(arg_weight_table) == len(arg_weight_table[0]), \
               "weight table is not square"

        self.table_weight = arg_weight_table
        self.map_match_left_to_right = [None] * len(self.table_weight)
        self.map_match_right_to_left = [None] * len(self.table_weight)
        self.list_all_node_ids_right_category = \
            range( len(self.table_weight), 2 * len(self.table_weight) )
        self.solution = None

    def find_match(self):
        """find minimum match given weight table"""

        while True:
            aug_path = self._find_min_augument_path()
            
            if len(aug_path) == 0:
                break
            
            # This part compute new match as follows:
            #  new_match = match (exclusive or) path
            #            = (match \ path) or (path \ match)
            #    where path is a augumenting path of the corresponding match. 
            # After the update, the following condition satisfies: 
            #  |new_match| = |match| + 1.

            flag_left_category_node = True
            id_prev_node = None
            while len(aug_path) != 0:
                id_node = aug_path.pop()

                assert ( flag_left_category_node and \
                         self._is_node_left_category(id_node) ) or \
                       ( not flag_left_category_node and \
                         not self._is_node_left_category(id_node) ), \
                         "augument path corrupted"

                if id_prev_node != None:
                    if flag_left_category_node:
                        assert self.map_match_left_to_right[id_node] == \
                               id_prev_node, \
                               "data inconsistance in map_match_left_to_right"
                         
                        # the matched edge in augumenting path should be removed
                        self.map_match_left_to_right[id_node] = None  
            
                    else: # right category node, meaning the edge goes to
                          # new match
                        self.map_match_left_to_right[id_prev_node] = id_node
                id_prev_node = id_node
                flag_left_category_node  =  not flag_left_category_node

      
            # update map_match_right_left according to new
            # map_match_left_to_right
            self.map_match_right_to_left = [None] * len(self.map_match_right_to_left)
            for i in range( 0, len(self.map_match_right_to_left) ):
                if (self.map_match_left_to_right[i] != None):
                  self.map_match_right_to_left[
                      self._local_node_id(self.map_match_left_to_right[i])] = i

        # end of while len( aug_path = self.find_min_augment_path() ) != 0:

        self.solution = [ self._local_node_id(x) for x in
                                 self.map_match_left_to_right ]
        return self.solution


    def _find_min_augument_path(self):
        """return augument path with minimum weight given match. dijkistra's
           shortest path is used to find the path.
        """
        
        path, heap = [], []
        self._setup_heap(heap)

        while heap:
            node_entry = heappop(heap)
            
            if self._is_node_exposed_right_category(node_entry.id):
                tmp_node_entry = node_entry
                while True:
                    path.append(tmp_node_entry.id)
                    tmp_node_entry = tmp_node_entry.prev_node
                    if (tmp_node_entry == None):
                        break
                return path

            list_neighbor_node_id = \
                self._get_neighbors_aug_path(node_entry.id, heap)

            local_id_entry_node = self._local_node_id(node_entry.id)
            for neighbor_node_id in list_neighbor_node_id:
                local_id_neighbor_node = self._local_node_id(neighbor_node_id)

                if self._is_node_left_category(node_entry.id):
                    alt = node_entry.priority + \
                    self.table_weight[local_id_entry_node][local_id_neighbor_node]
                else:
                    alt = node_entry.priority - \
                    self.table_weight[local_id_neighbor_node][local_id_entry_node]

                node_neighbor = HeapNode.get_entry(neighbor_node_id)

                if alt < node_neighbor.priority:
                    node_neighbor.priority = alt
                    node_neighbor.prev_node = node_entry
                    heapify(heap)
        # end of  while heap

        assert len(path) == 0, "path with element(s) not expected."
        return path


    def _setup_heap(self, heap):
        """before _find_min_augument_path start, this function sets up heap
           as the source nodes should be treated as single node. Basically,
           all the nodes but source nodes will be inserted into heap with
           appropriate weights and prev_nodes.
        """
        min_weight_right_nodes = [sys.maxint] * len(self.table_weight)
        prev_of_right_nodes = [None] * len(self.table_weight)

        num_left_exposed_node = 0

        # insert nodes in left category
        for i in range( 0, len(self.map_match_left_to_right) ):
            if self.map_match_left_to_right[i] == None:
                num_left_exposed_node += 1
                left_exposed_node = HeapNode( self._global_node_id(i, True), 0 )

                for j in range( 0, len(self.table_weight) ):
                    if min_weight_right_nodes[j] > self.table_weight[i][j]:
                        min_weight_right_nodes[j] = self.table_weight[i][j]
                        prev_of_right_nodes[j] = left_exposed_node
            else:
                heappush( heap,
                          HeapNode( self._global_node_id(i, True),
                                    sys.maxint ) )
                    
        if num_left_exposed_node == 0:
            heap = []
            return

        for j in range(0, len(self.table_weight) ):
            heappush( heap,
                      HeapNode( self._global_node_id(j, False),
                                min_weight_right_nodes[j],
                                prev_of_right_nodes[j] ) )
    

    def _global_node_id(self, local_id, flag_left_category):
        """return global id of the node given local id and category flag"""
        assert local_id >= 0 and local_id < len(self.table_weight), \
                "unexpected local_id: %d" % local_id
        return ( local_id if flag_left_category else
                    len(self.table_weight) + local_id )


    def _local_node_id(self, global_id):
        """return local id given global id"""
        assert global_id >= 0 and global_id < 2 * len(self.table_weight), \
                "unexpected global_id: %d" % global_id
        return ( global_id if self._is_node_left_category(global_id) else
                    global_id - len(self.table_weight) )


    def _is_node_left_category(self, global_id_node):
        """return true if the node is in left category, false otherwise"""
        assert global_id_node >= 0 and global_id_node < 2 * len(self.table_weight), \
                "unexpected global_id: %d" % global_id_node
        return ( global_id_node < len(self.table_weight) )

    
    def _is_node_exposed_right_category(self, global_id_node):
        """return true if the node is exposed and in right category, false otherwise"""
        assert global_id_node >= 0 and \
                 global_id_node < (len(self.table_weight) * 2), \
               "unexpected global_id: %d" % global_id
        local_id_node = self._local_node_id(global_id_node)
        return (global_id_node >= len(self.table_weight) and
                self.map_match_right_to_left[local_id_node] == None);

  
    def _get_neighbors_aug_path(self, global_id_node, heap):
        """return neighbors in alternate path."""
        
        assert global_id_node >= 0 and \
                 global_id_node < ( len(self.table_weight) * 2 ), \
               "unexpected global_id: %d" % global_id
        
        
        if self._is_node_left_category(global_id_node): # left category
            if self.map_match_left_to_right[global_id_node] == None: # exposed node
                return self.list_all_node_ids_right_category
            else: # node with match
                list = []
                for global_id_right_node in self.list_all_node_ids_right_category:
                    if global_id_right_node != \
                        self.map_match_left_to_right[global_id_node] and \
                       heap.count( HeapNode(global_id_right_node, 0, None, False) ) > 0:
                        list.append(global_id_right_node)
                return list

        else: # right category
            # return the node in left category which can be reached through
            # matched edge
            idx = self._local_node_id(global_id_node)
            assert (self.map_match_right_to_left[idx] != None), \
                    "there is no neighbor for node %d" % global_id_node
            return [self.map_match_right_to_left[idx]]
        


    
# this part is for unit testing of MinWeightBipartiteMatch class
class TestMinWeightBipartiteMatch (unittest.TestCase):
    """Test MinWeightBipartiteMatch class."""

    def setUp(self):
        self.mwbm = MinWeightBipartiteMatch([[3,5.0,6],[5,8,6],[84,2,10]])
        self.mwbm.map_match_left_to_right[0] = self.mwbm._local_node_id(3)
        self.mwbm.map_match_right_to_left[self.mwbm._local_node_id(3)] = 0
        self.heap = []
        self.mwbm._setup_heap(self.heap)

    def test_01_node_id_related_func(self):
        """test node id related functions: _global_node_id, _local_node_id,
           _is_node_left_category functions
        """

        result = self.mwbm._global_node_id(2, False)
        self.failUnless (result == 5,
                         '_global_node_id(2, false) fail. result = %s'
                         % (result) )

        result = self.mwbm._global_node_id(1, True)
        self.failUnless (result == 1,
                         '_global_node_id(1, true) fail. result = %s'
                         % (result) )

        result = self.mwbm._local_node_id(5)
        self.failUnless (result == 2,
                         '_local_node_id(5) fail. result = %s'
                         % (result) )

        result = self.mwbm._local_node_id(2)
        self.failUnless (result == 2,
                         '_local_node_id(2) fail. result = %s'
                         % (result) )


    def test_02_get_neighbors_aug_path(self):
        """test _get_neighbors_aug_path() function."""

        result = self.mwbm._get_neighbors_aug_path(2, self.heap)
        self.failUnless (result == [3,4,5] or result == [2,5,4], # and so on
                         '_get_neighbors_aug_path(2, self.heap) fail. result = %s'
                         % (result) )

        result = self.mwbm._get_neighbors_aug_path(3, self.heap)
        self.failUnless (result == [0], 
                         '_get_neighbors_aug_path(3, self.heap) fail. result = %s'
                         % (result) )


    def test_03_find_min_augument_path(self):
        """test _find_min_augument_path() function."""
        
        result = self.mwbm._find_min_augument_path()
        self.failUnless (result == [4,2],
                         '_find_min_augument_path() fail. result = %s'
                         % (result) )

        self.mwbm.map_match_left_to_right[2] = self.mwbm._local_node_id(4)
        self.mwbm.map_match_right_to_left[self.mwbm._local_node_id(4)] = 2
        result = self.mwbm._find_min_augument_path()
        self.failUnless (result == [5,1],
                         '_find_min_augument_path() fail. result = %s'
                         % (result) )

    def test_04_find_match(self):
        """test find_match() function."""

        self.mwbm.map_match_left_to_right = [None] * len(self.mwbm.table_weight)
        self.mwbm.map_match_right_to_left = [None] * len(self.mwbm.table_weight)
        result = self.mwbm.find_match()
        self.failUnless (result == [0,2,1],
                         'find_match() fail. result = %s'
                         % (result) )
        
        
    def tearDown(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
