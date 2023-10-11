import pickle
import json
import os
from datetime import datetime
from uuid import uuid4 # para generar IDs
# Load data, provide a menu for the user to manage employees,
# invoices, and generate reports.
class Codec:
    def find_path(self, filename):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, filename)
    
    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    
    def upload(self, path, archive):
        with open(path, 'w') as f:
            json.dump(archive, f, indent=3)

    def serialize(self, root, path):
        """Encodes a tree to a list of dictionaries."""
        if not root:
            return []
        stack = [root]
        res = []
        
        while stack:
            tmp = stack.pop(0)
            if not tmp:
                res.append(None)
            else:
                # Append a dictionary representing an employee node
                res.append({
                    "name": tmp.name,
                    "position": tmp.position,
                    "salary": tmp.salary,
                    "hiring_date": tmp.hiring_date.strftime("%Y-%m-%d")
                })
                stack.append(tmp.left)
                stack.append(tmp.right)
		
        self.upload(self.find_path(path), res)
        return res

    def deserialize(self, path, t):
        data = self.load(path)
        if t == 0:
            tree = EmployeeBinaryTree()
        else:
            tree = AVLTree()
        return create_tree(data, tree)

class EmployeeNode:
    def __init__(self, name=None, position=None, salary=None, hiring_date=None):
        self.name = name
        self.position = position
        self.salary = salary
        # Convert the hiring date string to a datetime object
        self.hiring_date = datetime.strptime(hiring_date, "%Y-%m-%d").date() if hiring_date else None
        self.left = None
        self.right = None
        
class EmployeeBinaryTree:
    def __init__(self):
        self.root = None

    def height(self):
        """Return the height of the tree."""
        return self._height(self.root)

    def _height(self, node):
        """Recursive helper method to compute the height."""
        if node is None:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return 1 + max(left_height, right_height)

    def insert(self, employee):
        if employee is None:
            return None
        if self.root is None:
            self.root = EmployeeNode(employee["name"], employee["position"], employee["salary"], employee["hiring_date"])
        else:
            self._insert_recursively(self.root, employee)

    def _insert_recursively(self, current, employee):
        if datetime.strptime(employee['hiring_date'], "%Y-%m-%d").date()< current.hiring_date:
            if current.left is None:
                current.left = EmployeeNode(employee["name"], employee["position"], employee["salary"], employee["hiring_date"])
            else:
                self._insert_recursively(current.left, employee)
        elif datetime.strptime(employee['hiring_date'], "%Y-%m-%d").date()>current.hiring_date:
            if current.right is None:
                current.right = EmployeeNode(employee["name"], employee["position"], employee["salary"], employee["hiring_date"])
            else:
                self._insert_recursively(current.right, employee)

    def find_by_name(self, name):
        """Search for an employee by name."""
        return self._find_by_name(self.root, name.lower())

    def _find_by_name(self, current, name):
        """Recursive helper method to search for an employee by name."""
        if current is None:
            return None
        if current.name.lower() == name:
            return current
        # Search in the left and right subtrees
        found = self._find_by_name(current.left, name)
        if found:
            return found
        return self._find_by_name(current.right, name)

    def find(self, hiring_date):
        return self._find_recursively(self.root, hiring_date)
    
    def _find_recursively(self, current, hiring_date):
        if current is None or current.hiring_date == hiring_date:
            return current
        if hiring_date < current.hiring_date:
            return self._find_recursively(current.left, hiring_date)
        return self._find_recursively(current.right, hiring_date)

    def delete(self, employee):
        if employee is None:
            return None
        self.root = self._delete_recursively(self.root, employee.hiring_date)

    def _delete_recursively(self, current, hiring_date):
        if current is None:
            return None
        if hiring_date < current.hiring_date:
            current.left = self._delete_recursively(current.left, hiring_date)
        elif hiring_date > current.hiring_date:
            current.right = self._delete_recursively(current.right, hiring_date)
        else:
            if current.left is None:
                return current.right
            elif current.right is None:
                return current.left
            else:
                successor = self._find_min(current.right)
                current.name = successor.name
                current.position = successor.position
                current.salary = successor.salary
                current.hiring_date = successor.hiring_date
                current.right = self._delete_recursively(current.right, successor.hiring_date)
        return current

    def _find_min(self, current):
        if current.left is None:
            return current
        return self._find_min(current.left)

    def modify(self, old, new):
        self.delete(old)
        self.insert(new)
