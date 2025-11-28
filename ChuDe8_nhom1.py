import heapq
import json
import os
from dataclasses import dataclass
from typing import List, Tuple

duong_dan_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dulieuLMS.json")

@dataclass
class DoVat:
    ID: int
    trong_luong: int
    gia_tri: int
    don_gia: float

@dataclass(order=True)
class Nut:
    uu_tien: float
    cap_do: int
    tong_trong_luong: int
    tong_gia_tri: int
    chon: Tuple[int, ...]
    duong_di: List[str]

def tinh_can_tren(nut: Nut, so_luong: int, trong_luong_toi_da: int, do_vat_da_sap_xep: List[DoVat]) -> Tuple[float, str]:
    if nut.tong_trong_luong > trong_luong_toi_da:
        return nut.tong_gia_tri, f"{nut.tong_gia_tri} (Vượt trọng lượng)"
    
    trong_luong_con_lai = trong_luong_toi_da - nut.tong_trong_luong
    cap_do_tiep_theo = nut.cap_do + 1
    
    # Nút gốc (chưa chọn đồ vật nào)
    if nut.cap_do == 0 and nut.tong_gia_tri == 0:
        don_gia_cao_nhat = do_vat_da_sap_xep[0].don_gia
        can_tren = trong_luong_toi_da * don_gia_cao_nhat
        cong_thuc = f"{trong_luong_toi_da} x {don_gia_cao_nhat:.2f} = {can_tren:.2f}"
        return can_tren, cong_thuc
    
    # Các nhánh khác: Cận trên = Trọng lượng còn lại × Đơn giá đồ vật tiếp theo + Giá trị hiện tại
    if cap_do_tiep_theo <= so_luong:
        do_vat_tiep_theo = do_vat_da_sap_xep[cap_do_tiep_theo - 1]
        don_gia_tiep_theo = do_vat_tiep_theo.don_gia
        can_tren = trong_luong_con_lai * don_gia_tiep_theo + nut.tong_gia_tri
        
        if nut.tong_gia_tri > 0:
            cong_thuc = f"{trong_luong_con_lai} x {don_gia_tiep_theo:.2f} + {nut.tong_gia_tri} = {can_tren:.2f}"
        else:
            cong_thuc = f"{trong_luong_con_lai} x {don_gia_tiep_theo:.2f} = {can_tren:.2f}"
    else:
        # Đã xét hết tất cả đồ vật
        can_tren = nut.tong_gia_tri
        cong_thuc = f"{nut.tong_gia_tri} (Đã xét hết đồ vật)"
    
    return can_tren, cong_thuc

