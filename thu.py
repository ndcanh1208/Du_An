import json

file_account = "D:\\Python\\Du_an\\du_lieu_nguoi_dung.json"
file_do_dung = "D:\\AnDuc\\btl_pyThon2\\danh_sach_do_dung.json"
file_trai_nghiem = "D:\\AnDuc\\btl_pyThon2\\beta.json"

tai_khoan_nguoi_dung = {}
danh_sach_beta = {}
def open_file_account():
    global tai_khoan_nguoi_dung
    try:
        with open(file_account, 'r', encoding='utf-8') as f:
            tai_khoan_nguoi_dung = json.load(f)
    except:
        tai_khoan_nguoi_dung = {}
        
def doc_file_trai_nghiem():
    global danh_sach_beta
    try:
        with open(file_trai_nghiem, "r", encoding="utf-8") as f:
            danh_sach_beta = json.load(f)
    except:
        danh_sach_beta = {}

def ghi_file():
    with open(file_account, "w", encoding="utf-8") as f:
        json.dump(tai_khoan_nguoi_dung, f, indent=4)
        
def ghi_file_trai_nghiem():
    with open(file_trai_nghiem, "w", encoding="utf-8") as f:
        json.dump(danh_sach_beta, f, indent=4)

def dang_nhap():
    print("ĐĂNG NHẬP")
    ten_dang_nhap = input("Nhập tên đăng nhập: ")
    email = input("Nhập email đăng nhập: ")
    mat_khau = input("Nhập mật khẩu: ")
    if ten_dang_nhap in tai_khoan_nguoi_dung:
        tai_khoan = tai_khoan_nguoi_dung[ten_dang_nhap]
        if tai_khoan["email"] == email and tai_khoan["password"] == mat_khau:
            print("Đăng nhập thành công")
            return True
    else:
        print("Sai tài khoản hoặc mật khẩu!")
        return False

def dang_ky():
    global tai_khoan_nguoi_dung
    print("ĐĂNG KÝ")
    ten_dang_nhap = input("Nhập tên đăng nhập: ")
    if ten_dang_nhap in tai_khoan_nguoi_dung:
        print("Tên đăng nhập đã tồn tại!")
        return False
    if email in tai_khoan_nguoi_dung:
        print("Đã có tài khoản sử dụng email này!")
        return False
    email = input("Nhập email: ")
    mat_khau = input("Nhập mật khẩu: ")
    xac_nhan_mat_khau = input("Nhập lại mật khẩu: ")
    if mat_khau != xac_nhan_mat_khau:
        print("Mật khẩu không khớp!")
        return False
    ten_tai_khoan_moi = {
        "email": email,
        "password": mat_khau
    }
    tai_khoan_nguoi_dung[ten_dang_nhap] = ten_tai_khoan_moi
    ghi_file()
    print("Đăng kí tài khoản thành công!")
    return True

def doi_mat_khau():
    print("ĐỔI MẬT KHẨU")
    ten_dang_nhap = input("Nhập tên đăng nhập: ")
    mat_khau_cu = input("Nhập mật khẩu hiện tại: ")
    if ten_dang_nhap in tai_khoan_nguoi_dung:
        tai_khoan = tai_khoan_nguoi_dung[ten_dang_nhap]
        if tai_khoan["password"] == mat_khau_cu:
            mat_khau_moi = input("Nhập mật khẩu mới: ")
            xac_nhan_mat_khau = input("Nhập lại mật khẩu mới: ")
            if mat_khau_moi != xac_nhan_mat_khau:
                print("Mật khẩu không khớp!")
                return False
            tai_khoan["password"] = mat_khau_moi
            ghi_file()
            print("Đổi mật khẩu thành công!")
            return True
        print("Sai mật khẩu cũ!")
        return False
    print("Tài khoản không tồn tại!")
    return False

