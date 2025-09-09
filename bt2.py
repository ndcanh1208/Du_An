def quine_mccluskey(minterms, num_vars, var_names=None):
   
    # chuẩn hoá & kiểm tra
    minterms = sorted(set(minterms))
    if var_names is None:
        var_names = [f"x{i}" for i in range(1, num_vars+1)]
    if len(var_names) != num_vars:
        raise ValueError("var_names length must equal num_vars")
    max_val = 2**num_vars - 1
    for m in minterms:
        if m < 0 or m > max_val:
            raise ValueError(f"minterm {m} out of range for {num_vars} variables")

    def int_to_bits(n):
        return format(n, f'0{num_vars}b')

    # bước 1: nhóm ban đầu theo số 1s
    groups = {}
    for m in minterms:
        bits = int_to_bits(m)
        ones = bits.count('1')
        groups.setdefault(ones, []).append({'bits': bits, 'minterms': {m}, 'combined': False})

    prime_implicants = []
    # vòng lặp kết hợp
    while True:
        next_round = {}
        combined_any = False
        keys = sorted(groups.keys())
        for k in keys:
            g1 = groups.get(k, [])
            g2 = groups.get(k+1, [])
            for a in g1:
                for b in g2:
                    diffs = [i for i,(x,y) in enumerate(zip(a['bits'], b['bits'])) if x != y]
                    if len(diffs) == 1:
                        combined_any = True
                        i = diffs[0]
                        new_bits = list(a['bits'])
                        new_bits[i] = '-'
                        new_bits = ''.join(new_bits)
                        new_minterms = a['minterms'] | b['minterms']
                        # lưu vào next_round (tránh trùng)
                        if new_bits not in next_round:
                            next_round[new_bits] = {'bits': new_bits, 'minterms': set(new_minterms), 'combined': False}
                        else:
                            next_round[new_bits]['minterms'] |= new_minterms
                        a['combined'] = True
                        b['combined'] = True
        # thu những term không bị combined => prime implicants
        for grp in groups.values():
            for term in grp:
                if not term.get('combined', False):
                    # tránh trùng
                    if term['bits'] not in [p['bits'] for p in prime_implicants]:
                        prime_implicants.append({'bits': term['bits'], 'minterms': set(term['minterms'])})
        if not combined_any:
            break
        # chuẩn bị groups cho vòng tiếp theo
        groups = {}
        for t in next_round.values():
            count1 = t['bits'].count('1')
            groups.setdefault(count1, []).append(t)

    # chart: implicant -> minterms
    chart = {p['bits']: sorted(p['minterms']) for p in prime_implicants}

    # tìm essential prime implicants
    remaining = set(minterms)
    minterm_to_primes = {m: [p['bits'] for p in prime_implicants if m in p['minterms']] for m in minterms}
    essential = []
    for m, primes in minterm_to_primes.items():
        if len(primes) == 1:
            p = primes[0]
            if p not in essential:
                essential.append(p)
    # loại minterm đã được cover bởi essential
    for p in essential:
        for m in chart[p]:
            remaining.discard(m)

    # greedy cho phần còn lại
    additional = []
    while remaining:
        best = None
        best_cover = set()
        for p, covers in chart.items():
            cover = set(covers) & remaining
            if len(cover) > len(best_cover):
                best = p
                best_cover = cover
        if best is None:
            break
        additional.append(best)
        for m in best_cover:
            remaining.discard(m)

    selected = essential + additional

    # chuyển implicant bits -> term biến (ví dụ A B' C)
    def bits_to_term(bits):
        parts = []
        for ch, var in zip(bits, var_names):
            if ch == '1':
                parts.append(var)
            elif ch == '0':
                parts.append(var + "'")
            else:  # '-'
                continue
        if not parts:
            return "1"  # phủ hết (hàm luôn đúng)
        return ''.join(parts)

    simplified_expression = ' + '.join(bits_to_term(b) for b in selected) if selected else '0'

    return {
        "prime_implicants": [p['bits'] for p in prime_implicants],
        "chart": chart,
        "essential_prime_implicants": essential,
        "additional_implicants": additional,
        "selected_implicants": selected,
        "simplified_expression": simplified_expression
    }
