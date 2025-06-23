import json

tai_khoan_nguoi_dung = {}
danh_sach_do_dung_ban_thu_nghiem = {}
danh_sach_do_dung_ban_nang_cao = {}

#Bản thử nghiệm
def them_do_dung_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    so_luong_do_dung = int(input("Nhập số lượng đồ dùng muốn thêm: "))
    for i in range(so_luong_do_dung):
        ten_do_dung = input("Nhập tên đồ dùng: ")
        thoi_gian_mua = input("Nhập thời gian mua đồ dùng (dd/mm/yyyy): ")
        if len(thoi_gian_mua) != 10:
            while len(thoi_gian_mua) != 10:
                print("Nhập sai định dạng thời gian mua. Vui lòng nhập lại theo định dạng dd/mm/yyyy.")
                thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
        if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[0] + thoi_gian_mua[1]) > 31 or int(thoi_gian_mua[0] + thoi_gian_mua[1]) < 1:
            while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[0] + thoi_gian_mua[1])) > 31 or int(thoi_gian_mua[0] + thoi_gian_mua[1] < 1):
                print("Ngày không hợp lệ. Vui lòng nhập lại.")
                thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
        if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[3] + thoi_gian_mua[4]) > 12 or int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
            while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[3] + thoi_gian_mua[4])) > 12 or int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
                print("Tháng không hợp lệ. Vui lòng nhập lại.")
                thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
        thoi_gian_bao_hanh = input("Nhập thời gian bảo hành (tháng): ")
        gia_mua = float(input("Nhập giá mua đồ dùng: "))
        do_dung = {
            "thoi_gian_mua": thoi_gian_mua,
            "thoi_gian_bao_hanh": thoi_gian_bao_hanh,
            "gia_mua": gia_mua
        }
        danh_sach_do_dung_ban_thu_nghiem[ten_do_dung] = do_dung
    luu_danh_sach_do_dung_ban_thu_nghiem_vao_file()

def hien_thi_danh_sach_do_dung_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    if danh_sach_do_dung_ban_thu_nghiem == {}:
        print("Danh sách đồ dùng hiện tại rỗng.")
    else:
        print(f"{"=" * 66}")
        print(f"|{" " * 4}Tên đồ dùng{" " * 5}| Giá mua{" " * 2}|Thời gian mua|Thời gian bảo hành|")
        for ten_do_dung, thong_tin in danh_sach_do_dung_ban_thu_nghiem.items():
            print(f"|{" " * (20 - len(ten_do_dung))}{ten_do_dung}|{" " * (10 - len(str(f'{thong_tin["gia_mua"]:.3f}')))}{thong_tin["gia_mua"]:.3f}|{" " * 3}{thong_tin["thoi_gian_mua"]}|{" " * (18 - len(thong_tin["thoi_gian_bao_hanh"]))}{thong_tin["thoi_gian_bao_hanh"]}|")
        print(f"{"=" * 66}")
        doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()

def tim_kiem_do_dung_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    ten_do_dung = input("Nhập tên đồ dùng cần tìm kiếm: ")
    if ten_do_dung in danh_sach_do_dung_ban_thu_nghiem:
        thong_tin = danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]
        print(f"{"=" * 66}")
        print(f"|{" "*4}Tên đồ dùng{" "*5}| Giá mua{" "*2}|Thời gian mua|Thời gian bảo hành|")
        print(f"|{" "*(20 - len(ten_do_dung))}{ten_do_dung}|{" "*(10 - len(str(f'{thong_tin["gia_mua"]:.3f}')))}{thong_tin["gia_mua"]:.3f}|{" "*3}{thong_tin["thoi_gian_mua"]}|{" "*(18 - len(thong_tin["thoi_gian_bao_hanh"]))}{thong_tin["thoi_gian_bao_hanh"]}|")
        print(f"{"=" * 66}")
    else:
        print("Không tìm thấy đồ dùng với tên đã nhập.")