def nhanh_can_balo(do_vat: List[DoVat], trong_luong_toi_da: int):
    do_vat_da_sap_xep = sorted(do_vat, key=lambda x: x.don_gia, reverse=True)
    so_luong = len(do_vat_da_sap_xep)

    nut_goc = Nut(uu_tien=0.0, cap_do=0, tong_trong_luong=0, tong_gia_tri=0, chon=tuple(), duong_di=["1"])
    hang_doi = []
    can_tren_goc, _ = tinh_can_tren(nut_goc, so_luong, trong_luong_toi_da, do_vat_da_sap_xep)
    nut_goc.uu_tien = -can_tren_goc
    heapq.heappush(hang_doi, nut_goc)

    gia_tri_tot_nhat = 0
    so_do_vat_tot_nhat = 0
    lua_chon_tot_nhat = tuple()
    duong_di_tot_nhat = ["1"]
    
    # Lưu trữ tất cả các nhánh
    danh_sach_nhanh = []
    

    while hang_doi:
        nut = heapq.heappop(hang_doi)
        can_tren = -nut.uu_tien
        if can_tren <= gia_tri_tot_nhat:
            continue

        if nut.cap_do >= so_luong:
            continue

        cap_do_tiep_theo = nut.cap_do + 1
        do_vat_hien_tai = do_vat_da_sap_xep[cap_do_tiep_theo - 1]

        # Nhánh 1: Chọn đồ vật
        trong_luong_chon_do_vat = nut.tong_trong_luong + do_vat_hien_tai.trong_luong
        gia_tri_do_vat_duoc_chon = nut.tong_gia_tri + do_vat_hien_tai.gia_tri
        chon_do_vat = nut.chon + (1,)
        duong_di_voi = nut.duong_di + [nut.duong_di[-1] + ".1"]
        
        nut_voi = Nut(uu_tien=0.0, cap_do=cap_do_tiep_theo, tong_trong_luong=trong_luong_chon_do_vat,
                     tong_gia_tri=gia_tri_do_vat_duoc_chon, chon=chon_do_vat, duong_di=duong_di_voi)
        can_tren_nhanh_chon, cong_thuc_voi = tinh_can_tren(nut_voi, so_luong, trong_luong_toi_da, do_vat_da_sap_xep)
        nut_voi.uu_tien = -can_tren_nhanh_chon

        # Nhánh 2: Không chọn đồ vật
        chon_khong = nut.chon + (0,)
        duong_di_khong = nut.duong_di + [nut.duong_di[-1] + ".0"]
        
        nut_khong = Nut(uu_tien=0.0, cap_do=cap_do_tiep_theo, tong_trong_luong=nut.tong_trong_luong,
                       tong_gia_tri=nut.tong_gia_tri, chon=chon_khong, duong_di=duong_di_khong)
        can_tren_nhanh_khong_chon, cong_thuc_khong = tinh_can_tren(nut_khong, so_luong, trong_luong_toi_da, do_vat_da_sap_xep)
        nut_khong.uu_tien = -can_tren_nhanh_khong_chon

        # Xử lý nhánh 1 (Chọn)
        if trong_luong_chon_do_vat <= trong_luong_toi_da:
            so_do_vat_voi = sum(chon_do_vat)
            
            # Xác định trạng thái
            if gia_tri_do_vat_duoc_chon >= gia_tri_tot_nhat and can_tren_nhanh_chon <= gia_tri_do_vat_duoc_chon:
                trang_thai_voi = 'Lời giải tối ưu'
                so_sanh_voi = ''
            elif can_tren_nhanh_chon <= gia_tri_tot_nhat:
                trang_thai_voi = 'Cắt tỉa'
                so_sanh_voi = f'Cận trên <= giá trị tối ưu hiện tại ({gia_tri_tot_nhat})'
            else:
                trang_thai_voi = 'Hợp lệ'
                # So sánh với nhánh không chọn
                if abs(can_tren_nhanh_chon - can_tren_nhanh_khong_chon) < 1e-9:
                    so_sanh_voi = f'Cận trên BẰNG nhánh không chọn ({can_tren_nhanh_khong_chon:.2f})'
                elif can_tren_nhanh_chon > can_tren_nhanh_khong_chon:
                    so_sanh_voi = f'Cận trên CAO hơn nhánh không chọn ({can_tren_nhanh_khong_chon:.2f})'
                else:
                    so_sanh_voi = f'Cận trên THẤP hơn nhánh không chọn ({can_tren_nhanh_khong_chon:.2f})'
            
            danh_sach_nhanh.append({
                'loai': 'Chọn',
                'do_vat': do_vat_hien_tai.ID,
                'duong_di': duong_di_voi[-1],
                'tong_gia_tri': gia_tri_do_vat_duoc_chon,
                'tong_trong_luong': trong_luong_chon_do_vat,
                'can_tren': can_tren_nhanh_chon,
                'cong_thuc_can_tren': cong_thuc_voi,
                'trang_thai': trang_thai_voi,
                'so_sanh': so_sanh_voi
            })
            
            if gia_tri_do_vat_duoc_chon > gia_tri_tot_nhat or (gia_tri_do_vat_duoc_chon == gia_tri_tot_nhat and so_do_vat_voi > so_do_vat_tot_nhat):
                gia_tri_tot_nhat = gia_tri_do_vat_duoc_chon
                so_do_vat_tot_nhat = so_do_vat_voi
                lua_chon_tot_nhat = chon_do_vat + tuple(0 for _ in range(so_luong - len(chon_do_vat)))
                duong_di_tot_nhat = duong_di_voi
            
            # Đưa vào hàng đợi nếu hợp lệ
            if trang_thai_voi not in ['Cắt tỉa', 'Lời giải tối ưu']:
                if can_tren_nhanh_chon > gia_tri_tot_nhat:
                    heapq.heappush(hang_doi, nut_voi)
        else:
            so_sanh_voi = 'Vượt trọng lượng'
            
            danh_sach_nhanh.append({
                'loai': 'Chọn',
                'do_vat': do_vat_hien_tai.ID,
                'duong_di': duong_di_voi[-1],
                'tong_gia_tri': gia_tri_do_vat_duoc_chon,
                'tong_trong_luong': trong_luong_chon_do_vat,
                'can_tren': can_tren_nhanh_chon,
                'cong_thuc_can_tren': cong_thuc_voi,
                'trang_thai': 'Vượt trọng lượng',
                'so_sanh': so_sanh_voi
            })
        
        # Xử lý nhánh 2 (Không chọn)
        # Xác định trạng thái
        if can_tren_nhanh_khong_chon <= gia_tri_tot_nhat:
            trang_thai_khong = 'Cắt tỉa'
            so_sanh_khong = f'Cận trên <= giá trị tối ưu hiện tại ({gia_tri_tot_nhat})'
        else:
            trang_thai_khong = 'Hợp lệ'
            # So sánh với nhánh chọn
            if abs(can_tren_nhanh_chon - can_tren_nhanh_khong_chon) < 1e-9:
                so_sanh_khong = f'Cận trên BẰNG nhánh chọn ({can_tren_nhanh_chon:.2f})'
            elif can_tren_nhanh_khong_chon > can_tren_nhanh_chon:
                so_sanh_khong = f'Cận trên CAO hơn nhánh chọn ({can_tren_nhanh_chon:.2f})'
            else:
                so_sanh_khong = f'Cận trên THẤP hơn nhánh chọn ({can_tren_nhanh_chon:.2f})'
            
        danh_sach_nhanh.append({
            'loai': 'Không chọn',
            'do_vat': do_vat_hien_tai.ID,
            'duong_di': duong_di_khong[-1],
            'tong_gia_tri': nut.tong_gia_tri,
            'tong_trong_luong': nut.tong_trong_luong,
            'can_tren': can_tren_nhanh_khong_chon,
            'cong_thuc_can_tren': cong_thuc_khong,
            'trang_thai': trang_thai_khong,
            'so_sanh': so_sanh_khong
        })
        
        # Đưa vào hàng đợi nếu hợp lệ
        if trang_thai_khong not in ['Cắt tỉa']:
            if can_tren_nhanh_khong_chon > gia_tri_tot_nhat:
                heapq.heappush(hang_doi, nut_khong)


    if not lua_chon_tot_nhat:
        return [], 0, 0, ["1"], danh_sach_nhanh

    danh_sach_ID = []
    tong_trong_luong = 0
    tong_gia_tri = 0
    for da_chon, do_vat_hien_tai in zip(lua_chon_tot_nhat, do_vat_da_sap_xep):
        if da_chon == 1:
            danh_sach_ID.append(do_vat_hien_tai.ID)
            tong_trong_luong += do_vat_hien_tai.trong_luong
            tong_gia_tri += do_vat_hien_tai.gia_tri

    danh_sach_ID.sort()
    return danh_sach_ID, tong_gia_tri, tong_trong_luong, duong_di_tot_nhat, danh_sach_nhanh