if __name__ == "__main__":
    # (a) 3 biến: Σm(1,2,5,7)
    minterms = [1, 2, 5, 7]
    num_vars = 3
    result = quine_mccluskey(minterms, num_vars, var_names=["A", "B", "C"])

    print("=== Ví dụ (a): 3 biến ===")
    print("Prime implicants:", result["prime_implicants"])
    print("Chart:", result["chart"])
    print("Essential prime implicants:", result["essential_prime_implicants"])
    print("Selected implicants:", result["selected_implicants"])
    print("Simplified expression:", result["simplified_expression"])

    # (b) 4 biến: Σm(0,1,2,5,6,7,8,9,10,14)
    minterms = [0,1,2,5,6,7,8,9,10,14]
    num_vars = 4
    result = quine_mccluskey(minterms, num_vars, var_names=["A","B","C","D"])

    print("\n=== Ví dụ (b): 4 biến ===")
    print("Prime implicants:", result["prime_implicants"])
    print("Chart:", result["chart"])
    print("Essential prime implicants:", result["essential_prime_implicants"])
    print("Selected implicants:", result["selected_implicants"])
    print("Simplified expression:", result["simplified_expression"])
#Phương pháp K-map
from typing import List, Set, Tuple, Dict
from itertools import product

# =========================
# Karnaugh Map (2..4 vars)
# =========================

def gray_code(n: int) -> List[str]:
    """Danh sách mã Gray n bit theo thứ tự chuẩn."""
    if n == 0:
        return [""]
    prev = gray_code(n - 1)
    return ["0" + x for x in prev] + ["1" + x for x in reversed(prev)]

def bits_of(n: int, k: int) -> str:
    return format(n, f"0{k}b")

def pow2s_up_to(n: int) -> List[int]:
    x, out = 1, []
    while x <= n:
        out.append(x)
        x <<= 1
    return out

class KMap:
    """
    K-map cho 2..4 biến.
    mode='SOP': điền 1 tại minterms, nhóm 1 để tạo SOP
    mode='POS': điền 0 tại maxterms, nhóm 0 để tạo POS
    """
    def __init__(self, num_vars: int, mode: str = "SOP",
                 minterms: List[int] = None, maxterms: List[int] = None,
                 var_names: List[str] = None):
        assert num_vars in (2, 3, 4), "Hỗ trợ 2–4 biến."
        self.n = num_vars
        self.mode = mode.upper()
        assert self.mode in ("SOP", "POS")
        self.var_names = var_names or [chr(ord('A') + i) for i in range(self.n)]

        self.size = 1 << self.n
        self.minterms = sorted(set(minterms or []))
        self.maxterms = sorted(set(maxterms or []))

        # Bố cục hàng/cột theo Gray:
        # 2 biến: hàng=biến 0, cột=biến 1
        # 3 biến: hàng=biến 0, cột=biến 1..2 (2 bit)
        # 4 biến: hàng=biến 0..1 (2 bit), cột=biến 2..3 (2 bit)
        if self.n == 2:
            self.row_bits, self.col_bits = 1, 1
        elif self.n == 3:
            self.row_bits, self.col_bits = 1, 2
        else:  # n == 4
            self.row_bits, self.col_bits = 2, 2

        self.row_labels = gray_code(self.row_bits)
        self.col_labels = gray_code(self.col_bits)

        # Lập ánh xạ minterm -> (row, col) theo thứ tự biến [A,B,C,D]
        self.index_map: Dict[int, Tuple[int, int]] = {}
        self._build_index_map()

        # Khởi tạo lưới giá trị
        self.grid = [[0 for _ in self.col_labels] for _ in self.row_labels]
        self._fill_grid()

    def _build_index_map(self):
        # Với nhãn hàng & cột (mã Gray), khớp bit theo thứ tự biến
        # n=2: row=A, col=B
        # n=3: row=A, col=BC
        # n=4: row=AB, col=CD
        for r, rb in enumerate(self.row_labels):
            for c, cb in enumerate(self.col_labels):
                if self.n == 2:
                    full = rb + cb               # A | B
                elif self.n == 3:
                    full = rb + cb               # A | B C
                else:  # 4
                    full = rb + cb               # A B | C D
                m = int(full, 2)
                self.index_map[m] = (r, c)

    def _fill_grid(self):
        if self.mode == "SOP":
            ones = set(self.minterms)