def sap_xep_do_dung_ban_thu_nghiem():
    global danh_sach_do_dung_ban_thu_nghiem
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    danh_sach_tam = list(danh_sach_do_dung_ban_thu_nghiem.keys())
    thong_tin_tam = list(danh_sach_do_dung_ban_thu_nghiem.values())
    for i in range(len(danh_sach_tam) - 1):
        for j in range(len(danh_sach_tam) - i - 1):
            if danh_sach_tam[j] > danh_sach_tam[j + 1]:
                danh_sach_tam[j], danh_sach_tam[j + 1] = danh_sach_tam[j + 1], danh_sach_tam[j]
                thong_tin_tam[j], thong_tin_tam[j + 1] = thong_tin_tam[j + 1], thong_tin_tam[j]
    danh_sach_do_dung_ban_thu_nghiem = {}
    for i in range(len(danh_sach_tam)):
        danh_sach_do_dung_ban_thu_nghiem[danh_sach_tam[i]] = thong_tin_tam[i]
    luu_danh_sach_do_dung_ban_thu_nghiem_vao_file()
    hien_thi_danh_sach_do_dung_ban_thu_nghiem()

def xoa_do_dung_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    ten_do_dung = input("Nhập tên đồ dùng muốn xóa: ")
    if ten_do_dung in danh_sach_do_dung_ban_thu_nghiem:
        del danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]
        luu_danh_sach_do_dung_ban_thu_nghiem_vao_file()
        print(f"Đã xóa đồ dùng {ten_do_dung} thành công")
    else:
        print(f"Không tìm thấy đồ dùng {ten_do_dung} để xóa")
        
def cap_nhat_do_dung_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    ten_do_dung = input("Nhập tên đồ dùng cần sửa: ")
    if ten_do_dung in danh_sach_do_dung_ban_thu_nghiem:
        print("Nhập thông tin mới, nếu không nhập thông tin nào thì sẽ giữ nguyên thông tin cũ")
        thoi_gian_mua = input(f"Thời gian mua hiện tại [{danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['thoi_gian_mua']}]: ")
        thoi_gian_bao_hanh_cu = danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['thoi_gian_bao_hanh']
        thoi_gian_bao_hanh = input(f"Thời gian bảo hành hiện tại [{thoi_gian_bao_hanh_cu}]: ")
        gia_mua_cu = danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['gia_mua']
        gia_mua = input(f"Giá mua hiện tại [{gia_mua_cu}]: ")
        if thoi_gian_mua != "":
            danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['thoi_gian_mua'] = thoi_gian_mua
        if thoi_gian_bao_hanh != "":
            danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['thoi_gian_bao_hanh'] = thoi_gian_bao_hanh     
        if gia_mua != "":
            try:
                gia_mua = float(gia_mua)
                danh_sach_do_dung_ban_thu_nghiem[ten_do_dung]['gia_mua'] = gia_mua
            except:
                print("Giá mua không hợp lệ, giữ nguyên giá cũ.")
        luu_danh_sach_do_dung_ban_thu_nghiem_vao_file()
        print(f"Cập nhật thông tin đồ dùng {ten_do_dung} thành công")
    else:
        print(f"Không tìm thấy đồ dùng {ten_do_dung} để sửa")

def thong_ke_tong_tien_ban_thu_nghiem():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    tong_tien = 0
    for key in danh_sach_do_dung_ban_thu_nghiem:
        tong_tien += danh_sach_do_dung_ban_thu_nghiem[key]['gia_mua']
    print(f"Tổng tiền mua tất cả đồ dùng: {tong_tien:.3f} VNĐ")

def xoa_toan_bo_du_lieu_trong_file():
    doc_danh_sach_do_dung_ban_thu_nghiem_tu_file()
    danh_sach_do_dung_ban_thu_nghiem.clear()
    luu_danh_sach_do_dung_ban_thu_nghiem_vao_file()
    print("Đã xóa toàn bộ dữ liệu trong file")

