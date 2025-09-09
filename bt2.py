#Phương pháp Quine
from collections import defaultdict
from typing import List, Set, Tuple

# ===== Helpers =====
def to_bin(n: int, bits: int) -> str:
    return format(n, f"0{bits}b")

def ones_count(s: str) -> int:
    return s.count("1")

def diff_by_one_bit(a: str, b: str) -> Tuple[bool, int]:
    """Trả về (True, index) nếu a và b khác đúng 1 bit; ngược lại (False, -1)."""
    idx = -1
    diff = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            diff += 1
            idx = i
            if diff > 1:
                return False, -1
    return (diff == 1, idx if diff == 1 else -1)

def combine(a: str, b: str) -> str:
    """Ghép hai mã nhị phân khác đúng 1 bit thành mẫu với '-' ở vị trí khác."""
    return "".join(x if x == y else "-" for x, y in zip(a, b))

def covers(pattern: str, m: int) -> bool:
    """Kiểm tra pattern (chuỗi gồm 0/1/-) có phủ minterm m hay không."""
    bits = to_bin(m, len(pattern))
    return all(p == '-' or p == b for p, b in zip(pattern, bits))

def pattern_to_expr(pattern: str, var_names: List[str]) -> str:
    """Chuyển pattern (0/1/-) sang hạng đẳng thức dạng tích (AND) như A'B C ..."""
    terms = []
    for ch, v in zip(pattern, var_names):
        if ch == '-':
            continue
        terms.append(v if ch == '1' else f"{v}'")
    return "".join(terms) if terms else "1"  # '1' nếu là khẳng định luôn đúng

# ===== Quine–McCluskey core =====
def find_prime_implicants(minterms: List[int], num_vars: int) -> Tuple[List[str], dict]:
    """Trả về (danh sách prime implicants dạng pattern, mapping pattern->set(minterms_phủ))."""
    # Bước 1: Nhóm theo số lượng bit 1
    groups = defaultdict(list)
    for m in sorted(set(minterms)):
        b = to_bin(m, num_vars)
        groups[ones_count(b)].append((b, {m}))

    all_combinations = []
    used = set()
    prime_implicants = set()

    while True:
        next_groups = defaultdict(list)
        marked = set()
        keys = sorted(groups.keys())
        combined_any = False
        # Bước 2-3: Ghép các nhóm k và k+1 nếu khác đúng 1 bit
        for i in range(len(keys) - 1):
            g1 = groups[keys[i]]
            g2 = groups[keys[i + 1]]
            for (pat1, cov1) in g1:
                for (pat2, cov2) in g2:
                    # Bỏ qua nếu có '-' không trùng nhau quá 1 vị trí?
                    # Ở vòng đầu chưa có '-', nhưng các vòng sau vẫn xử lý theo diff_by_one_bit
                    # chỉ ghép được khi khác đúng 1 vị trí không phải '-'
                    # Ta thay '-' bằng chính nó để diff_by_one_bit vẫn hợp lệ:
                    if len(pat1) != len(pat2):
                        continue
                    # Chỉ cho phép khác đúng 1 bit (bỏ qua '-' coi như giống)
                    diff = 0
                    idx = -1
                    for k, (x, y) in enumerate(zip(pat1, pat2)):
                        if x != y:
                            if x == '-' or y == '-':
                                diff = 2
                                break
                            diff += 1
                            idx = k
                            if diff > 1:
                                break
                    if diff == 1:
                        combined = combine(pat1, pat2)
                        next_groups[ones_count(combined.replace('-', ''))].append((combined, cov1 | cov2))
                        marked.add((pat1, tuple(sorted(cov1))))
                        marked.add((pat2, tuple(sorted(cov2))))
                        combined_any = True

        # Đánh dấu các pattern không được ghép ở vòng này là prime implicants
        for g in groups.values():
            for (p, cov) in g:
                if (p, tuple(sorted(cov))) not in marked:
                    prime_implicants.add((p, frozenset(cov)))

        if not combined_any:
            break
        groups = defaultdict(list)
        # Khử trùng lặp trong next_groups
        seen = set()
        for lst in next_groups.values():
            for p, cov in lst:
                key = (p, tuple(sorted(cov)))
                if key not in seen:
                    groups[ones_count(p.replace('-', ''))].append((p, cov))
                    seen.add(key)

    # Gom kết quả
    pi_list = []
    cover_map = {}
    for p, cov in sorted(prime_implicants, key=lambda x: (x[0].count('-'), x[0])):
        pi_list.append(p)
        cover_map[p] = set(cov)
    return pi_list, cover_map

