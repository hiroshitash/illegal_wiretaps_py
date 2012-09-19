# HeapNode class

import unittest

__all__ = ['HeapNode']

class HeapNode(object):
    """HeapNode represents a heap entry for a graph node, which can be pushed
       into a heap. HeapNode has id, priority and prev_node. id is node id in
       a graph, priority is 
    """

    dict_created_nodes = {}
    
    def __init__(self, arg_id, arg_priority, arg_prev_node = None, arg_flag_regist = True):
        self.id = arg_id
        self.priority = arg_priority
        self.prev_node = arg_prev_node
        if arg_flag_regist:
            HeapNode.dict_created_nodes[self.id] = self

    def __eq__(self, other):
        if not isinstance(other, HeapNode):
            return False
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        if self.priority == other.priority:
            return 0
        elif self.priority > other.priority:
            return 1
        else:
            return -1

    def __str__(self):
        return "id: %s pri: %s prev_node: (%s)\n" \
               % (self.id, self.priority, self.prev_node)

    @staticmethod
    def get_entry(id_node):
        if HeapNode.dict_created_nodes.has_key(id_node):
            return HeapNode.dict_created_nodes[id_node]
        return None

    __repr__ = __str__

        
# this part is for unit testing of Prime_Handler class
class TestHeapNode (unittest.TestCase):
    """Test HeapNode class."""

    def setUp(self):
        self.node1_2 = HeapNode(1, 2)
        self.alt_node1_2 = HeapNode(1, 2)
        self.node2_4 = HeapNode(2, 4)
        self.node3_6 = HeapNode(3, 6)
        self.node4_10 = HeapNode(4, 10)
        self.node5_15 = HeapNode(5, 15, None, False)
        
    def runTest(self):
        """test __eq__, __ne__, __cmp__ of HeapNode"""

        result = (self.node1_2 == self.alt_node1_2)
        self.failUnless (result == True,
                         '%s == %s fail. result = %s' \
                         % (self.node1_2, self.alt_node1_2, result) )

        result = (self.node1_2 != self.alt_node1_2)
        self.failUnless (result == False,
                         '%s != %s fail. result = %s' \
                         % (self.node1_2, self.alt_node1_2, result) )

        result = (self.node1_2 < self.alt_node1_2)
        self.failUnless (result == False,
                         '%s < %s fail. result = %s' \
                         % (self.node1_2, self.alt_node1_2, result) )

        result = (self.node1_2 <= self.alt_node1_2)
        self.failUnless (result == True,
                         '%s <= %s fail. result = %s' \
                         % (self.node1_2, self.alt_node1_2, result) )

        result = HeapNode.get_entry(2)
        self.failUnless (result.id == 2 and result.priority == 4 and \
                         result.prev_node == None,
                         'get_entry(2) fail. result = %s' % (result) )

        result = HeapNode.get_entry(5)
        self.failUnless (result == None,
                         'get_entry(5) fail. result = %s' % (result) )

        

    def tearDown(self):
        pass
    
if __name__ == '__main__':
    unittest.main()
    

                                   