def luu_danh_sach_do_dung_ban_thu_nghiem_vao_file():
    try:
        with open('D:\\Python\\Du_an\\danh_sach_do_dung_thu_nghiem.json', 'w', encoding = "utf-8") as f:
            json.dump(danh_sach_do_dung_ban_thu_nghiem, f, ensure_ascii = False, indent = 4)
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn")

def doc_danh_sach_do_dung_ban_thu_nghiem_tu_file():
    try:
        with open('D:\\Python\\Du_an\\danh_sach_do_dung_thu_nghiem.json', 'r', encoding = "utf-8") as f:
            global danh_sach_do_dung_ban_thu_nghiem
            danh_sach_do_dung_ban_thu_nghiem = json.load(f)
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn")

def ban_thu_nghiem():
    while True:
        print(f"{"=" * 40}")
        print("Chương trình quản lí đồ dùng gia đình (Bản thử nghiệm)")
        print("1. Thêm đồ dùng vào file")
        print("2. Hiển thị danh sách đồ dùng trong file")
        print("3. Tìm kiếm đồ dùng trong file")
        print("4. Sắp xếp đồ dùng trong file")
        print("5. Xóa đồ dùng trong file")
        print("6. Cập nhật thông tin đồ dùng trong file")
        print("7. Thống kê tổng số tiền đã mua đồ dùng")
        print("8. Xóa toàn bộ dữ liệu trong file")
        print("0. Kết thúc chương trình")
        print("99. Thoát về menu chính")
        print(f"{"=" * 40}")
        lua_chon = int(input("Nhập lựa chọn của bạn: "))
        if lua_chon == 0:
            print("Kết thúc chương trình")
            print(f"{"=" * 40}")
            exit()
        elif lua_chon == 1:
            them_do_dung_ban_thu_nghiem()
        elif lua_chon == 2:
            hien_thi_danh_sach_do_dung_ban_thu_nghiem()
        elif lua_chon == 3:
            tim_kiem_do_dung_ban_thu_nghiem()
        elif lua_chon == 4:
            sap_xep_do_dung_ban_thu_nghiem()
        elif lua_chon == 5:
            xoa_do_dung_ban_thu_nghiem()
        elif lua_chon == 6:
            cap_nhat_do_dung_ban_thu_nghiem()
        elif lua_chon == 7:
            thong_ke_tong_tien_ban_thu_nghiem()
        elif lua_chon == 8:
            xoa_toan_bo_du_lieu_trong_file()
        elif lua_chon == 99:
            print("Thoát về menu chính")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            print()

# Hệ thống quản lý
def doc_file_du_lieu_nguoi_dung():
    global tai_khoan_nguoi_dung
    try:
        with open("D:\\Python\\Du_an\\du_lieu_nguoi_dung.json", 'r', encoding='utf-8') as f:
            tai_khoan_nguoi_dung = json.load(f)
    except:
        tai_khoan_nguoi_dung = {}

def luu_danh_sach_nguoi_dung_vao_file():
    with open("D:\\Python\\Du_an\\du_lieu_nguoi_dung.json", "w", encoding="utf-8") as f:
        json.dump(tai_khoan_nguoi_dung, f, indent=4)

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
    email = input("Nhập email: ")
    if email in tai_khoan_nguoi_dung:
        print("Đã có tài khoản sử dụng email này!")
        return False
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
    luu_danh_sach_nguoi_dung_vao_file()
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
            luu_danh_sach_nguoi_dung_vao_file()
            print("Đổi mật khẩu thành công!")
            return True
        print("Sai mật khẩu cũ!")
        return False
    print("Tài khoản không tồn tại!")
    return False

def xoa_tai_khoan():
    print("XÓA TÀI KHOẢN")
    ten_dang_nhap = input("Nhập tên đăng nhập: ")
    if ten_dang_nhap not in tai_khoan_nguoi_dung:
        print("Tài khoản không tồn tại!")
        return False
    mat_khau = input("Nhập mật khẩu: ")
    if tai_khoan_nguoi_dung[ten_dang_nhap]["password"] != mat_khau:
        print("Mật khẩu không đúng!")
        return False
    del tai_khoan_nguoi_dung[ten_dang_nhap]
    print(f"Tài khoản {ten_dang_nhap} đã được xóa thành công.")
    luu_danh_sach_nguoi_dung_vao_file()
    return True