def prime_implicant_chart(prime_implicants: List[str], cover_map: dict, minterms: List[int]):
    """Tạo bảng phủ: hàng là PI, cột là minterm; giá trị 1 nếu PI phủ minterm."""
    chart = {p: set() for p in prime_implicants}
    for p in prime_implicants:
        for m in minterms:
            if covers(p, m):
                chart[p].add(m)
    return chart

def find_essential_pis(chart: dict, minterms: List[int]) -> Tuple[Set[str], Set[int]]:
    """Tìm các essential prime implicants và tập minterm đã được phủ bởi chúng."""
    essential = set()
    covered = set()
    # Với mỗi minterm, xem nó được bao phủ bởi bao nhiêu PI
    for m in minterms:
        owners = [p for p, cols in chart.items() if m in cols]
        if len(owners) == 1:
            essential.add(owners[0])
    # Đánh dấu đã phủ
    for p in essential:
        covered |= chart[p]
    return essential, covered

def greedy_cover(chart: dict, minterms: List[int], already: Set[int]) -> Set[str]:
    """Phủ các minterm còn lại bằng chiến lược tham lam (không phải Petrick tối ưu)."""
    remaining = set(minterms) - already
    chosen = set()
    pis = list(chart.keys())
    while remaining:
        # Chọn PI phủ được nhiều minterm còn lại nhất
        best_p, best_gain = None, -1
        for p in pis:
            gain = len(chart[p] & remaining)
            if gain > best_gain:
                best_gain = gain
                best_p = p
        if best_p is None or best_gain == 0:
            break  # bế tắc (không nên xảy ra nếu chart đúng)
        chosen.add(best_p)
        remaining -= chart[best_p]
    return chosen

def quine_mccluskey(minterms: List[int], num_vars: int, var_names: List[str] = None):
    if var_names is None:
        # Tạo tên biến A, B, C, ...
        var_names = [chr(ord('A') + i) for i in range(num_vars)]
    # 1) Tìm prime implicants
    pi_list, cover_map = find_prime_implicants(minterms, num_vars)
    # 2) Lập prime implicant chart
    chart = prime_implicant_chart(pi_list, cover_map, minterms)
    # 3) Tìm essential prime implicants
    essential, covered = find_essential_pis(chart, minterms)
    # 4) Nếu còn cột chưa phủ, dùng tham lam để hoàn tất
    extra = greedy_cover(chart, minterms, covered)
    selected = sorted(essential | extra)

    # Chuẩn bị kết quả biểu thức
    terms_expr = [pattern_to_expr(p, var_names) for p in selected]
    simplified_expr = " + ".join(terms_expr) if terms_expr else "0"

    # Trả về đầy đủ thông tin trung gian để quan sát
    return {
        "prime_implicants": pi_list,
        "chart": {p: sorted(list(cols)) for p, cols in chart.items()},
        "essential_prime_implicants": sorted(list(essential)),
        "additional_implicants": sorted(list(extra - essential)),
        "selected_implicants": selected,
        "simplified_expression": simplified_expr
    }

# ===== Demo usage =====
if __name__ == "__main__":
    # Ví dụ: f(A,B,C,D) = Σ m(0,1,2,5,6,7,8,9,10,14)
    minterms = [5,9,11,12,13,14,15]
    num_vars = 4
    result = quine_mccluskey(minterms, num_vars, var_names=["A","B","C","D"])

    print("Prime implicants:")
    for p in result["prime_implicants"]:
        print("  ", p)

    print("\nPrime implicant chart (PI -> minterms covered):")
    for p, cols in result["chart"].items():
        print(f"  {p}: {cols}")

    print("\nEssential prime implicants:")
    for p in result["essential_prime_implicants"]:
        print("  ", p)

    if result["additional_implicants"]:
        print("\nAdditional implicants (greedy to cover remaining):")
        for p in result["additional_implicants"]:
            print("  ", p)

    print("\nSelected implicants:")
    for p in result["selected_implicants"]:
        print("  ", p)

    print("\nSimplified Boolean expression:")
    print("  f =", result["simplified_expression"])

# Nhập từ bàn phím:
    # 1. num_vars số biến >= 2
    # 2. danh sách minterms SOP qua bàn phím, ví dụ: 0 1 2 5 6 7 8 9 10 14