if __name__ == "__main__":
    try:
        with open(duong_dan_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"Error: File '{duong_dan_file}' is empty")
                exit(1)
            du_lieu = json.loads(content)
    except FileNotFoundError:
        print(f"Error: File '{duong_dan_file}' not found")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{duong_dan_file}': {e}")
        exit(1)
    
    danh_sach = []
    for item in du_lieu['danh_sach_do_vat']:
        trong_luong = item['trong_luong']
        gia_tri = item['gia_tri']
        don_gia = gia_tri / trong_luong
        danh_sach.append(DoVat(item['id'], trong_luong, gia_tri, don_gia))
    
    trong_luong_toi_da = 120
    
    # Sắp xếp đồ vật theo đơn giá giảm dần (giống như trong thuật toán)
    do_vat_da_sap_xep = sorted(danh_sach, key=lambda x: x.don_gia, reverse=True)
    
    chon, tong_gia_tri, tong_trong_luong, duong_di, danh_sach_nhanh = nhanh_can_balo(danh_sach, trong_luong_toi_da)
    
    # Tạo dictionary để tra cứu trọng lượng đồ vật
    do_vat_dict = {dv.ID: dv.trong_luong for dv in danh_sach}
    
    # Tính cận trên của nút gốc
    can_tren_goc = sum(dv.gia_tri for dv in do_vat_da_sap_xep)
    trong_luong_tat_ca = sum(dv.trong_luong for dv in do_vat_da_sap_xep)
    
    # Tính cận trên thực tế bằng phương pháp tham lam
    can_tren_thuc = 0
    trong_luong_tam = 0
    for dv in do_vat_da_sap_xep:
        if trong_luong_tam + dv.trong_luong <= trong_luong_toi_da:
            trong_luong_tam += dv.trong_luong
            can_tren_thuc += dv.gia_tri
        else:
            con_lai = trong_luong_toi_da - trong_luong_tam
            can_tren_thuc += dv.don_gia * con_lai
            break
    
    # Xuất kết quả ra file
    file_ket_qua = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ketquaLMS.txt")
    
    with open(file_ket_qua, 'w', encoding='utf-8') as f:
        # Hiển thị danh sách đồ vật sau khi sắp xếp
        f.write("=" * 60 + "\n")
        f.write("=== DANH SÁCH ĐỒ VẬT SAU KHI SẮP XẾP THEO ĐƠN GIÁ ===\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'ID':<8} {'Trọng lượng':<12} {'Giá trị':<10} {'Đơn giá':<10}\n")
        f.write("-" * 60 + "\n")
        for i, dv in enumerate(do_vat_da_sap_xep, 1):
            f.write(f"{dv.ID:<8} {dv.trong_luong:<12} {dv.gia_tri:<10} {dv.don_gia:<10.2f}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Trọng lượng tối đa của balo: {trong_luong_toi_da}\n")
        f.write(f"Tổng số đồ vật: {len(do_vat_da_sap_xep)}\n")
        
        # Hiển thị nút gốc
        f.write("\n" + "=" * 60 + "\n")
        f.write("=== NÚT GỐC (BẮT ĐẦU) ===\n")
        f.write("=" * 60 + "\n")
        f.write(f"Đường đi: 1\n")
        f.write(f"Giá trị hiện tại: 0\n")
        f.write(f"Trọng lượng đồ vật được chọn: 0\n")
        f.write(f"Trọng lượng còn lại: {trong_luong_toi_da}\n")
        f.write(f"Cận trên: {can_tren_thuc:.2f}\n")
        f.write(f"Trạng thái: Bắt đầu chọn đồ vật\n")
        
        # Hiển thị chi tiết các nhánh
        f.write("\n" + "=" * 60 + "\n")
        f.write("=== CHI TIẾT CÁC NHÁNH ===\n")
        f.write("=" * 60 + "\n")
        
        for i, nhanh in enumerate(danh_sach_nhanh, 1):
            trong_luong_do_vat = do_vat_dict[nhanh['do_vat']]
            trong_luong_con_lai = trong_luong_toi_da - nhanh['tong_trong_luong']
            
            f.write(f"\nNhánh {i}:\n")
            f.write(f"  Loại: {nhanh['loai']} đồ vật {nhanh['do_vat']}\n")
            f.write(f"  Đường đi: {nhanh['duong_di']}\n")
            f.write(f"  Giá trị hiện tại: {nhanh['tong_gia_tri']}\n")
            f.write(f"  Trọng lượng đồ vật được chọn: {nhanh['tong_trong_luong']}\n")
            f.write(f"  Trọng lượng còn lại: {trong_luong_con_lai}\n")
            
            if nhanh['loai'] == 'Chọn':
                trong_luong_truoc = nhanh['tong_trong_luong'] - trong_luong_do_vat
                f.write(f"  Tính trọng lượng: {trong_luong_truoc} + {trong_luong_do_vat} = {nhanh['tong_trong_luong']}\n")
            
            f.write(f"  Trọng lượng còn lại trong balo: {trong_luong_con_lai}\n")
            # f.write(f"  Cận trên: {nhanh['can_tren']:.2f}\n")
            f.write(f"  Cận trên: {nhanh['cong_thuc_can_tren']}\n")  # Thêm dòng này
            f.write(f"  Trạng thái: {nhanh['trang_thai']}\n")
            
            # Hiển thị so sánh với nhánh còn lại
            if 'so_sanh' in nhanh and nhanh['so_sanh']:
                f.write(f"  So sánh: {nhanh['so_sanh']}\n")
        
        # Hiển thị kết quả tối ưu
        f.write("\n" + "=" * 60 + "\n")
        f.write("=== KẾT QUẢ TỐI ƯU ===\n")
        f.write("=" * 60 + "\n")
        
        # Tìm nhánh tối ưu trong danh sách nhánh
        nhanh_toi_uu = None
        so_nhanh_toi_uu = None
        for i, nhanh in enumerate(danh_sach_nhanh, 1):
            if (nhanh['tong_gia_tri'] == tong_gia_tri and 
                nhanh['trang_thai'] == 'Lời giải tối ưu'):
                nhanh_toi_uu = nhanh
                so_nhanh_toi_uu = i
                break
        
        if so_nhanh_toi_uu:
            f.write(f"Nhánh tối ưu: Nhánh {so_nhanh_toi_uu}\n")
        
        f.write(f"Đồ vật được chọn (mã số): {chon}\n")
        f.write(f"Số lượng đồ vật: {len(chon)}\n")
        f.write(f"Tổng giá trị: {tong_gia_tri}\n")
        f.write(f"Tổng trọng lượng: {tong_trong_luong}\n")
        f.write(f"Trọng lượng còn lại: {trong_luong_toi_da - tong_trong_luong}\n")
        f.write(f"Đường đi: {' -> '.join(duong_di)}\n")
    
    print(f"Kết quả chi tiết các nhánh đi đã được xuất ra file: {file_ket_qua}")
    
    print("\n" + "=" * 60)
    print("=== KẾT QUẢ TỐI ƯU ===")
    print("=" * 60)
    
    if so_nhanh_toi_uu:
        print(f"Nhánh tối ưu: Nhánh {so_nhanh_toi_uu}")
    
    print("Đồ vật được chọn (ID):", chon)
    print("Số lượng đồ vật:", len(chon))
    print("Tổng giá trị:", tong_gia_tri)
    print("Tổng trọng lượng:", tong_trong_luong)
    print("Trọng lượng còn lại:", trong_luong_toi_da - tong_trong_luong)
    print("Đường đi:", " -> ".join(duong_di))