#LIST PRE ORDER BUT BY HIRING DATE? ASK
    def inorder(self):
        self._recursive_inorder(self.root)
    def _recursive_inorder(self, current):
        cont = 0
        if current is not None:
            if cont==6:
                return
            self._recursive_inorder(current.left)
            print("Nombre y apellido: ",current.name)
            print("Cargo: ",current.position)
            print("Salario: ",current.salary)
            print("Fecha de contratación: ",current.hiring_date)
            print("\n")
            cont+=1
            self._recursive_inorder(current.right)

    def preorder(self):
        self._recursive_preorder(self.root)
        
    def _recursive_preorder(self, current):
        if current is not None:
            print("Nombre y apellido: ",current.name)
            print("Cargo: ",current.position)
            print("Salario: ",current.salary)
            print("Fecha de contratación: ",current.hiring_date)
            print("\n")
            self._recursive_preorder(current.left)
            self._recursive_preorder(current.right)

    def postorder(self):
        self._recursive_postorder(self.root)
    def _recursive_postorder(self, current):
        if current is not None:
            self._recursive_postorder(current.left)
            self._recursive_postorder(current.right)
            print("Nombre y apellido: ",current.name)
            print("Cargo: ",current.position)
            print("Salario: ",current.salary)
            print("Fecha de contratación: ",current.hiring_date)
            print("\n")

class InvoiceNode:
    def __init__(self, total, additional_services, payment_method, payment_status):
        self.total = total
        if additional_services is None:
            self.additional_services = "Sin servicios adicionales"
        else:
            self.additional_services = additional_services
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self):
        """Return the height of the tree."""
        return self._height(self.root)

    def _height(self, node):
        """Recursive helper method to compute the height."""
        if node is None:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return 1 + max(left_height, right_height)

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # Rotate functions
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        # Rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, y):
        z = y.left
        T3 = z.right

        # Rotation
        z.right = y
        y.left = T3

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))

        return z

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    # Insertion method
    def insert(self, invoice):
        if not self.root:
            self.root = InvoiceNode(invoice['total'], invoice['additional_services'],
                                    invoice['payment_method'], invoice['payment_status'])
        else:
            self.root = self._insert(self.root, invoice)

    def _insert(self, node, invoice):
        # Normal BST insertion
        if not node:
            return InvoiceNode(invoice['total'], invoice['additional_services'],
                               invoice['payment_method'], invoice['payment_status'])

        # total uniquely identifies an invoice
        if invoice['total'] < node.total:
            node.left = self._insert(node.left, invoice)
        else:
            node.right = self._insert(node.right, invoice)

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Get balance factor
        balance = self._get_balance(node)

        # If unbalanced, perform rotations

        # Left Left
        if balance > 1 and invoice['total'] < node.left.total:
            return self._right_rotate(node)

        # Right Right
        if balance < -1 and invoice['total'] > node.right.total:
            return self._left_rotate(node)

        # Left Right
        if balance > 1 and invoice['total'] > node.left.total:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left
        if balance < -1 and invoice['total'] < node.right.total:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def postorder(self, payment_method):
        self._recursive_postorder(self.root, payment_method)
    def _recursive_postorder(self, current, payment_method):
        if current is not None:
            self._recursive_postorder(current.left, payment_method)
            self._recursive_postorder(current.right, payment_method)
            if payment_method == current.payment_method:
                print("Monto total: ",current.total)
                print("Servicios adicionales: ",current.additional_services)
                print("Método de pago: ",current.payment_method)
                print("Estado de pago: ",current.payment_status)
                print("\n")

