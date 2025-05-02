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
        #Esta instruccion es equivalente a: if node is None. Se ejecuta cuando en algun ciclo de recursividad no hay hijo del lado que se evaluo
        if not node:
            return Node(value)
        #Filosofia BB. Los nodos de valor menor van a la izquierda, y los mayores a la derecha
        if value < node.value: #Chequea si el valor es menor al del nodo actual
            node.left = self._insert_recursive(node.left, value)# EL node.left del nodo se convierte en lo que devuelve el metodo   
        elif value > node.value: #Si no cumple el anterior if, Chequea si el valor es mayor al del nodo actual
            # SI el nodo no tiene derecha, se ejecuta el if not node, que devuelve un nodo con el valor a insertar, y se asigna como node.right del nodo, quedando insertado en el arbol
            node.right = self._insert_recursive(node.right, value)
        else:
            return node # Si el valor es igual al de un nodo ya en el arbol, solo devuelve el valor sin agregarlo
        
        # Si el value es mayor o menor al del nodo que se está evaluando, no se ahce ningun return y se aactualiza el balance y la altura del nodo
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
        # Se reemplaza el arbol entero con un arbol que no tiene el nodo con el valor dado, y con los cambios pertinentes
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        if not node:
            return node
        # Si el valor es menor al del nodo, vuelve a llamar al metodo en el nodo izquierdo. Cuando no cumple ser menor, se evalua si es mayor.
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        #  Con suficientes llamadas, y si existe, llega el momento que el value no es ni menor ni mayor al del nodo en cuestion, por contraste, es igual y se entra el else
        else:
            #Evalua si el nodo a eliminar tiene hijos. Si no tiene, devuelve None, entonces el nodo a elminar se cambia por None y se "borra".
            if node.left is None: # Si no tiene node.left y tiene right, el nodo padre se reemplaza por su nodo derecha.
                return node.right
            elif node.right is None: # SI tiene node.left, no entra al anterior if y entra a este. SI no tiene right, el padre se reemplaza por su izquierda
                return node.left
            # Si tiene ambos hijos, para mantener el principio BB, mayor derecha y menor izquierda, busca el node.right del nodo a eliminar.
            actual = node.right
            # Si el node.right tiene hijos izquierdos, quiere decir que ese hijo izquierda es mayor al del node, y menor al del node.right. Es decir, puede reemplazar al nodo a eliminar sin romper el BB
            while actual.left is not None: 
                actual = actual.left
            # Pone el nodo con el valor necesario en la variable temp
            temp = actual
            #le asigna su value al del nodo, efectivamente eliminando el valor que se queria eliminar
            node.value = temp.value
            # AL hacer esto, queda duplicado un nodo, por lo que se llama al metodo para borrar dicho nodo duplicado
            node.right = self._delete_recursive(node.right, temp.value)
            
        if node is None:
            return node
        # Mismo proceso del insert recursivo
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
        resultado = [] #Una lista vacia
        self._inorden_recursivo(self.root, resultado) # Se llama al recorrido recursivo
        return ', '.join(map(str, resultado)) #Regresa los elementos de la lista separados por comas y en forma de string, que se itera con map()
    
    def _inorden_recursivo(self, node, resultado):
        if node:
            self._inorden_recursivo(node.left, resultado)
            resultado.append(node.value)
            self._inorden_recursivo(node.right, resultado)
            # Las listas se pasan como referencia, es decir, no se hace copia de la lista cuando se modifica o se pasa como parametro. Para el metodo, esto significa que la misma lista que se pasa con el node.left es a la que se hace append. En sintesis, cada llamada a resultado modifica la misma lista sin necesidad de escribir la orden explicitamente. Por eso funciona esta forma

            
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
