# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
    def printList(self):
        print self.val,
        if(self.next):
            print "->",
            self.next.printList()

class Solution:
    # @param a ListNode
    # @return a ListNode
    def swapPairs(self, head):
        if head is None:
            return None
        p = head
        q = head.next
        if q is None:
            return p
        t = q.next
        q.next=p
        p.next = self.swapPairs(t)
        return q

if __name__=="__main__":

    t1 = ListNode(1)
    t2 = ListNode(2)
    t3 = ListNode(3)
    t4 = ListNode(4)
    t1.next=t2
    t2.next=t3
    t3.next=t4
    t1.printList()
    a = Solution()
    b = a.swapPairs(t1)
    print 
    b.printList()

    print 
    t1 = ListNode(1)
    t2 = ListNode(2)
    t3 = ListNode(3)
    t4 = ListNode(4)
    t5 = ListNode(5)
    t1.next=t2
    t2.next=t3
    t3.next=t4
    t4.next=t5
    t1.printList()
    a = Solution()
    b = a.swapPairs(t1)
    print 
    b.printList()
