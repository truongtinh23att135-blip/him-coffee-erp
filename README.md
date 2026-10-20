# HIM COFFEE ERP

Hệ thống quản lý quán cà phê trên **Odoo 19 Community**: website đặt đồ uống, POS, máy in ảo cho quầy Bar, kho theo công thức, hóa đơn, chấm công, tính lương.

Tác giả: **Trương Văn Tình**

## Tính năng

- **Website đặt hàng** `/him`: menu, giỏ hàng, đặt hàng COD, theo dõi đơn. Giá tính ở máy chủ (size L, topping, mã giảm giá).
- **Máy in ảo cho Bar** `/him/bar`: phiếu pha chế tự hiện khi có đơn online hoặc đơn POS, in khổ A5 (mẫu hóa đơn) hoặc 80mm.
- **POS**: nút **Gửi Bar** (chỉ gửi phần món mới), thanh toán tiền mặt hoặc QR chuyển khoản.
- **Kho và công thức** (BoM Kit): bán một ly thì tự trừ nguyên liệu, có cảnh báo sắp hết.
- **Hóa đơn**: VAT đã gồm trong giá, điều khoản thanh toán, nhật ký riêng cho tiền COD.
- **Nhân sự, chấm công, tính lương** (module lương `simple_payroll` chưa nằm trong repo này).

## Luồng nghiệp vụ

## Tài liệu

- [Tài liệu nghiệp vụ (BA Functional Specification)](docs/tai-lieu-nghiep-vu.docx)

## Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| `docker/` | `docker-compose.yml` chạy Odoo 19 và PostgreSQL 15 |
| `addons/him_shop` | Website `/him`, máy in ảo, màn hình Bar `/him/bar` |
| `addons/him_shop_pos` | Cầu nối POS, logic chỉ gửi phần món mới |
| `addons/him_shop_pos_button` | Nút **Gửi Bar** trên giao diện POS |
| `firebase-prototype/` | Bản web đầu tiên (Firebase), giữ làm lịch sử phát triển |

## Chạy thử

1. `cd docker && docker compose up -d`, mở `http://localhost:8069`, tạo database `him_coffee_erp`.
2. Cài ứng dụng: Sales, Inventory, Manufacturing, Purchase, Invoicing (kèm Vietnam - Accounting), Point of Sale (Restaurant), Employees, Attendances.
3. Cài module tùy chỉnh: `docker compose exec web odoo -i him_shop,him_shop_pos,him_shop_pos_button -d him_coffee_erp --db_host db --db_user odoo --db_password odoo --no-http --stop-after-init`, rồi `docker compose restart web`.
4. Tạo khóa API trong Odoo (Preferences, Account Security), lưu vào `~/Documents/odoo-api-key.txt` (**không đưa vào repo**).
5. Mở `http://localhost:8069/him` (web) và `http://localhost:8069/him/bar` (màn hình Bar, cần đăng nhập Odoo).

Tình trạng

- Hoàn thành: website đặt hàng, đơn vào Sales, kho trừ theo công thức, hóa đơn COD, máy in ảo Bar, mã QR chuyển khoản trên POS, nút Gửi Bar từ POS xuống Bar, tự xác nhận tiền chuyển khoản.

- Lưu ý thuế: thuế GTGT 8% áp dụng đến hết 31/12/2026, từ 2027 đổi theo quy định.

Lưu ý bảo mật

Đây là bản demo: mật khẩu cơ sở dữ liệu mặc định, dữ liệu nhân viên, lương, chấm công là dữ liệu mẫu. Không đưa khóa API, số tài khoản ngân hàng hay bản sao lưu cơ sở dữ liệu vào repo.

Bản quyền

Mã nguồn thuộc về tác giả Trương Văn Tình. Hình ảnh món và thương hiệu HIM COFFEE thuộc về chủ sở hữu.
