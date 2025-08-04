# 1.3.1.1. Luận lý trong Python
# •	Thay a = True, b = False bằng a = 3 > 5, b = 4 != 4. Giải thích đầu ra.
a = 3 > 5
b = 4 != 4
print(" a and b", a and b)
# 3 > 5 là sai => a là false
# 4 khác 4 là sai => b là false
# A ^ B là false

# •	Thử thay a ^ b bằng a and (not	 b) và so sánh kết quả.
a = True
b = False
a = a ^ b
print(a)
print(" a and (not b)", a and (not b) )

# •	Dùng phép so sánh ==, !=, <, > trong một ví dụ tổng hợp để kết hợp với and, or.
a = 3 < 6
b = 6 == 7
c = 3 != 2
print ( "a and b ", a and b)
print ( "a or b ", a or b)
print ( "c and a", c and a)

# 1.3.1.2. Biểu thức điều kiện if
# •	Thêm điều kiện elif nhiet_do < 50: → xử lý "Nước lạnh".
def kiemtra_nuocsoi(nhiet_do):
    if nhiet_do < 50:
        return "Nước lạnh"
    elif nhiet_do < 100:
        return "Nước chưa sôi"
    else:
        return "Nước đã sôi"
print(kiemtra_nuocsoi(99))
print(kiemtra_nuocsoi(100))
# •	Viết lại hàm bằng cú pháp ngắn gọn return "..." if ... else "...".
def kiemtra_nuocsoi(nhiet_do):
    return "Nước sôi" if nhiet_do >= 100 else "Nước chưa sôi" if nhiet_do > 50 else "Nước lạnh"
print(kiemtra_nuocsoi(49))
print(kiemtra_nuocsoi(100))
# •	Kiểm tra hàm với giá trị âm (-10) và giải thích logic hoạt động.
def kiemtra_nuocsoi(nhiet_do):
    return "Nước sôi" if nhiet_do >= 100 else "Nước chưa sôi" if nhiet_do > 50 else "Nước lạnh"
print(kiemtra_nuocsoi(-10))
# ===> Với nhiệt độ là -10 thì nhiệt độ nhỏ hơn 100 nên sẽ không trả về "Nước sôi", tương tự, nhiệt độ nhỏ hơn 50 nên sẽ trả về "Nước lạnh"
# 1.3.1.3.
# •	Thay a = True, b = print("B được kiểm tra") or True → Quan sát xem print() có chạy không.
a = True
b = print("B được kiểm tra") or True
print(a and b) 
print(a or b)
# => print có chạy
# •	Thay a = False, b = print("B được kiểm tra") or True → So sánh xem lúc này print() có chạy không? Vì sao?
a = False
b = True
b = print("B được kiểm tra") or True
print(a and b)  # False
print(a or b)   # True
# => print có chạy vì print trả về None và kết quả của None và True là True 
# •	Viết lại 2 biểu thức phức tạp hơn:
# x = 0
# print(x != 0 and (10 / x) > 1)  # Điều kiện đầu tiên sai, điều kiện sau không bị kiểm tra
# → Giải thích vì sao chương trình không lỗi.
# => Chương trình không lỗi vì điều kiện đầu luôn sai và điều kiện sau không được kiểm tra
# 1.3.2.1. Kiểu set – tập hợp không thứ tự
#Thay 2 * x bằng 2 * x + 1. Tập S mới đại diện cho tập gì?
S = {2*x+1 for x in range(10)}  # tập các số chẵn từ 0 đến 18
 
# Các phép toán
print(S) # tập các số lẻ từ 1 đến 19
print(len(S)) # 10 phần tử lẻ khác nhau, không có kq trùng nhau
A = {1, 2, 3}
B = {2, 3, 4}

A.add(5)
print("A sau khi thêm 5:", A) # thêm phần tử 5 vào A sẽ là: A = {1,2,3,5}
print("A union B:", A.union(B)) # hợp cả A và B và loại kq trùng: {1,2,3,4,5}
print(A.union(B))        # {1, 2, 3, 4}
print(A.intersection(B)) # {2, 3}
print(A - B)             # {1}
print(B - A)             # {4} B - A là các phần tử có trong B nhưng không có trong A → {4}
# 1.3.2.2. Kiểm tra thuộc tính tập hợp
# Thêm C và C là tập con của      
A = {1, 2, 3}
B = {2, 3, 4}
C = {2, 3}
print("C là tập con của A?", C.issubset(A))

# kiểm tra A.issubset(C) và B.issubset(C)
A = {1, 2, 3}
B = {2, 3, 4}
C = {2, 3}                 
print("A là con của C?", A.issubset(C))
print("B là con của C?", B.issubset(C))

#Kiểm tra điều kiện
print("set() == set([]) ", set() == set([]))

#Tạo tập rỗng D = set(). Ktra D.issubset(A) và A.issubset(D)
A = {1, 2, 3}
D = set()  
print("D là tập con của A?", D.issubset(A))        
print("A là tập cha của D?", A.issuperset(D))
