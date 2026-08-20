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

## Building and representing trees
Interview problems commonly provide a tree through a `TreeNode` with `val`, `left`, and `right` fields, or as a level-order array where `null` means a missing child. A level-order array is not a heap unless the problem says it is: it is simply a compact way to describe the tree. When constructing from such an array, consume children with a queue and do not create nodes for `null` values. Clarify whether node values are unique before using values as identifiers.

## Recursion contracts
For a recursive helper, state exactly what it returns before writing code. For example, `height(node)` returns the height of the subtree rooted at `node`, and its base case for an empty subtree is usually `0`. A helper that validates balance can return `-1` for an invalid subtree and a non-negative height otherwise; this avoids recalculating heights and keeps the whole algorithm O(n). Prefer returning the information a parent needs over relying on mutable global state.

## BST validation and duplicates
Checking only that a node is greater than its left child and smaller than its right child is insufficient: a deep descendant can still violate an ancestor's bound. Validate a BST by carrying lower and upper bounds down the recursion, or by confirming that an inorder traversal is strictly increasing. Decide the duplicate policy up front. If duplicates go consistently to one side, make the corresponding comparison inclusive and keep that policy for search, insertion, and validation.

## Paths, diameter, and backtracking
A root-to-leaf path problem normally needs a path-local list. Append a node before exploring its children, then remove it when returning so sibling branches do not share stale values. For diameter measured in edges, each node can contribute `leftHeight + rightHeight`; update the best answer while a height helper returns `1 + max(leftHeight, rightHeight)`. A maximum path sum differs because a path may start and end anywhere: discard a child contribution when it is negative.

## Choosing iterative traversal
Use an explicit stack when recursion depth might exceed the language limit. Iterative preorder pushes right before left so left is processed first. Iterative inorder repeatedly pushes the left spine, visits one node, then moves right. Postorder can use a visited flag or two stacks. For BFS, use a queue with an index or deque-style structure; repeatedly removing from the front of a JavaScript array can make a linear traversal accidentally quadratic.

## Edge cases checklist
Before finalizing a tree solution, test an empty tree, one node, a completely skewed tree, duplicate values when allowed, negative values for sum problems, and a case where the answer lies entirely in one subtree. Check whether a problem defines height and diameter in nodes or edges, whether targets are guaranteed to exist, and whether modifying the input tree is allowed.
