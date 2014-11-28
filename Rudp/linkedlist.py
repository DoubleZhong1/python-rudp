__author__ = 'brianhoffman'




class Node():

    def __init__(self, value):
        self.value = value
        self._child_node = None


# TODO: do note that this is an ordered linked-list. Perhaps this class should
#     be renamed to better indicate that.
# TODO: use a generator/iterator pattern for looping through the list.
class LinkedList():

    def __init__(self, order_by):
        print 'Init LinkedList'

        self._child_node = None
        self._order_by = order_by
        self._current_node = None

        self.insertion_result = {}
        self.insertion_result['INSERTED'] = 'inserted'
        self.insertion_result['EXISTS'] = 'exists'
        self.insertion_result['FAILED'] = 'failed'

    def insert(self, obj):
        if not self._child_node:
            self._child_node = Node(obj)
            self._current_node = self._child_node
            return self.insertion_result.get('INSERTED')

        return self._insert(self, obj)

    def clear(self):
        self._child_node = None
        self._current_node = None

    def resetIndex(self):
        self._current_node = self._child_node

    def seek(self):
        if not self._current_node:
            return False

        if not self._current_node._child_node:
            return False

        self._current_node = self._current_node._child_node
        return True

    def currentValue(self):
        if not self._current_node:
            raise LookupError('There aren\'t any nodes on the list.')

        return self._current_node.value

    def hasValue(self):
        return bool(self._child_node)

    def nextValue(self):
        if not self._current_node:
            raise LookupError('There aren\'t any nodes on the list.')
        elif not self._current_node._child_node:
            raise LookupError('The current node does not have any child nodes')

        return self._current_node._child_node.value

    def hasNext(self):
        return bool(self._current_node._child_node)

    def toArray(self):
        return self._toArray(self, [])

    def _toArray(self, node, accum):
        if not node._child_node:
            return accum
        return self._toArray(node._child_node, accum + [node._child_node.value])

    def _insert(self, parentNode, obj):
        if not parentNode._child_node:
            parentNode._child_node = Node(obj)
            return self.insertion_result.get('INSERTED')

        order = self._order_by(obj, parentNode._child_node.value)

        if order <= -1:
            node = Node(obj)
            node._child_node = parentNode._child_node
            parentNode._child_node = node;
            return self.insertion_result.get('INSERTED')
        elif order >= 1:
            return self._insert(parentNode._child_node, object)
        elif order is 0:
            return self.insertion_result.get('EXISTS')

        return self.insertion_result.get('FAILED')