#Bản nâng cao
def doc_danh_sach_do_dung_ban_nang_cao_tu_file():
    try:
        with open('D:\\Python\\Du_an\\danh_sach_do_dung_nang_cao.json', 'r', encoding = "utf-8") as f:
            global danh_sach_do_dung_ban_nang_cao
            danh_sach_do_dung_ban_nang_cao = json.load(f)
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn")
        danh_sach_do_dung_ban_nang_cao = {}

def luu_danh_sach_do_dung_ban_nang_cao_vao_file():
    try:
        with open('D:\\Python\\Du_an\\danh_sach_do_dung_nang_cao.json', 'w', encoding = "utf-8") as f:
            json.dump(danh_sach_do_dung_ban_nang_cao, f, ensure_ascii = False, indent = 4)
    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra đường dẫn")

def them_do_dung_ban_nang_cao():
    doc_danh_sach_do_dung_ban_nang_cao_tu_file()
    so_do_dung = int(input("Nhập số đồ dùng muốn thêm: "))
    for i in range(so_do_dung):
        print(f"Thêm đồ dùng thứ {i + 1}")
        ten_do_dung = input("Nhập tên đồ dùng: ")
        if ten_do_dung in danh_sach_do_dung_ban_nang_cao:
            print("=" * 40)
            print(f"Đồ dùng {ten_do_dung} đã tồn tại trong danh sách.")
            print("1. Tăng số lượng ")
            print(f"2. Ghi đè thông tin của {ten_do_dung}")
            print("3. Bỏ thêm đồ dùng này")
            lua_chon = int(input("Nhập lựa chọn của bạn: "))
            while lua_chon != 1 or lua_chon != 2 or lua_chon != 3:
                if lua_chon == 1:
                    so_luong_tang = int(input("Nhập số lượng đồ dùng muốn tăng: "))
                    danh_sach_do_dung_ban_nang_cao[ten_do_dung]["so_luong"] += so_luong_tang
                    print("=" * 40)
                    luu_danh_sach_do_dung_ban_nang_cao_vao_file()
                elif lua_chon == 2:
                    thoi_gian_mua = input("Nhập thời gian mua đồ dùng (dd/mm/yyyy): ")
                    if len(thoi_gian_mua) != 10:
                        while len(thoi_gian_mua) != 10:
                            print("Nhập sai định dạng thời gian mua. Vui lòng nhập lại theo định dạng dd/mm/yyyy.")
                            thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
                    if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[0] + thoi_gian_mua[1]) > 31 or int(thoi_gian_mua[0] + thoi_gian_mua[1]) < 1:
                        while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[0] + thoi_gian_mua[1])) > 31 and int(thoi_gian_mua[0] + thoi_gian_mua[1] < 1):
                            print("Ngày không hợp lệ. Vui lòng nhập lại.")
                            thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
                    if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[3] + thoi_gian_mua[4]) > 12 or int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
                        while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[3] + thoi_gian_mua[4])) > 12 and int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
                            print("Tháng không hợp lệ. Vui lòng nhập lại.")
                            thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
                    thoi_gian_bao_hanh = int(input("Nhập thời gian bảo hành (tháng): "))
                    gia_mua = float(input("Nhập giá mua đồ dùng (nghìn VND): "))
                    gia_ban = float(input("Nhập giá bán đồ dùng (nghìn VND): "))
                    so_luong = int(input("Nhập số lượng đồ dùng: "))
                    danh_sach_do_dung_ban_nang_cao[ten_do_dung] = {
                        "thoi_gian_mua": thoi_gian_mua,
                        "thoi_gian_bao_hanh": thoi_gian_bao_hanh,
                        "gia_mua": gia_mua,
                        "gia_ban": gia_ban,
                        "so_luong": so_luong
                    }
                    print("=" * 40)
                    luu_danh_sach_do_dung_ban_nang_cao_vao_file()
                elif lua_chon == 3:
                    print("Bỏ thêm đồ dùng này")
                    print("=" * 40)
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
                    print("=" * 40)
                    print(f"Đồ dùng {ten_do_dung} đã tồn tại trong danh sách.")
                    print("1. Tăng số lượng ")
                    print(f"2. Ghi đè thông tin của {ten_do_dung}")
                    print("3. Bỏ thêm đồ dùng này")
                    lua_chon = int(input("Nhập lựa chọn của bạn: "))
        else:
            thoi_gian_mua = input("Nhập thời gian mua đồ dùng (dd/mm/yyyy): ")
            if len(thoi_gian_mua) != 10:
                while len(thoi_gian_mua) != 10:
                    print("Nhập sai định dạng thời gian mua. Vui lòng nhập lại theo định dạng dd/mm/yyyy.")
                    thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
            if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[0] + thoi_gian_mua[1]) > 31 or int(thoi_gian_mua[0] + thoi_gian_mua[1]) < 1:
                while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[0] + thoi_gian_mua[1])) > 31 and int(thoi_gian_mua[0] + thoi_gian_mua[1] < 1):
                    print("Ngày không hợp lệ. Vui lòng nhập lại.")
                    thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
            if len(thoi_gian_mua) >= 10 and int(thoi_gian_mua[3] + thoi_gian_mua[4]) > 12 or int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
                while len(thoi_gian_mua) >= 10 and (int(thoi_gian_mua[3] + thoi_gian_mua[4])) > 12 and int(thoi_gian_mua[3] + thoi_gian_mua[4]) < 1:
                    print("Tháng không hợp lệ. Vui lòng nhập lại.")
                    thoi_gian_mua = input("Nhập lại thời gian mua đồ dùng (dd/mm/yyyy): ")
            thoi_gian_bao_hanh = int(input("Nhập thời gian bảo hành (tháng): "))
            gia_mua = float(input("Nhập giá mua đồ dùng (nghìn VND): "))
            gia_ban = float(input("Nhập giá bán đồ dùng (nghìn VND): "))
            so_luong = int(input("Nhập số lượng đồ dùng: "))

