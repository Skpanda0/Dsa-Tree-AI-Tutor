# Tree Data Structures and Algorithms

## Core terms
A tree is a connected acyclic graph. A rooted tree names one node as the root. A node's children are the nodes immediately below it; a leaf has no children. The height of a node is the number of edges on its longest downward path. A tree with n nodes has n - 1 edges.

## Binary trees
In a binary tree each node has at most two children, conventionally left and right. A full binary tree has either zero or two children at every node. A complete binary tree fills each level from left to right, except possibly the final level. A perfect binary tree has all internal nodes with two children and all leaves at the same depth.

## Traversals
Depth-first traversal visits a branch before another branch. Preorder is node, left, right. Inorder is left, node, right; for a binary search tree it emits keys in sorted order. Postorder is left, right, node, and is useful when deleting or evaluating subtrees. Breadth-first traversal (level order) uses a queue and visits one level at a time. Every traversal takes O(n) time; DFS uses O(h) call-stack space and BFS can use O(w) queue space, where h is height and w is maximum width.

## Binary search trees
For every BST node, all keys in its left subtree are smaller and all keys in its right subtree are larger (with a consistent duplicate policy). Search, insert, and delete take O(h) time. They are O(log n) on a balanced tree but O(n) on a skewed tree. To delete a node with two children, replace its value with its inorder successor (minimum in right subtree) or predecessor (maximum in left subtree), then delete that replacement node.

## Balanced trees
AVL trees maintain a balance factor of -1, 0, or 1 for each node and use rotations after insertion or deletion. Red-black trees use coloring invariants and rotations to keep height O(log n). A left rotation promotes a right child; a right rotation promotes a left child. Balanced BST operations run in O(log n).

## Heaps
A binary heap is a complete binary tree usually stored in an array. In a zero-indexed array, a node at i has children 2i + 1 and 2i + 2, and parent floor((i - 1) / 2). A min-heap keeps each parent no larger than its children; a max-heap reverses that relation. Peek is O(1), insertion and removal are O(log n), and bottom-up heap construction is O(n).

## Trie
A trie stores strings by characters along root-to-node paths. Insertion, lookup, and prefix lookup take O(L), where L is the query length. Each node has child references and often an end-of-word marker. Tries are useful for autocomplete and prefix search, at a memory cost.

## Lowest common ancestor
The lowest common ancestor (LCA) of two nodes is their deepest shared ancestor. In a BST, compare both values with the current node: move left if both are smaller, right if both are larger, otherwise the current node is the LCA. In a general binary tree, recursively search both subtrees; a node where both searches succeed is the LCA.

## Common patterns
Use recursion when the result depends naturally on child results: height, balanced-tree checking, diameter, path sum, and subtree validation. Use an explicit stack to avoid recursion-depth limits. For level-based questions, use BFS and process the queue size for each level. Track a global or returned best value carefully for diameter and maximum path sum.
