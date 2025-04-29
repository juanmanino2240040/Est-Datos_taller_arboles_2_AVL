import sys 

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 


def getHeight(node):
    if not node:
        return 0
    return node.height

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

def rotate_right(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x

def rotate_left(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node 
        
        updateHeight(node)
        
        balance = getBalance(node)

        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node) 
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node) 
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node) 
        
        return node
    
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        if not node:
            return node
    
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            actual = node.right
            while actual.left is not None:
                actual = actual.left
            temp = actual
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)
            
        if node is None:
            return node
        
        updateHeight(node)
        
        balance = getBalance(node)
        
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node) 
        elif balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node) 
        elif balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)
        elif balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)
        
        return node
    
    def _inorden(self):
        resultado = []
        self._inorden_recursivo(self.root, resultado)
        return ', '.join(map(str, resultado))
    
    def _inorden_recursivo(self, node, resultado):
        if node:
            self._inorden_recursivo(node.left, resultado)
            resultado.append(node.value)
            self._inorden_recursivo(node.right, resultado)
            
    def _mostrar_arbol(self):
        self._mostrar_arbol_recursivo(self.root, "", True)
    
    def _mostrar_arbol_recursivo(self, node, indent, last):
        if node:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(node.value)
            self._mostrar_arbol_recursivo(node.left, indent, False)
            self._mostrar_arbol_recursivo(node.right, indent, True)

# Prueba del árbol AVL
avl = AVLTree()
values_to_insert = [10, 20, 30, 40, 50, 25]

print("Insertando valores:", values_to_insert)
for val in values_to_insert:
    avl.insert(val)


print("\n--- Árbol AVL después de inserciones ---")
avl._mostrar_arbol()
print("\n--- Árbol AVL después de eliminacion de la raiz ---")
avl.delete(30)
avl._mostrar_arbol()
print(avl._inorden())
    