def tim_ghi_chu_dai_nhat_ban_nang_cao():
    doc_danh_sach_do_dung_ban_nang_cao_tu_file()
    bien_tam = ""
    for ten_do_dung, thong_tin in danh_sach_do_dung_ban_nang_cao.items():
        if "ghi_chu" in thong_tin:
            if len(thong_tin["ghi_chu"]) > len(bien_tam):
                bien_tam = thong_tin["ghi_chu"]       
    return len(bien_tam)

def hien_thi_danh_sach_do_dung_ban_nang_cao():
    doc_danh_sach_do_dung_ban_nang_cao_tu_file()
    if danh_sach_do_dung_ban_nang_cao == {}:
        print("Danh sách đồ dùng hiện tại rỗng.")
    else:
        khoang_cach = tim_ghi_chu_dai_nhat_ban_nang_cao()
        print("=" * (139 + khoang_cach))
        print(f"|STT|{" " * 19}Tên đồ dùng{" " * 20}|{" " * 1}Thời gian mua{" " * 2}|Thời gian bảo hành|{" " * 3}Giá mua{" " * 4}|{" " * 3}Giá bán{" " * 4}|Số lượng|Ghi chú{" " * khoang_cach}|")
        i = 1
        for ten_do_dung, thong_tin in danh_sach_do_dung_ban_nang_cao.items():
            print("=" * (139 + khoang_cach))
            if "ghi_chu" not in thong_tin:
                print(f"|{" " * (3 - len(str(i)))}{i}|{" " * (50 - len(ten_do_dung))}{ten_do_dung}|{" " * 6}{thong_tin["thoi_gian_mua"]}|{" " * (12 - len(str(thong_tin["thoi_gian_bao_hanh"])))}{thong_tin["thoi_gian_bao_hanh"]} tháng|{" " * (12 - len(str(thong_tin["gia_mua"])))}{thong_tin["gia_mua"]:.3f}|{" " * (12 - len(str(thong_tin["gia_ban"])))}{thong_tin["gia_ban"]:.3f}|{" " * (8 - len(str(thong_tin["so_luong"])))}{thong_tin["so_luong"]}|{" " * ( 7 + khoang_cach)}|")
            else:
                print(f"|{" " * (3 - len(str(i)))}{i}|{" " * (50 - len(ten_do_dung))}{ten_do_dung}|{" " * 6}{thong_tin["thoi_gian_mua"]}|{" " * (12 - len(str(thong_tin["thoi_gian_bao_hanh"])))}{thong_tin["thoi_gian_bao_hanh"]} tháng|{" " * (12 - len(str(thong_tin["gia_mua"])))}{thong_tin["gia_mua"]:.3f}|{" " * (12 - len(str(thong_tin["gia_ban"])))}{thong_tin["gia_ban"]:.3f}|{" " * (8 - len(str(thong_tin["so_luong"])))}{thong_tin["so_luong"]}|{thong_tin["ghi_chu"]}{" " * 7}|")
            i = i + 1
        print("=" * (139 + khoang_cach))

