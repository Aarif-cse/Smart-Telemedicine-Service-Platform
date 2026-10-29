"""Shows one AVL rotation step by step (left rotation on a right-heavy chain)."""
from avl_tree import AVLTree

tree = AVLTree()
for pid in (10, 20, 30):
    tree.insert(pid, None)
    print(f"Inserted {pid}: root = {tree.root.key}, height = {tree.height()}, rotations = {tree.rotations}")

print("Inorder:", [k for k, _ in tree.inorder()])
print("Left child of root :", tree.root.left.key)
print("Right child of root:", tree.root.right.key)
