class interval():
    def __init__(self, i0, i1):
        assert i0<=i1
        self.i0=i0
        self.i1=i1

    def __add__(self,other):
        if isinstance(other,(int, float)):
            return interval(self.i0+other, self.i1+other)
        elif isinstance(other, interval):
            return interval(self.i0+other.i0, self.i1+other.i1)
        else:
            raise ValueError(f"unsupported operand type(s) for +: 'interval' and '{other.__class__.__name__}'")

    def __sub__(self,other):
        if isinstance(other,(int, float)):
            return interval(self.i0-other, self.i1-other)
        elif isinstance(other, interval):
            return interval(self.i0-other.i1, self.i1-other.i0)
        else:
            raise ValueError(f"unsupported operand type(s) for -: 'interval' and '{other.__class__.__name__}'")

    def __mul__(self, other):
        if isinstance(other,(int, float)):
            if other>=0:
                return interval(self.i0*other, self.i1*other)
            else:
                return interval(self.i1*other, self.i0*other)
        elif isinstance(other, interval):
            min_i=min(self.i0*other.i0, self.i0*other.i1, self.i1*other.i0, self.i1*other.i1)
            max_i=max(self.i0*other.i0, self.i0*other.i1, self.i1*other.i0, self.i1*other.i1)
            return interval(min_i, max_i)
        else:
            raise ValueError(f"unsupported operand type(s) for *: 'interval' and '{other.__class__.__name__}'")

    def __truediv__(self, other):
        if isinstance(other,(int, float)):
            return self * (1/other)
        elif isinstance(other, interval):
            if other.i0*other.i1<0:
                return 1/0
            else:
                return self*interval(1/other.i1,1/other.i0)
        else:
            raise ValueError(f"unsupported operand type(s) for /: 'interval' and '{other.__class__.__name__}'")

    def __contains__(self, item):
        if isinstance(item,(int, float)):
            return True if self.i0<=item<=self.i1 else False
        else:
            raise ValueError(f"in 'interval' requires 'int' or 'float' as left operand, not '{item.__class__.__name__}'")

    def __abs__(self):
        return max(abs(self.i0),abs(self.i1))

    def width(self):
        return self.i1-self.i0

    def middle(self):
        return 0.5*(self.i0+self.i1)

    def radius(self):
        return 0.5*(self.i1-self.i0)

    def __radd__(self,other):
        return self+other

    def __rmul__(self,other):
        return self*other

    def __rsub__(self, other):
        if isinstance(other,(int, float)):
            return interval(other-self.i0, other-self.i1)
        else:
            raise ValueError(f"unsupported operand type(s) for -: 'interval' and '{other.__class__.__name__}'")

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return interval(other/self.i0, other/self.i1) if other<=0 else interval(other/self.i1, other/self.i0)
        else:
            raise ValueError(f"unsupported operand type(s) for /: 'interval' and '{other.__class__.__name__}'")


    def __str__(self):
        return f"[{self.i0: ^3.3f}; {self.i1: ^3.3f}]"


def det(A):
    return A[0][0]*A[1][1]-A[0][1]*A[1][0]


def inverse_matrix(A):
    new_A=[[] for i in range(2)]            
    a=A[0][0]; b=A[0][1]; c=A[1][0]; d= A[1][1]
    
    if 0 not in d:
        new_A[0].append(1/(a-b*c/d))
    else:
        a0=d.i1/(d.i1*a-b*c)
        a1=d.i0/(d.i0*a-b*c)
        new_A[0].append(interval(a0.i0,a1.i1))

    if 0 not in b:
        new_A[0].append(-1/(a*d/b-c))
    else:
        a0=-b.i1/(a*d-b.i1*c)
        a1=-b.i0/(a*d-b.i0*c)
        new_A[0].append(interval(a0.i0,a1.i1))

    if 0 not in c:
        new_A[1].append(-1/(a*d/c-b))
    else:
        a0=-c.i1/(a*d-b*c.i1)
        a1=-c.i0/(a*d-b*c.i0)
        new_A[1].append(interval(a0.i0,a1.i1))
               
    if 0 not in a:
        new_A[1].append(1/(d-b*c/a))
    else:
        a0=a.i1/(a.i1*d-b*c)
        a1=a.i0/(a.i1*d-b*c)
        new_A[1].append(interval(a0.i0,a1.i1))
               
    return new_A


def mult_matrixes(inverse_A,B):
    X=[interval(0,0) for i in range(2)]
    for i in range(len(inverse_A)):
        for k in range(len(inverse_A[i])):
            X[i]=X[i]+inverse_A[i][k]*B[k]
    return X


def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[i])):
            print(A[i][j], end="\t")
        print()



# 1
i1=list(map(float,input("Введіть через пробіл межі першого інтервалу ").split()))
i2=list(map(float,input("Введіть через пробіл межі другого інтервалу ").split()))
interval_1=interval(*i1)
interval_2=interval(*i2)
print(f"Введені інтервали {interval_1} тa {interval_2}")
print(f"Cума інтевалів {interval_1+interval_2}")
print(f"Різниця інтевалів {interval_1-interval_2}")
print(f"Добуток інтевалів {interval_1*interval_2}")
print(f"Частка інтевалів {interval_1/interval_2}",end='\n\n') #if res_interval is not None  else print(f"Ділення неможливе {interval_2} містить 0")

my_interval=interval(-15.2, 1.7)
print(f"Заданий інтервал {my_interval}")
print(f"Середина інтервалу {my_interval.middle()}")
print(f"Ширина інтервалу {my_interval.width()}")
print(f"Радіус інтервалу {my_interval.radius()}")
print(f"Абсолютне значення інтервалу {abs(my_interval)}",end='\n\n')

# 2

A=[[interval(1, 2), interval(-1, 2)],
   [interval(-1, 1), interval(1, 3)]]
B=[interval(-1, 1), interval(1, 2)]
#B=[interval(-1, 1), interval(0, 2)]
print("Матриця A:")
print_matrix(A)
print("Матриця B:")
#print_matrix(B)
d=det(A)
print(f"Визначник матриці A={d}")
print("Матриця A невироджена") if 0 not in d else print("Матриця A вироджена")

# візьмемо a=[11,12]
A_2=[[interval(11, 12), interval(-1, 2)],
     [interval(-1, 1), interval(1, 3)]]
#A_2=[[interval(2,4),interval(-2,0)],
#     [interval(-1,1),interval(2,4)]]
print("Матриця A2:")
print_matrix(A_2)
d=det(A_2)
print(f"Визначник матриці A2={d}")
print("Матриця A2 невироджена") if 0 not in d else print("Матриця A2 вироджена")

inverse_A_2=inverse_matrix(A_2)
print("Обернена до матриці A:")
print_matrix(inverse_A_2)
X=mult_matrixes(inverse_A_2,B)
print("Результат Х:",*X)