def tim_kiem_do_dung_ban_nang_cao(lua_chon):
    doc_danh_sach_do_dung_ban_nang_cao_tu_file()
    if lua_chon == 1:
        ten_do_dung = input("Nhập tên đồ dùng muốn tìm kiếm: ")
        khoang_cach = tim_ghi_chu_dai_nhat_ban_nang_cao()
        ket_qua = {}
        for ten, thong_tin in danh_sach_do_dung_ban_nang_cao.items():
            if ten_do_dung in ten:
                ket_qua[ten] = thong_tin
        if ket_qua == {}:
            print(f"Không tìm thấy đồ dùng {ten_do_dung} trong danh sách.")
        else:
            print("=" * (139 + khoang_cach))
            print(f"|STT|{" " * 19}Tên đồ dùng{" " * 20}|{" " * 1}Thời gian mua{" " * 2}|Thời gian bảo hành|{" " * 3}Giá mua{" " * 4}|{" " * 3}Giá bán{" " * 4}|Số lượng|Ghi chú{" " * khoang_cach}|")
            i = 1
            print("=" * (139 + khoang_cach))
            for ten, thong_tin in ket_qua.items():
                if "ghi_chu" not in thong_tin:
                    print(f"|{" " * (3 - len(str(i)))}{i}|{" " * (50 - len(ten_do_dung))}{ten_do_dung}|{" " * 6}{thong_tin["thoi_gian_mua"]}|{" " * (12 - len(str(thong_tin["thoi_gian_bao_hanh"])))}{thong_tin["thoi_gian_bao_hanh"]} tháng|{" " * (12 - len(str(thong_tin["gia_mua"])))}{thong_tin["gia_mua"]:.3f}|{" " * (12 - len(str(thong_tin["gia_ban"])))}{thong_tin["gia_ban"]:.3f}|{" " * (8 - len(str(thong_tin["so_luong"])))}{thong_tin["so_luong"]}|{" " * ( 7 + khoang_cach)}|")
                else:
                    print(f"|{" " * (3 - len(str(i)))}{i}|{" " * (50 - len(ten_do_dung))}{ten_do_dung}|{" " * 6}{thong_tin["thoi_gian_mua"]}|{" " * (12 - len(str(thong_tin["thoi_gian_bao_hanh"])))}{thong_tin["thoi_gian_bao_hanh"]} tháng|{" " * (12 - len(str(thong_tin["gia_mua"])))}{thong_tin["gia_mua"]:.3f}|{" " * (12 - len(str(thong_tin["gia_ban"])))}{thong_tin["gia_ban"]:.3f}|{" " * (8 - len(str(thong_tin["so_luong"])))}{thong_tin["so_luong"]}|{thong_tin["ghi_chu"]}{" " * 7}|")
                i = i + 1
            print("=" * (139 + khoang_cach))

