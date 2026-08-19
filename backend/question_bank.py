"""Tree DSA practice problems used by the LeetCode-style workspace."""

QUESTIONS = [
    {"id": "inorder", "title": "Binary Tree Inorder Traversal", "difficulty": "Easy", "prompt": "Given the root of a binary tree, return the inorder traversal of its node values.", "examples": "Input: [1,null,2,3]\nOutput: [1,3,2]", "starter": "def inorder_traversal(root):\n    # Write your solution\n    pass"},
    {"id": "max-depth", "title": "Maximum Depth of Binary Tree", "difficulty": "Easy", "prompt": "Return the maximum depth of a binary tree.", "examples": "Input: [3,9,20,null,null,15,7]\nOutput: 3", "starter": "def max_depth(root):\n    # Write your solution\n    pass"},
    {"id": "same-tree", "title": "Same Tree", "difficulty": "Easy", "prompt": "Return true when two binary trees are structurally identical with equal node values.", "examples": "Input: p=[1,2,3], q=[1,2,3]\nOutput: true", "starter": "def is_same_tree(p, q):\n    pass"},
    {"id": "invert", "title": "Invert Binary Tree", "difficulty": "Easy", "prompt": "Invert a binary tree and return its root.", "examples": "Input: [4,2,7,1,3,6,9]\nOutput: [4,7,2,9,6,3,1]", "starter": "def invert_tree(root):\n    pass"},
    {"id": "symmetric", "title": "Symmetric Tree", "difficulty": "Easy", "prompt": "Determine whether a binary tree is a mirror of itself.", "examples": "Input: [1,2,2,3,4,4,3]\nOutput: true", "starter": "def is_symmetric(root):\n    pass"},
    {"id": "diameter", "title": "Diameter of Binary Tree", "difficulty": "Easy", "prompt": "Return the length in edges of the longest path between any two nodes.", "examples": "Input: [1,2,3,4,5]\nOutput: 3", "starter": "def diameter_of_binary_tree(root):\n    pass"},
    {"id": "balanced", "title": "Balanced Binary Tree", "difficulty": "Easy", "prompt": "Determine whether every node has left and right subtree heights differing by at most one.", "examples": "Input: [3,9,20,null,null,15,7]\nOutput: true", "starter": "def is_balanced(root):\n    pass"},
    {"id": "level-order", "title": "Binary Tree Level Order Traversal", "difficulty": "Medium", "prompt": "Return node values level by level from left to right.", "examples": "Input: [3,9,20,null,null,15,7]\nOutput: [[3],[9,20],[15,7]]", "starter": "def level_order(root):\n    pass"},
    {"id": "right-view", "title": "Binary Tree Right Side View", "difficulty": "Medium", "prompt": "Return the values visible when looking at the tree from the right side.", "examples": "Input: [1,2,3,null,5,null,4]\nOutput: [1,3,4]", "starter": "def right_side_view(root):\n    pass"},
    {"id": "good-nodes", "title": "Count Good Nodes", "difficulty": "Medium", "prompt": "Count nodes that are not smaller than every value on the root-to-node path.", "examples": "Input: [3,1,4,3,null,1,5]\nOutput: 4", "starter": "def good_nodes(root):\n    pass"},
    {"id": "validate-bst", "title": "Validate Binary Search Tree", "difficulty": "Medium", "prompt": "Determine whether a binary tree satisfies the strict BST property.", "examples": "Input: [2,1,3]\nOutput: true", "starter": "def is_valid_bst(root):\n    pass"},
    {"id": "kth-smallest", "title": "Kth Smallest Element in a BST", "difficulty": "Medium", "prompt": "Return the kth smallest value in a BST.", "examples": "Input: [3,1,4,null,2], k=1\nOutput: 1", "starter": "def kth_smallest(root, k):\n    pass"},
    {"id": "lca-bst", "title": "LCA of a BST", "difficulty": "Medium", "prompt": "Find the lowest common ancestor of two nodes in a binary search tree.", "examples": "Input: [6,2,8,0,4,7,9], p=2, q=8\nOutput: 6", "starter": "def lowest_common_ancestor(root, p, q):\n    pass"},
    {"id": "lca-binary", "title": "LCA of a Binary Tree", "difficulty": "Medium", "prompt": "Find the lowest common ancestor of two given nodes in a binary tree.", "examples": "Input: [3,5,1,6,2,0,8], p=5, q=1\nOutput: 3", "starter": "def lowest_common_ancestor(root, p, q):\n    pass"},
    {"id": "build-tree", "title": "Construct Tree from Preorder and Inorder", "difficulty": "Medium", "prompt": "Construct and return the binary tree from preorder and inorder traversal arrays.", "examples": "Input: preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]", "starter": "def build_tree(preorder, inorder):\n    pass"},
    {"id": "max-path", "title": "Binary Tree Maximum Path Sum", "difficulty": "Hard", "prompt": "Return the maximum sum of a non-empty path in a binary tree.", "examples": "Input: [-10,9,20,null,null,15,7]\nOutput: 42", "starter": "def max_path_sum(root):\n    pass"},
    {"id": "serialize", "title": "Serialize and Deserialize Binary Tree", "difficulty": "Hard", "prompt": "Design functions to serialize a binary tree into a string and restore it.", "examples": "Input: [1,2,3,null,null,4,5]", "starter": "class Codec:\n    def serialize(self, root):\n        pass\n\n    def deserialize(self, data):\n        pass"},
    {"id": "trie", "title": "Implement Trie", "difficulty": "Medium", "prompt": "Implement insert, search, and startsWith for a prefix tree.", "examples": "insert('apple'), search('app') => false", "starter": "class Trie:\n    def insert(self, word):\n        pass\n\n    def search(self, word):\n        pass"},
    {"id": "heap", "title": "Kth Largest Element", "difficulty": "Medium", "prompt": "Return the kth largest element using a heap.", "examples": "Input: nums=[3,2,1,5,6,4], k=2\nOutput: 5", "starter": "def find_kth_largest(nums, k):\n    pass"},
    {"id": "path-sum", "title": "Path Sum", "difficulty": "Easy", "prompt": "Return true if a root-to-leaf path has the target sum.", "examples": "Input: root=[5,4,8,11,null,13,4,7,2,null,null,null,1], target=22\nOutput: true", "starter": "def has_path_sum(root, target_sum):\n    pass"},
]

