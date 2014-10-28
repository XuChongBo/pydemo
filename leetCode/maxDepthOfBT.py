# Definition for a  binary tree node
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    # @param root, a tree node
    # @return an integer
    def maxDepth(self, root):
        if root is None:
            return 0
        l = self.maxDepth(root.left)
        r = self.maxDepth(root.right)
        m = l if l>r else r
        return m+1


if __name__=="__main__":
    t0 = TreeNode(11)
    t1 = TreeNode(12)
    t0.left=t1

    a = Solution()
    print a.maxDepth(t0)