try:
    so_bien = int(input("Nhập số biến (>=2): "))
    if so_bien < 2:
        raise ValueError("Số biến phải lớn hơn hoặc bằng 2.")
    dau_vao_minterm = input("Nhập các minterm (cách nhau bằng dấu cách): ")
    minterms = list(map(int, dau_vao_minterm.split()))
    if any(m < 0 or m >= 2**so_bien for m in minterms):
        raise ValueError(f"Các minterm phải nằm trong khoảng [0, {2**so_bien - 1}].")
        
    ket_qua = quine_mccluskey(minterms, so_bien)
        
    print("\nBiểu thức Boolean tối giản:")
    print("  f =", ket_qua["bieuthuc_toi_gian"])
except Exception as e:
    print("Lỗi:", e)

# Nhập từ bàn phím:
    # 1. num_vars thuộc {2,3,4}.
    # 2. mode thuộc {'SOP', 'POS'}.
    # 3. Nếu SOP: nhập danh sách minterms.; nếu POS: nhập danh sách maxterms.
try:
    num_vars = int(input("Nhập số biến (2, 3 hoặc 4): "))
    if num_vars not in {2, 3, 4}:
        raise ValueError("Số biến phải là 2, 3 hoặc 4.")
    
    mode = input("Chọn chế độ (SOP hoặc POS): ").strip().upper()
    if mode not in {'SOP', 'POS'}:
        raise ValueError("Chế độ phải là 'SOP' hoặc 'POS'.")
    
    terms_input = input(f"Nhập {'minterm' if mode == 'SOP' else 'maxterm'} (cách nhau bằng khoảng trắng): ")
    terms = list(map(int, terms_input.split()))
    
    if any(t < 0 or t >= 2**num_vars for t in terms):
        raise ValueError(f"Các giá trị phải nằm trong khoảng [0, {2**num_vars - 1}].")
    
    if mode == 'SOP':
        minterms = terms
    else:  # POS
        all_terms = set(range(2**num_vars))
        minterms = sorted(all_terms - set(terms))
    
    result = quine_mccluskey(minterms, num_vars)
    
    print("\nBiểu thức logic rút gọn:")
    print("  f =", result["simplified_expression"])
except Exception as e:
    print("Lỗi:", e)

# Nhập từ bàn phím:
    # 1. num_vars số biến
    # biểu thức Bollearn rút gọn dạng SOP chuẩn mini 
    # kí hiệu liền nhau là AND, OR là +, NOT là '
try:
    num_vars = int(input("Nhập số biến (>=2): "))
    if num_vars < 2:
        raise ValueError("Số biến phải lớn hơn hoặc bằng 2.")
    
    expr = input("Nhập biểu thức Boolean dạng SOP (ví dụ: A'B + AC): ").strip()
    if not expr:
        raise ValueError("Biểu thức không được để trống.")
    
    var_names = [chr(ord('A') + i) for i in range(num_vars)]
    
    # Chuyển biểu thức thành danh sách minterms
    def expr_to_minterms(expr: str, var_names: List[str]) -> List[int]:
        terms = expr.split('+')
        minterms = set()
        for term in terms:
            term = term.strip()
            if not term:
                continue
            bits = ['-'] * len(var_names)
            for ch in term:
                if ch in var_names:
                    idx = var_names.index(ch)
                    bits[idx] = '1'
                elif ch.endswith("'") and ch[:-1] in var_names:
                    idx = var_names.index(ch[:-1])
                    bits[idx] = '0'
                else:
                    raise ValueError(f"Ký hiệu không hợp lệ trong biểu thức: {ch}")
            # Chuyển bits sang số nguyên
            def generate_minterms(bits: List[str], pos: int = 0) -> List[int]:
                if pos == len(bits):
                    return [0]
                if bits[pos] == '-':
                    res0 = generate_minterms(bits, pos + 1)
                    res1 = generate_minterms(bits, pos + 1)
                    return [r << 1 for r in res0] + [(r << 1) | 1 for r in res1]
                elif bits[pos] == '0':
                    return [r << 1 for r in generate_minterms(bits, pos + 1)]
                else:  # '1'
                    return [(r << 1) | 1 for r in generate_minterms(bits, pos + 1)]
            minterms.update(generate_minterms(bits))
        return sorted(minterms)
    
    minterms = expr_to_minterms(expr, var_names)
    
    result = quine_mccluskey(minterms, num_vars, var_names)
    
    print("\nBiểu thức logic rút gọn:")
    print("  f =", result["simplified_expression"])
except Exception as e:
    print("Lỗi:", e)