# The editor renders these separately from the function-only starter code.
TEST_CASES = {
    "inorder": [("root = [1,null,2,3]", "[1,3,2]"), ("root = []", "[]")],
    "max-depth": [("root = [3,9,20,null,null,15,7]", "3"), ("root = []", "0")],
    "same-tree": [("p=[1,2,3], q=[1,2,3]", "true"), ("p=[1,2], q=[1,null,2]", "false")],
    "invert": [("root = [4,2,7,1,3,6,9]", "[4,7,2,9,6,3,1]"), ("root = []", "[]")],
    "symmetric": [("root = [1,2,2,3,4,4,3]", "true"), ("root = [1,2,2,null,3,null,3]", "false")],
    "diameter": [("root = [1,2,3,4,5]", "3"), ("root = [1,2]", "1")],
    "balanced": [("root = [3,9,20,null,null,15,7]", "true"), ("root = [1,2,2,3,3,null,null,4,4]", "false")],
    "level-order": [("root = [3,9,20,null,null,15,7]", "[[3],[9,20],[15,7]]"), ("root = []", "[]")],
    "right-view": [("root = [1,2,3,null,5,null,4]", "[1,3,4]"), ("root = [1,null,3]", "[1,3]")],
    "good-nodes": [("root = [3,1,4,3,null,1,5]", "4"), ("root = [1]", "1")],
    "validate-bst": [("root = [2,1,3]", "true"), ("root = [5,1,4,null,null,3,6]", "false")],
    "kth-smallest": [("root=[3,1,4,null,2], k=1", "1"), ("root=[5,3,6,2,4,null,null,1], k=3", "3")],
    "lca-bst": [("root=[6,2,8,0,4,7,9], p=2, q=8", "6"), ("p=2, q=4", "2")],
    "lca-binary": [("root=[3,5,1,6,2,0,8], p=5, q=1", "3"), ("p=5, q=4", "5")],
    "build-tree": [("pre=[3,9,20,15,7], in=[9,3,15,20,7]", "[3,9,20,null,null,15,7]"), ("pre=[-1], in=[-1]", "[-1]")],
    "max-path": [("root=[-10,9,20,null,null,15,7]", "42"), ("root=[-3]", "-3")],
    "serialize": [("root=[1,2,3,null,null,4,5]", "same tree after deserialize"), ("root=[]", "empty tree")],
    "trie": [("insert('apple'), search('apple')", "true"), ("startsWith('app')", "true")],
    "heap": [("nums=[3,2,1,5,6,4], k=2", "5"), ("nums=[3,2,3,1,2,4,5,5,6], k=4", "4")],
    "path-sum": [("root=[5,4,8,11,null,13,4,7,2], target=22", "true"), ("root=[1,2,3], target=5", "false")],
}

for question in QUESTIONS:
    question["test_cases"] = TEST_CASES[question["id"]]