def create_tree(data, tree):
    while data:
        tree.insert(data.pop(0))
    return tree

def create_employee(tree):
    flag = True
    employee = {}
    while flag:
        name = input("\nNombre y apellido: ")
        if name == '':
            print("\nEl campo del nombre es obligatorio.")
        elif tree.find_by_name(name):
            print("\n%s ya existe dentro de los empleados." %name.title())
        else:
            employee['name']=name.title()
            flag = False
    flag = True
    while flag:
        position = input("\nCargo: ")
        if position == '':
            print("\nEl campo del cargo es obligatorio.")
        else:
            employee['position']=position.title()
            flag = False
    flag = True
    while flag:
        salary=input("\nSalario: ")
        try:
            float(salary)
        except:
            print("\nEl campo del salario es obligatorio y debe ser un número.")
        else:
            employee['salary']=salary
            flag = False
    flag = True
    while flag:
        hiring_date = input("\nFecha de contratación (formato aaaa-mm-dd): ")
        try:
            datetime.strptime(hiring_date, "%Y-%m-%d").date()
            employee['hiring_date'] = hiring_date
            flag = False
        except:
            print("\nFormato de fecha inválido. Intente nuevamente.")
    return employee

def create_invoice():
    flag = True
    invoice = {}
    while flag:
        total = input("\nMonto total: ")
        try:
            float(total)
        except:
            print("\nEl campo del monto total es obligatorio y debe ser un número.")
        else:
            invoice['total']=total
            flag = False
    flag = True
    while flag:
        additional_services = input("\nServicios adicionales: ")
        if additional_services == '':
            invoice['additional_services']=("\nSin servicios adicionales.")
        else:
            invoice['additional_services']=additional_services.title()
            flag = False
    flag = True
    while flag:
        payment_method= input("\nMétodo de pago (tarjeta/efectivo/transferencia): ")
        if payment_method.lower() not in ['tarjeta', 'efectivo','transferencia']:
            print("\nEl campo del método de pago es obligatorio y solo puede ser tarjeta, efectivo o transferencia.")
        else:
            invoice['payment_method']=payment_method.title()
            flag = False
    flag = True
    while flag:
        payment_status = input("\nEstado de pago (confirmado/pendiente): ")
        if payment_status.lower() not in ['confirmado', 'pendiente']:
            print("\nEl campo del estado de pago es obligatorio y solo puede ser confirmado o pendiente.")
        else:
            invoice['payment_status']=payment_status.title()
            flag = False
    return invoice
	
def menu_hotels(hotel_chain_name):
    flag = True
    while flag:
        print("""\n%s's Hotels:
1. Valencia
2. Caracas
3. Maracay
0. Volver al menú principal""" %hotel_chain_name)
        option = input("\nSeleccione un hotel para gestionar empleados: ")
        if option == '0':
            return None
        elif option not in ['1','2','3']:
            print("\nSelección inválida. Intente nuevamente.")
        else:
            if option == '1':
                return 'Valencia'
            elif option == '2':
                return 'Caracas'
            elif option == '3':
                return 'Maracay'

    
