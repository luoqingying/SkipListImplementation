import random

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.below = None
        self.above = None
        self.isLeaf = True
        self.curr_height = 0

class SkipList:
    def __init__(self, max_level, prob):
        # can change to built-in MAX number in python
        # here I only tested with non-negative numbers less than 100
        self.MOST_NEGATIVE = -1
        self.MOST_POSITIVE = 100

        self.map = {} # key-value pair
        self.max_level = max_level
        self.prob = prob # prob of pointing down
        self.head = Node(self.MOST_NEGATIVE)
        self.tail = Node(self.MOST_POSITIVE)
        self.head.right = self.tail
        self.tail.left = self.head
        self.curr_level = 0

    def get(self, key):
        if not self.contain(key):
            return None
        return self.map[key]

    def put(self, key, value):
        # put the first node
        if len(self.map) == 0:
            node = Node(key)
            self.head.right = node
            node.left = self.head
            self.tail.left = node
            node.right = self.tail
            self.curr_level += 1
            self.map[key] = value
            return

        if not self.contain(key):
            # insert in skiplist
            level = self.getRandomLevel()
            
            # create a list of new nodes for length level, while the bottom one is leaf
            new_nodes = [None] * level
            prev = None
            for i in range(level):
                node = Node(key)
                new_nodes[i] = node
                if i != level - 1:
                    node.isLeaf = False
                if prev == None:
                    prev = node
                    continue
                node.above = prev
                prev.below = node
                prev = node
                
            update_list = []
            if self.curr_level <= level:
                # create new level
                num_of_new_level = level - self.curr_level
                for i in range(num_of_new_level):
                    new_head = Node(self.MOST_NEGATIVE)
                    new_tail = Node(self.MOST_POSITIVE)
                    new_head.right = new_tail
                    new_tail.left = new_head

                    self.head.above = new_head
                    new_head.below = self.head
                    self.head = new_head
                    self.tail.above = new_tail
                    new_tail.below = self.tail
                    self.tail = new_tail

                    self.curr_level += 1

            level_node = self.head
            
            if self.curr_level > level:
                # need to find the level node to start
                count = self.curr_level - level
                while count > 0:
                    level_node = level_node.below
                    count -= 1
            
            while level_node != None and level_node.key < key:
                row_node = level_node
                while row_node != None and row_node.key < key:
                    row_node = row_node.right
                update_list.append(row_node.left)
                level_node = update_list[-1].below

            for i in range(len(update_list)):
                node = update_list[i]
                inserted_node = new_nodes[i]
                right = node.right
                node.right = inserted_node
                inserted_node.left = node
                right.left = inserted_node
                inserted_node.right = right
       
        self.map[key] = value
        return True

    def getRandomLevel(self):
        level = 1
        while level < self.max_level and random.uniform(0,1) < self.prob:
            level += 1 
        return level
    
    def remove(self, key):
        if not self.contain(key):
            return True
        
        # delete key in skiplist
        node = self.find_node_at_leaf(key)
        while node != None:
            left = node.left
            right = node.right
            left.right = right
            right.left = left
            node = node.above

        # delete key in the map
        del self.map[key]

        return True
    
    def contain(self, key):
        return key in self.map

    def find_node_at_leaf(self, key):
        # return either the exact node with same key, 
        # or the biggest one that is smaller than key
        level_node = self.head
        leaf_node = None
        while level_node != None:
            row_node = level_node
            while row_node != None and row_node.key <= key:
                row_node = row_node.right
            if row_node.left.key == key and row_node.left.isLeaf:
                leaf_node = row_node.left
                break
            level_node = row_node.left.below
        return leaf_node
        
    def print_object(self):
        print ("\n********** Printing SkipList **********")
        level_node = self.head
        res = []
        while level_node != None:
            row_str = ""
            row_node = level_node
            while row_node != None:
                row_str += str(row_node.key) + ","
                row_node = row_node.right
            res.append(row_str)
            level_node = level_node.below
        
        for i in range(len(res)):
            print ("Level", i)
            print (res[i])

obj = SkipList(5, 0.7)
obj.put(1,"1")
obj.put(3,"3")
obj.put(2,"2")
obj.put(0,"0")
obj.put(11,"11")
obj.put(20,"1")
obj.put(23,"3")
obj.put(22,"2")
obj.put(50,"0")
obj.put(31,"11")
obj.print_object()
obj.remove(3)
obj.remove(0)
obj.remove(2)
obj.remove(1)
obj.remove(11)
obj.print_object()