def ban_nang_cao():
    while True:
        print("Chương trình quản lí đồ dùng gia đình (Bản nâng cao)")
        print("1. Thêm đồ dùng vào file")
        print("2. Hiển thị danh sách đồ dùng trong file")
        print("3. Tìm kiếm đồ dùng trong file")
        print("4. Sắp xếp đồ dùng trong file")
        print("5. Xóa đồ dùng trong file")
        print("6. Cập nhật thông tin đồ dùng trong file")
        print("7. Thống kê tổng chi phí mua đồ dùng")
        print("8. Thống kê bảo hành đồ dùng")
        print("9. Thêm ghi chú cho đồ dùng")
        print("10. Kiểm tra lịch sử thay đổi dữ liệu")
        print("11. Tạo hóa đơn bán đồ dùng")
        print("12. Thống kê lãi và lỗ")
        print("13. Thống kê lịch sử mua bán đồ dùng")
        print("14. Tính trung bình chi phí đồ dùng")
        print("15. Xóa toàn bộ dữ liệu trong file")
        print("0. Kết thúc chương trình")
        print("99. Thoát về menu chính")
        lua_chon = int(input("Nhập lựa chọn của bạn: "))
        if lua_chon == 0:
            print("Kết thúc chương trình")
            print(f"{"=" * 40}")
            exit()
        elif lua_chon == 1:
            them_do_dung_ban_nang_cao()
        elif lua_chon == 2:
            hien_thi_danh_sach_do_dung_ban_nang_cao()
        elif lua_chon == 3:
            print("1. Tìm kiếm theo tên đồ dùng.")
            print("2. Tìm kiếm theo khoảng giá bán.")
            print("3. TÌm kiếm theo khoảng giá mua.")
            lua_chon = int(input("Nhập vào lựa chọn của bạn: "))
            while lua_chon != 1 and lua_chon != 2 and lua_chon != 3:
                if lua_chon == 1:
                    tim_kiem_do_dung_ban_nang_cao(1)
                elif lua_chon == 2:
                    tim_kiem_do_dung_ban_nang_cao(2)
                elif lua_chon == 3:
                    tim_kiem_do_dung_ban_nang_cao(3)
                else:
                    print("Bạn đã chọn sai lựa chọn. Vui lòng chọn lại.")
        elif lua_chon == 99:
            print("Thoát về menu chính")
            break

# Hàm chính
if __name__ == "__main__":
    doc_file_du_lieu_nguoi_dung()
    print(f"{"=" * 40}")
    print("HỆ THỐNG CHƯƠNG TRÌNH QUẢN LÍ ĐỒ DÙNG GIA ĐÌNH")
    print("1. Đăng nhập để sử dụng bản nâng cao")
    print("2. Đăng kí")
    print("3. Đổi mật khẩu")
    print("4. Xóa tài khoản")
    print("5. Sử dụng bản thử nghiệm")
    print("0. Kết thúc chương trình")
    print(f"{"=" * 40}")
    lua_chon = int(input("Nhập lựa chọn của bạn: "))
    while lua_chon != 0:
        if lua_chon == 1:
            if dang_nhap():
                print(f"{"=" * 40}")
                ban_nang_cao()
        elif lua_chon == 2:
            dang_ky()
        elif lua_chon == 3:
            doi_mat_khau()
        elif lua_chon == 4:
            xoa_tai_khoan()
        elif lua_chon == 5:
            lua_chon = ban_thu_nghiem()
        elif  lua_chon == 0:
            print("Kết thúc chương trình")
            print("=*40")
            exit()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        print(f"{"="*40}")
        print("HỆ THỐNG CHƯƠNG TRÌNH QUẢN LÍ ĐỒ DÙNG GIA ĐÌNH")
        print("1. Đăng nhập để sử dụng bản nâng cao")
        print("2. Đăng kí")
        print("3. Sử dụng bản thử nghiệm")
        print("4. Đổi mật khẩu")
        print("5. Xóa tài khoản")
        print("0. Kết thúc chương trình")
        print(f"{"="*40}")
        lua_chon = int(input("Nhập lựa chọn của bạn: "))