def xoa_tai_khoan():
    print("XÓA TÀI KHOẢN")
    ten_dang_nhap = input("Nhập tên đăng nhập: ")
    if ten_dang_nhap in tai_khoan_nguoi_dung:
        tai_khoan_nguoi_dung.pop(ten_dang_nhap)
        ghi_file()
        print("Xóa tài khoản thành công!")
        return True
    print("Tài khoản không tồn tại!")
    return False


def xem_do_dung():
    doc_file_trai_nghiem()
    if not danh_sach_beta:
        print("Không có đồ dùng nào trong danh sách.")
        return

    print("\nDanh sách đồ dùng:")
    for ma, do_dung in danh_sach_beta.items():
        print(f"{ma}. Tên: {do_dung['ten']}, Loại: {do_dung['loai']}")


def them_do_dung():
    doc_file_trai_nghiem()
    ten = input("Nhập tên đồ dùng: ")
    thoi_gian_mua = input("Nhập thiwf gian mua (dd/mm/yyyy): ")
    gia_mua = input("Nhập giá mua: ")
    thoi_gian_bao_hanh = input("Nhập thời gian bảo hành (tháng): ")
    danh_sach_beta[ten] = {
        "thoi_gian_mua": thoi_gian_mua,
        "gia_mua": gia_mua,
        "thoi_gian_bao_hanh": thoi_gian_bao_hanh
        
    }
    ghi_file_trai_nghiem()
    print("Đã thêm đồ dùng vào danh sách thành công")
    return True

def xoa_do_dung():
    xem_do_dung()
    try:
        vi_tri = int(input("Nhập số thứ tự đồ dùng muốn xóa: "))
        if 1 <= vi_tri <= len(danh_sach_beta):
            xoa = danh_sach_beta.pop(vi_tri - 1)
            ghi_file_trai_nghiem()
            print(f"Đã xóa đồ dùng: {xoa['ten']}")
        else:
            print("Vị trí không hợp lệ.")
    except:
        print("Dữ liệu không hợp lệ.")

def login():
    while True:
        print("\n=== Quản lí đồ dùng gia đình ===")
        lua_chon = input(
            """Vui lòng đăng nhập trước khi vào chương trình:
        1. Đăng nhập
        2. Đăng kí
        3. Đổi mật khẩu
        4. Xóa tài khoản
        5. Dùng trước bản thử nghiệm
        0. Thoát
        => """
        )
        if lua_chon == "1":
            dang_nhap()
            return True
        elif lua_chon == "2":
            dang_ky()
        elif lua_chon == "3":
            doi_mat_khau()
        elif lua_chon == "4":
            xoa_tai_khoan()
        elif lua_chon == "5":
            beta()
        elif lua_chon == "0":
            print("Đã thoát chương trình == Quản lí đồ dùng gia đình ==")
            break
        else:
            print("Lựa chọn không hợp lệ!")

def beta():
    doc_file_trai_nghiem()
    print ("Chào mừng bạn đến với chương trình === Quản Lí Đồ Dùng Gia Đình ===")
    while True:
        print("\n=== Quản lí đồ dùng gia đình ===")
        print("1. Xem đồ dùng")
        print("2. Thêm đồ dùng")
        print("3. Xóa đồ dùng")
        print("0. Thoát bản thử nghiệm")
        chon = input("Chọn chức năng: ")
        if chon == "1":
            xem_do_dung()
        elif chon == "2":
            them_do_dung()
        elif chon == "3":
            xoa_do_dung()
        elif chon == "0":
            print("Thoát bản thử nghiệm")
            break
        else:
            print("Vui lòng chọn lại.")
            
def premium():
    while True:
        lua_chon = input("nhap so: ")
        if lua_chon == "1":
            print("Chào mừng bạn đến với chương trình === Quản Lí Đồ Dùng")
if __name__ == "__main__":
    open_file_account()
    while True:  
        if login():
            premium()
        else:
            break