for m in range(self.size):
                r, c = self.index_map[m]
                self.grid[r][c] = 1 if m in ones else 0
        else:  # POS
            zeros = set(self.maxterms)
            for m in range(self.size):
                r, c = self.index_map[m]
                self.grid[r][c] = 0 if m in zeros else 1

    # ---------- Tìm nhóm hình chữ nhật có quấn biên ----------
    def _rect_cells(self, r0: int, c0: int, h: int, w: int) -> Set[Tuple[int, int]]:
        R, C = len(self.row_labels), len(self.col_labels)
        cells = set()
        for dr in range(h):
            for dc in range(w):
                cells.add(((r0 + dr) % R, (c0 + dc) % C))
        return cells

    def _all_groups(self, target: int) -> List[Set[Tuple[int, int]]]:
        """Tạo tất cả nhóm hình chữ nhật giá trị = target (1 cho SOP, 0 cho POS)."""
        R, C = len(self.row_labels), len(self.col_labels)
        total = R * C
        sizes = list(reversed(pow2s_up_to(total)))  # duyệt nhóm lớn trước không bắt buộc
        groups = set()
        for s in sizes:
            # s = h*w, với h,w là lũy thừa 2 và h<=R, w<=C
            factors = [(h, s // h) for h in pow2s_up_to(s) if s % h == 0]
            # chỉ lấy các cặp (h,w) hợp lệ trong lưới
            hw_list = [(h, w) for (h, w) in factors if h <= R and w <= C]
            for h, w in hw_list:
                for r0 in range(R):
                    for c0 in range(C):
                        cells = self._rect_cells(r0, c0, h, w)
                        if all(self.grid[r][c] == target for (r, c) in cells):
                            groups.add(frozenset(cells))
        # Loại nhóm bị chứa hoàn toàn trong nhóm lớn hơn (giữ "prime groups")
        groups = list(groups)
        prime = []
        for g in groups:
            if not any((g < h) for h in groups):  # g là tập con thực sự của h?
                prime.append(set(g))
        # Sắp xếp giảm dần theo kích thước nhóm
        prime.sort(key=lambda s: (-len(s), sorted(list(s))))
        return prime

    # ---------- Chuyển nhóm -> hạng thức ----------
    def _cells_to_minterms(self, cells: Set[Tuple[int, int]]) -> List[int]:
        rev_index = {v: k for k, v in self.index_map.items()}
        return [rev_index[(r, c)] for (r, c) in cells]

    def _group_to_term_SOP(self, cells: Set[Tuple[int, int]]) -> str:
        """Từ nhóm 1s suy ra tích (product term) cho SOP."""
        ms = self._cells_to_minterms(cells)
        k = self.n
        # Tìm bit cố định trên tất cả minterm
        bit_cols = list(zip(*(bits_of(m, k) for m in ms)))  # list of tuples cột bit
        parts = []
        for i, col in enumerate(bit_cols):
            if all(b == '0' for b in col):
                parts.append(f"{self.var_names[i]}'")
            elif all(b == '1' for b in col):
                parts.append(f"{self.var_names[i]}")
return "".join(parts) if parts else "1"

    def _group_to_term_POS(self, cells: Set[Tuple[int, int]]) -> str:
        """Từ nhóm 0s suy ra tổng (sum term) cho POS."""
        ms = self._cells_to_minterms(cells)
        k = self.n
        bit_cols = list(zip(*(bits_of(m, k) for m in ms)))
        # Tổng (OR) gồm biến “không đổi” nhưng nghịch dấu so với SOP:
        # - nếu bit luôn 0  -> (A + ...) chứa A (không đảo)
        # - nếu bit luôn 1  -> chứa A' trong dấu cộng
        # Biểu diễn chuẩn POS: (x + y + z)
        lits = []
        for i, col in enumerate(bit_cols):
            if all(b == '0' for b in col):
                lits.append(f"{self.var_names[i]}")
            elif all(b == '1' for b in col):
                lits.append(f"{self.var_names[i]}'")
        return "(" + " + ".join(lits) + ")" if lits else "(1)"

    # ---------- Chọn nhóm để phủ (ưu tiên lớn, thiết yếu, rồi tham lam) ----------
    def _select_groups(self, groups: List[Set[Tuple[int, int]]], target: int) -> List[Set[Tuple[int, int]]]:
        """Chọn tập nhóm phủ toàn bộ ô = target."""
        R, C = len(self.row_labels), len(self.col_labels)
        universe = {(r, c) for r in range(R) for c in range(C) if self.grid[r][c] == target}
        selected: List[Set[Tuple[int, int]]] = []

        if not universe:
            return []

        # 1) Nhóm thiết yếu: ô chỉ nằm trong đúng 1 nhóm
        cover_count: Dict[Tuple[int, int], int] = {cell: 0 for cell in universe}
        for g in groups:
            for cell in (g & universe):
                cover_count[cell] += 1

        essential = []
        for cell, cnt in cover_count.items():
            if cnt == 1:
                # tìm nhóm duy nhất chứa cell
                for g in groups:
                    if cell in g:
                        essential.append(g)
                        break
        # thêm thiết yếu
        for g in essential:
            if g not in selected:
                selected.append(g)

        covered = set().union(*selected) if selected else set()
        covered &= universe

        # 2) Tham lam: thêm nhóm phủ nhiều ô chưa phủ nhất
        remaining = universe - covered
        pool = [g for g in groups if g not in selected]
        while remaining:
            best, gain = None, -1
            for g in pool:
                g_gain = len(g & remaining)
                if g_gain > gain:
                    best, gain = g, g_gain
            if not best or gain <= 0:
                break
            selected.append(best)
            covered |= (best & universe)
            remaining = universe - covered
            pool.remove(best)

        return selected

    # ---------- Giao diện chính ----------
    def simplify(self):
        if self.mode == "SOP":
            target = 1
            all_groups = self._all_groups(target=1)
chosen = self._select_groups(all_groups, target=1)
            terms = [self._group_to_term_SOP(g) for g in chosen]
            expr = " + ".join(sorted(set(terms), key=terms.index)) if terms else "0"
            return expr, chosen, all_groups
        else:  # POS
            target = 0
            all_groups = self._all_groups(target=0)
            chosen = self._select_groups(all_groups, target=0)
            terms = [self._group_to_term_POS(g) for g in chosen]
            expr = "".join(sorted(set(terms), key=terms.index)) if terms else "(1)"
            return expr, chosen, all_groups

    def pretty_grid(self) -> str:
        """In lưới K-map với nhãn Gray cho trực quan."""
        header = [" " * (self.row_bits + 2)] + self.col_labels
        lines = ["\t".join(header)]
        for r, rb in enumerate(self.row_labels):
            row = [rb + " |"] + [str(self.grid[r][c]) for c in range(len(self.col_labels))]
            lines.append("\t".join(row))
        return "\n".join(lines)

# =========================
# Ví dụ sử dụng
# =========================
if __name__ == "__main__":
    # --- Ví dụ SOP:
    km = KMap(num_vars=3, mode="SOP", minterms=[0,2,6,7])
    expr, chosen_groups, all_groups = km.simplify()
    print("K-map (SOP) grid:")
    print(km.pretty_grid())
    print("\nNhóm (đã chọn): kích thước và các ô (r,c):")
    for g in chosen_groups:
        print(f"  size={len(g)} -> {sorted(list(g))}")
    print("\nBiểu thức rút gọn (SOP):")
    print("  f =", expr)

    # --- Ví dụ POS:
    km2 = KMap(num_vars=4, mode="POS", maxterms=[1,3,4,11,12])#Phương pháp Quine
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
    expr2, chosen_groups2, _ = km2.simplify()
    print("\nK-map (POS) grid:")
    print(km2.pretty_grid())
    print("\nBiểu thức rút gọn (POS):")
    print("  F =", expr2)