def menu_employees(config, codec):
    hotel_chain_name = config['hotel_chain_name']
    hotel = menu_hotels(hotel_chain_name)
    if hotel is None:
        return
    employee_tree = codec.deserialize(config['file_route_name'][hotel][0], 0)
    flag = True
    while flag:
        print("\n%s's Hotels %s:" %(hotel_chain_name, hotel))
        print("""    1. Agregar empleado
    2. Modificar empleado
    3. Eliminar empleado
    4. Mostrar cinco empleados más antiguos
    5. Listar empleados por fecha de contratación
    0. Volver al menú anterior""")
        option =  input("\nSeleccione una opción: ")
        if option == '1':
            print("\nCrear nuevo empleado")
            employee_tree.insert(create_employee(employee_tree))
            codec.serialize(employee_tree.root, config['file_route_name'][hotel][0])
            print("\nEmpleado creado exitosamente.")
        elif option == '2':
            print("\nLista de empleados\n")
            employee_tree.preorder()
            old = input("\nIngrese el nombre completo del empleado a modificar: ")
            found = employee_tree.find_by_name(old.title())
            if found is None:
                print("\nNo se encontró empleado bajo ese nombre.")
            else:
                print("\nLlenar datos nuevos:")
                new = create_employee(employee_tree)
                employee_tree.modify(found, new)
                codec.serialize(employee_tree.root, config['file_route_name'][hotel][0])
                print("\nEmpleado modificado exitosamente.")
        elif option == '3':
            print("\nLista de empleados\n")
            employee_tree.preorder()
            employee = input("\nIngrese el nombre completo del empleado a eliminar: ")
            found = employee_tree.find_by_name(employee.title())
            if found is None:
                print("\nNo se encontró empleado bajo ese nombre.")
            else:
                employee_tree.delete(found)
                codec.serialize(employee_tree.root, config['file_route_name'][hotel][0])
                print("\nEmpleado eliminado exitosamente.")
        elif option == '4':
            print("\nCinco empleados más antiguos:\n")
            employee_tree.inorder()
            print("\nAltura de árbol: ", employee_tree.height())
        elif option == '5':
            print("\nEmpleados (por fecha de contratación)\n")
            employee_tree.preorder()
            print("\nAltura de árbol: ", employee_tree.height())
        elif option == '0':
            return
        else: print("\nSelección inválida. Intente nuevamente.")
        
def menu_invoices(config, codec):
    hotel_chain_name = config['hotel_chain_name']
    hotel = menu_hotels(hotel_chain_name)
    if hotel is None:
        return
    invoice_tree = codec.deserialize(config['file_route_name'][hotel][1], 1)
    flag = True
    while flag:
        print("""\nListar facturas:
1. Listar facturas
2. Crear factura
0. Menú anterior""")
        option = input('\nSeleccione una opción: ')
        if option == '0':
            return
        if option == '1':
            print("""\n    1. Efectivo
    2. Transferencia
    3. Tarjeta
    0. Menú anterior""")
            op = input("\nSeleccione un método de pago: ")
            if op not in ['0', '1', '2', '3']:
                print("\nSelección inválida. Intente nuevamente.")
            else:   
                if op == '1':
                    method = 'Efectivo'
                elif op == '2':
                    method = 'Transferencia'
                elif op == '3':
                    method = 'Tarjeta'
                print("\n%s's hotels %s: Facturas canceladas por %s\n" %(hotel_chain_name, hotel, method.lower()))
                invoice_tree.postorder(method)
                print("\nAltura de árbol: ", invoice_tree.height())
            
        elif option == '2':
            print("\nCrear nueva factura")
            invoice_tree.insert(create_invoice())
            codec.serialize(invoice_tree.root, config['file_route_name'][hotel][1])
            print("\nFactura creada exitosamente.")
            
        else: print("\nSelección inválida. Intente nuevamente.")
    

def menu(config, codec):
    hotel_chain_name = config['hotel_chain_name']
    print("\nCadena de hoteles %s's Hotels" %hotel_chain_name)
    flag = True
    while flag:
        print("""\nMenú principal:
1. Gestionar empleados
2. Gestionar facturación y pagos
0. Salir""")
        option = input('\nSeleccione una opción: ')
        if option == '0':
            return print("\nFin.")
        elif option == '1':
            menu_employees(config, codec)
        elif option == '2':
            menu_invoices(config, codec)
        else: print("\nSelección inválida. Intente nuevamente.")
            
def main():
    codec = Codec()
    try:
        config = codec.load(codec.find_path('config.json'))
    except:
        print("No se encontró el archivo config.json.")
        
    menu(config, codec)
        
main()
