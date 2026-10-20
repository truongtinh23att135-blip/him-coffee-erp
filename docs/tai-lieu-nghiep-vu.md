**HIM COFFEE**

**Odoo ERP Business Analysis & Functional Specification**

(Phân tích nghiệp vụ & Đặc tả chức năng giải pháp Odoo ERP)

**Bản đặc tả tổng hợp – từ Business Overview đến UAT**

*Version 2.0 \| Draft for Review*

# Document Control (Quản lý tài liệu)

| **Trường**       | **Giá trị**                                                                                               |
|------------------|-----------------------------------------------------------------------------------------------------------|
| Document Name    | HIM Coffee – Odoo ERP Business Analysis & Functional Specification                                        |
| Version          | 1.0 – Draft for Review                                                                                    |
| Purpose          | Tài liệu mô tả nghiệp vụ, yêu cầu, quy trình TO-BE, solution mapping và kiểm thử UAT                      |
| Scope            | POS, Inventory, Purchase, Accounting, Employees, Attendance, Payroll, CRM/Sales và các tích hợp liên quan |
| Primary Audience | Business Owner, Store Manager, BA, Odoo Functional Consultant, Developer, QA, Accountant, HR              |
| Status           | Review / Validation                                                                                       |
| Important Note   | Các điểm chưa xác nhận với HIM được đánh dấu Assumption / Proposed / Open Question                        |

## Document Principles (Nguyên tắc xây dựng)

- Business-first: bắt đầu từ hoạt động kinh doanh, sau đó mới ánh xạ
  sang Odoo.

- Standard-first: ưu tiên Odoo Standard trước khi đề xuất Studio,
  Automation hoặc Custom Module.

- Fact / Assumption / Proposed Solution phải được phân biệt rõ.

- AS-IS không được tự ý coi là sự thật nếu chưa xác nhận với người dùng
  nghiệp vụ.

- TO-BE là quy trình đề xuất nhằm chuẩn hóa vận hành và tạo dữ liệu quản
  trị.

- Requirement phải truy vết được từ Business Requirement → Functional
  Requirement → Rule → Use Case → Odoo Solution → UAT.

# Executive Summary (Tóm tắt điều hành)

Mục tiêu của tài liệu là mô tả một giải pháp Odoo ERP có khả năng hỗ trợ
toàn bộ chuỗi vận hành của HIM Coffee, thay vì chỉ tập trung vào CRM.
CRM được xem là một thành phần hỗ trợ, đặc biệt cho khách hàng doanh
nghiệp/B2B; các quy trình vận hành cốt lõi nằm ở Restaurant POS,
Inventory, Purchase, Accounting và nhóm Employees/Attendance/Payroll.

Mô hình vận hành được phân tích theo nguyên tắc mỗi cơ sở có kho riêng
và không giả định tồn tại kho trung tâm. Vì vậy, mọi bài toán
replenishment (bổ sung hàng), internal transfer (điều chuyển nội bộ),
purchase (mua hàng) và online order đều phải xác định rõ cơ sở/kho chịu
trách nhiệm.

**ERP Value Chain (Chuỗi giá trị tổng thể)**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Nhu cầu / Khách hàng"] --&gt; B{"Kênh bán hàng"}<br />
B --&gt; C["POS nhà hàng"]<br />
B --&gt; D["Đơn hàng trực tuyến"]<br />
C --&gt; E["Pha chế / Phục vụ"]<br />
D --&gt; F["Xác định cơ sở phục vụ"]<br />
F --&gt; E<br />
E --&gt; G["Tiêu hao nguyên liệu"]<br />
G --&gt; H["Kho của cơ sở"]<br />
H --&gt; I{"Cần bổ sung hàng?"}<br />
I --&gt;|Có| J{"Nguồn nội bộ đủ?"}<br />
I --&gt;|Không| K["Tiếp tục vận hành"]<br />
J --&gt;|Có| L["Điều chuyển nội bộ"]<br />
J --&gt;|Không| M["Mua hàng"]<br />
L --&gt; H<br />
M --&gt; H<br />
C --&gt; N["Thanh toán"]<br />
D --&gt; N<br />
N --&gt; O["Doanh thu / Kế toán"]<br />
H --&gt; P["Giá vốn"]<br />
O --&gt; Q["Báo cáo quản trị"]<br />
P --&gt; Q<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 1. Tổng quan dự án

## 1.1. Bối cảnh dự án

HIM Coffee được phân tích dưới góc nhìn chuỗi cửa hàng F&B. Bài toán ERP
không chỉ là tạo đơn hàng mà phải liên kết bán hàng, pha chế, tồn kho
nguyên liệu, mua hàng, điều chuyển giữa các cơ sở, doanh thu, chi phí,
nhân sự và báo cáo.

## 1.2. Mục tiêu nghiệp vụ

| **ID**  | **Mục tiêu**                 | **Kết quả mong đợi**                                                     |
|---------|------------------------------|--------------------------------------------------------------------------|
| OBJ-001 | Chuẩn hóa bán hàng tại bàn   | Order được gắn bàn, chuyển đến khu vực chuẩn bị, thanh toán và đóng bàn. |
| OBJ-002 | Kiểm soát tồn kho theo cơ sở | Biết On Hand, Reserved, Available, Incoming theo từng kho.               |
| OBJ-003 | Chuẩn hóa replenishment      | Thiếu hàng phải xác định nguồn: điều chuyển hoặc mua.                    |
| OBJ-004 | Kiểm soát mua hàng           | Theo dõi RFQ → PO → Receipt → Bill → Payment.                            |
| OBJ-005 | Quản lý doanh thu            | Doanh thu theo ngày, cơ sở, POS, sản phẩm và phương thức thanh toán.     |
| OBJ-006 | Quản lý nhân sự              | Hồ sơ, ca, chấm công, nghỉ phép, OT và payroll.                          |
| OBJ-007 | Quản trị khách hàng          | Lưu lịch sử mua và quản lý B2B opportunity khi cần.                      |
| OBJ-008 | Tạo dữ liệu quản trị         | Dashboard phản ánh doanh thu, COGS, tồn kho, payroll và lợi nhuận.       |

# 2. Bối cảnh nghiệp vụ

## 2.1. Mô hình kinh doanh

Mô hình cốt lõi là bán đồ uống/thực phẩm tại cửa hàng, với Restaurant
POS là điểm phát sinh giao dịch. Ngoài giao dịch tại cửa hàng, hệ thống
có thể cần hỗ trợ online/app hoặc các kênh ngoài; phần online được xem
là một luồng cần xác nhận về tích hợp và quy tắc phân bổ cơ sở.

## 2.2. Mô hình vận hành

| **Area**    | **Đặc điểm phân tích**        | **Hệ quả ERP**                                                |
|-------------|-------------------------------|---------------------------------------------------------------|
| Store       | Nhiều cơ sở                   | Mỗi cơ sở cần định danh rõ.                                   |
| Warehouse   | Kho độc lập theo cơ sở        | Stock phải phân biệt theo warehouse/location.                 |
| POS         | Restaurant/table service      | Không dùng logic retail checkout thuần túy cho quy trình bàn. |
| Preparation | Bar/khu vực pha chế           | Order cần truyền thông tin sản phẩm và bàn.                   |
| Procurement | Nguyên liệu cần replenishment | Phải xác định internal transfer hay vendor purchase.          |
| Finance     | Revenue/COGS/OPEX             | Cần liên kết POS, inventory, purchase, payroll và accounting. |
| HR          | Nhân viên theo cơ sở/ca       | Cần master employee + schedule + attendance.                  |

## 2.3. Các giả định vận hành chính

- FACT: Mỗi cơ sở có kho riêng; không thiết kế luồng mặc định dựa trên
  kho trung tâm.

- FACT: Restaurant POS phù hợp với nghiệp vụ bàn của quán cà phê; không
  đồng nhất với Retail/Supermarket POS.

- ASSUMPTION: Bar có thể nhận order qua preparation screen hoặc phương
  thức tương đương; cần xác nhận cách HIM đang vận hành.

- ASSUMPTION: Các quy tắc discount, loyalty, refund, split bill,
  transfer table chưa được coi là policy chính thức nếu chưa được xác
  nhận.

- PROPOSED: Thiết lập branch/warehouse rõ ràng để mọi giao dịch có owner
  về mặt vận hành và báo cáo.

# 3. Phân tích các bên liên quan

| **Stakeholder**     | **Mục tiêu**                  | **Thông tin cần**                        | **Quyền/Trách nhiệm**                 |
|---------------------|-------------------------------|------------------------------------------|---------------------------------------|
| Owner/Director      | Kiểm soát hiệu quả kinh doanh | Revenue, COGS, Profit, branch comparison | Xem dashboard, phê duyệt policy       |
| Store Manager       | Điều hành cơ sở               | Sales, stock, staff, exceptions          | Duyệt transfer/adjustment theo policy |
| Cashier/Service     | Xử lý bán hàng                | Table, order, payment                    | Create/update order trong quyền hạn   |
| Barista/Preparation | Chuẩn bị sản phẩm             | Order, table, item, status               | Nhận và hoàn thành preparation        |
| Warehouse Staff     | Quản lý stock                 | On Hand, transfer, receipt               | Picking/receiving                     |
| Purchasing          | Mua nguyên liệu               | RFQ, vendor, PO                          | Tạo/điều phối PO                      |
| Accountant          | Đối soát tài chính            | Payments, bills, journals                | Reconcile, reporting                  |
| HR                  | Quản lý nhân sự               | Employee, contract, attendance           | Master data, payroll input            |
| CRM/Sales           | Khách B2B                     | Lead, opportunity, quotation             | Follow-up corporate customers         |
| System Admin        | Hệ thống                      | Users, roles, configuration              | Access/configuration                  |

# 4. Phạm vi dự án

## 4.1. Phạm vi thực hiện

| **Domain**     | **In Scope**                                                                     |
|----------------|----------------------------------------------------------------------------------|
| Restaurant POS | Bàn, order, product, preparation flow, payment, close order                      |
| Inventory      | Warehouses, locations, stock, replenishment, internal transfer, receiving        |
| Purchase       | Vendor, RFQ, PO, receipt, vendor bill handoff                                    |
| Accounting     | Revenue/payment integration, vendor bill, COGS concept, OPEX, payroll accounting |
| Employees      | Employee master, branch, department, job                                         |
| Attendance     | Check-in/out, work hours, overtime input                                         |
| Payroll        | Salary structure, allowance, deduction, gross/net calculation framework          |
| CRM            | B2B leads/opportunities, activities, quotation linkage                           |
| Reporting      | Revenue, stock, payroll, COGS/profit, operational KPI                            |

## 4.2. Ngoài phạm vi / Cần xác nhận

- Native mobile application development cho khách hàng.

- Third-party delivery rider management nếu chưa có integration
  specification.

- Advanced manufacturing nếu thực tế HIM không có production process phù
  hợp.

- Exact Vietnamese tax/insurance legal parameters trong payroll nếu chưa
  chốt thời điểm áp dụng và legal basis.

- Exact loyalty/discount percentages nếu chưa có business policy.

# 5. Quy trình hiện tại (AS-IS)

Phần AS-IS trong tài liệu BA phải phân biệt quy trình đã xác nhận với
các điểm cần khảo sát. Vì tài liệu hiện tại chưa có biên bản phỏng vấn
đầy đủ của từng bộ phận, các flow dưới đây được ghi nhận ở mức working
model và phải được HIM validate trước khi triển khai.

## 5.1. Quy trình bán hàng tại bàn – Mô hình cần xác nhận

Luồng quy trình hiện tại cần xác nhận

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách đến cơ sở"] --&gt; B["Chọn bàn"]<br />
B --&gt; C["Nhân viên ghi nhận món"]<br />
C --&gt; D["Gửi món cho quầy pha chế"]<br />
D --&gt; E["Quầy pha chế chuẩn bị"]<br />
E --&gt; F["Phục vụ khách"]<br />
F --&gt; G{"Khách gọi thêm?"}<br />
G --&gt;|Có| C<br />
G --&gt;|Không| H["Yêu cầu thanh toán"]<br />
H --&gt; I["Thu tiền"]<br />
I --&gt; J["Đóng đơn"]<br />
J --&gt; K["Bàn trở về trạng thái trống"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 5.2. Quy trình tồn kho – Mô hình cần xác nhận

Luồng quy trình hiện tại cần xác nhận

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Cơ sở phát sinh nhu cầu nguyên liệu"] --&gt; B["Kiểm tra tồn kho hiện
tại"]<br />
B --&gt; C["Kiểm tra kho HIM khác / nhà cung cấp"]<br />
C --&gt; D{"Có nguồn đáp ứng?"}<br />
D --&gt;|Có| E["Điều chuyển hoặc mua theo quy định"]<br />
D --&gt;|Không| F["Ghi nhận thiếu hàng / xử lý ngoại lệ"]<br />
E --&gt; G["Nhận hàng tại cơ sở"]<br />
G --&gt; H["Cập nhật tồn kho"]<br />
H --&gt; I["Tiếp tục vận hành"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 5.3. Các vấn đề cần xác nhận

| **ID** | **Potential Pain Point**                | **Business Impact**             | **Validation**         |
|--------|-----------------------------------------|---------------------------------|------------------------|
| PP-001 | Order/bàn chưa có trạng thái thống nhất | Khó biết order đang ở đâu       | Interview Store        |
| PP-002 | Tồn kho không đồng nhất giữa cơ sở      | Khó ra quyết định replenishment | Stock count            |
| PP-003 | Điều chuyển không có approval rõ        | Rủi ro thiếu hàng tại kho nguồn | Interview Manager      |
| PP-004 | Doanh thu và payment cần đối soát       | Sai lệch cash/payment           | Accounting workshop    |
| PP-005 | Chấm công/payroll thủ công              | Sai giờ, OT, lương              | HR workshop            |
| PP-006 | COGS chưa liên kết consumption          | Khó tính gross margin           | Accounting + Inventory |
| PP-007 | B2B customer follow-up rời rạc          | Mất cơ hội corporate            | CRM/Sales workshop     |

# 6. Vấn đề và phân tích nguyên nhân

| **Problem**                                  | **Likely Root Cause**            | **Effect**       | **ERP Response**              |
|----------------------------------------------|----------------------------------|------------------|-------------------------------|
| Không biết order đang ở trạng thái nào       | Thiếu workflow chuẩn             | Chậm phục vụ     | POS + preparation flow        |
| Thiếu nguyên liệu nhưng không biết lấy ở đâu | Không có source decision         | Stockout         | Inventory replenishment logic |
| Điều chuyển gây thiếu kho nguồn              | Không xét Available/Safety Stock | Rủi ro vận hành  | Approval + source check       |
| Doanh thu khó đối soát                       | Payment tách khỏi order          | Sai số cuối ngày | POS payment + reconciliation  |
| Lợi nhuận không rõ                           | Thiếu COGS/OPEX linkage          | Quản trị kém     | Revenue + COGS + OPEX model   |
| Lương phụ thuộc bảng tay                     | Attendance không liên kết        | Sai payroll      | Attendance + Payroll          |

# 7. Yêu cầu nghiệp vụ

| **ID**     | **Requirement**            | **Description**                                                                                           | **Priority** |
|------------|----------------------------|-----------------------------------------------------------------------------------------------------------|--------------|
| BR-POS-001 | Quản lý order theo bàn     | Hệ thống phải quản lý order gắn với bàn để nhân viên biết khách đang ngồi đâu và order nào thuộc bàn nào. | Must         |
| BR-POS-002 | Preparation visibility     | Khu vực chuẩn bị phải nhận được thông tin item/order cần làm.                                             | Must         |
| BR-POS-003 | Payment control            | Giao dịch phải được thanh toán và đóng đúng trạng thái.                                                   | Must         |
| BR-INV-001 | Stock by branch            | Tồn kho phải được theo dõi theo từng cơ sở/kho.                                                           | Must         |
| BR-INV-002 | Source-based replenishment | Thiếu hàng phải kiểm tra nguồn nội bộ và nguồn mua.                                                       | Must         |
| BR-INV-003 | Transfer control           | Điều chuyển phải có trạng thái và trách nhiệm rõ.                                                         | Must         |
| BR-PUR-001 | Purchase lifecycle         | Theo dõi từ nhu cầu đến PO, receipt và bill.                                                              | Must         |
| BR-ACC-001 | Revenue control            | Doanh thu phải đối soát theo giao dịch và payment.                                                        | Must         |
| BR-ACC-002 | Profit visibility          | Có thể xác định gross profit và operating profit theo phạm vi báo cáo.                                    | Should       |
| BR-HR-001  | Employee master            | Quản lý nhân viên theo cơ sở và vị trí.                                                                   | Must         |
| BR-HR-002  | Attendance                 | Ghi nhận giờ làm và dữ liệu OT.                                                                           | Must         |
| BR-HR-003  | Payroll                    | Tính lương dựa trên dữ liệu được phê duyệt.                                                               | Must         |
| BR-CRM-001 | Corporate CRM              | Quản lý lead/opportunity B2B khi có nhu cầu.                                                              | Should       |
| BR-RPT-001 | Management dashboard       | Quản lý xem KPI vận hành và tài chính.                                                                    | Must         |

# 8. Yêu cầu chức năng

| **ID**     | **Function**       | **Description**                                                            | **Module**           | **BR**     |
|------------|--------------------|----------------------------------------------------------------------------|----------------------|------------|
| FR-POS-001 | Open Table         | User có thể mở bàn và tạo order.                                           | POS                  | BR-POS-001 |
| FR-POS-002 | Add Item           | User thêm product và quantity vào order.                                   | POS                  | BR-POS-001 |
| FR-POS-003 | Send Preparation   | Order/item được gửi tới preparation workflow.                              | POS                  | BR-POS-002 |
| FR-POS-004 | Preparation Status | Theo dõi New/Preparing/Ready hoặc trạng thái tương đương theo Odoo config. | POS                  | BR-POS-002 |
| FR-POS-005 | Payment            | User chọn payment method và xác nhận thanh toán.                           | POS/Accounting       | BR-POS-003 |
| FR-POS-006 | Close Order        | Order được đóng sau khi hoàn tất payment.                                  | POS                  | BR-POS-003 |
| FR-INV-001 | Warehouse Master   | Tạo warehouse/location theo cơ sở.                                         | Inventory            | BR-INV-001 |
| FR-INV-002 | Stock Visibility   | Xem On Hand/Reserved/Available/Incoming.                                   | Inventory            | BR-INV-001 |
| FR-INV-003 | Transfer Request   | Tạo yêu cầu điều chuyển từ source tới destination.                         | Inventory            | BR-INV-003 |
| FR-INV-004 | Source Validation  | Kiểm tra stock source trước khi approve.                                   | Inventory            | BR-INV-002 |
| FR-INV-005 | Receive Transfer   | Kho đích xác nhận receipt.                                                 | Inventory            | BR-INV-003 |
| FR-PUR-001 | RFQ/PO             | Tạo RFQ/PO cho vendor.                                                     | Purchase             | BR-PUR-001 |
| FR-PUR-002 | Receipt            | Nhập hàng và cập nhật stock.                                               | Inventory/Purchase   | BR-PUR-001 |
| FR-PUR-003 | Vendor Bill        | Liên kết receipt/PO với vendor bill process.                               | Accounting           | BR-PUR-001 |
| FR-HR-001  | Employee Master    | Quản lý thông tin nhân viên.                                               | Employees            | BR-HR-001  |
| FR-HR-002  | Attendance         | Check-in/out và tổng hợp giờ.                                              | Attendances          | BR-HR-002  |
| FR-HR-003  | Payroll Inputs     | Tập hợp salary, OT, allowance, deduction.                                  | Payroll              | BR-HR-003  |
| FR-HR-004  | Payslip            | Tạo payslip và xác nhận theo approval flow.                                | Payroll              | BR-HR-003  |
| FR-ACC-001 | Revenue Report     | Báo cáo gross/net sales theo branch/date.                                  | Accounting/POS       | BR-ACC-001 |
| FR-ACC-002 | COGS Report        | Theo dõi cost/consumption theo product hoặc branch khi dữ liệu đủ.         | Accounting/Inventory | BR-ACC-002 |
| FR-CRM-001 | B2B Opportunity    | Tạo opportunity và stage pipeline.                                         | CRM                  | BR-CRM-001 |
| FR-RPT-001 | Dashboard          | Dashboard KPI cho owner/manager.                                           | Reporting            | BR-RPT-001 |

# 9. Yêu cầu phi chức năng

| **ID**  | **Category**       | **Requirement**                                                               |
|---------|--------------------|-------------------------------------------------------------------------------|
| NFR-001 | Security           | User chỉ truy cập chức năng/dữ liệu theo role.                                |
| NFR-002 | Branch Isolation   | Người dùng cửa hàng chỉ thấy dữ liệu được phép theo cơ sở.                    |
| NFR-003 | Auditability       | Các giao dịch quan trọng phải có người tạo/thời điểm/trạng thái.              |
| NFR-004 | Data Integrity     | Không cho phép trạng thái nghiệp vụ mâu thuẫn.                                |
| NFR-005 | Usability          | POS phải đủ đơn giản để nhân viên thao tác nhanh.                             |
| NFR-006 | Performance        | Các thao tác POS phổ biến không được tạo cảm giác chậm bất thường.            |
| NFR-007 | Availability       | Hệ thống phải có phương án vận hành khi có sự cố mạng theo khả năng Odoo POS. |
| NFR-008 | Reporting Accuracy | KPI phải có định nghĩa và nguồn dữ liệu rõ.                                   |
| NFR-009 | Scalability        | Thiết kế branch/warehouse cho phép mở rộng cơ sở.                             |
| NFR-010 | Maintainability    | Ưu tiên cấu hình Standard, hạn chế custom code không cần thiết.               |

# 10. Quy tắc nghiệp vụ

| **Rule ID**   | **Business Rule**                                                                                     |
|---------------|-------------------------------------------------------------------------------------------------------|
| BRULE-POS-001 | Một order tại bàn phải xác định đúng POS session/table.                                               |
| BRULE-POS-002 | Không coi bàn đã thanh toán là còn active.                                                            |
| BRULE-POS-003 | Cancel/refund sau preparation phải tuân theo quyền hạn.                                               |
| BRULE-INV-001 | Warehouse A thiếu hàng không đồng nghĩa tự động chuyển từ B.                                          |
| BRULE-INV-002 | Source warehouse phải được kiểm tra Available trước khi transfer.                                     |
| BRULE-INV-003 | Post-transfer Available của source không nên thấp hơn Safety Stock nếu policy này được HIM phê duyệt. |
| BRULE-INV-004 | Điều chuyển phải có source, destination, product, quantity và trạng thái.                             |
| BRULE-INV-005 | Chênh lệch shipped vs received phải được ghi nhận và xử lý.                                           |
| BRULE-PUR-001 | Nếu nguồn nội bộ không đủ thì có thể phát sinh purchase requirement.                                  |
| BRULE-PUR-002 | PO chỉ được gửi vendor theo approval policy.                                                          |
| BRULE-ACC-001 | Net Revenue = Gross Sales – Discounts – Returns/Refunds theo định nghĩa báo cáo.                      |
| BRULE-ACC-002 | Gross Profit = Net Revenue – COGS.                                                                    |
| BRULE-ACC-003 | Operating Profit = Gross Profit – Operating Expenses.                                                 |
| BRULE-HR-001  | Payroll chỉ chạy trên dữ liệu đã khóa/approved theo policy.                                           |
| BRULE-HR-002  | OT phải có người/role phê duyệt.                                                                      |
| BRULE-HR-003  | Exact tax/insurance parameters phải là configuration theo legal period, không hard-code vào tài liệu. |
| BRULE-CRM-001 | CRM Lead/Opportunity chủ yếu phục vụ prospect/B2B; không biến mọi khách POS thành opportunity.        |

# 11. Kịch bản sử dụng

| **UC ID**  | **Use Case**                 | **Actor**             | **Main Action**                                            | **Expected Result**                   |
|------------|------------------------------|-----------------------|------------------------------------------------------------|---------------------------------------|
| UC-POS-001 | Create Table Order           | Service Staff         | Mở bàn, thêm món, gửi preparation.                         | Order được tạo và gắn bàn.            |
| UC-POS-002 | Process Payment              | Cashier               | Kiểm tra order, payment, close.                            | Payment thành công, order đóng.       |
| UC-POS-003 | Prepare Order                | Barista               | Nhận order, chuẩn bị, đánh dấu ready.                      | Item sẵn sàng phục vụ.                |
| UC-INV-001 | Request Transfer             | Store Manager         | Tạo transfer request khi thiếu hàng.                       | Request có source/destination.        |
| UC-INV-002 | Approve Transfer             | Source Manager        | Kiểm tra stock và quyết định approve/adjust/reject.        | Transfer được phê duyệt hoặc từ chối. |
| UC-INV-003 | Receive Transfer             | Destination Warehouse | Kiểm tra hàng thực nhận.                                   | Stock đích cập nhật.                  |
| UC-PUR-001 | Purchase Replenishment       | Purchasing            | Tạo RFQ/PO và nhận hàng.                                   | Stock tăng và bill được xử lý.        |
| UC-HR-001  | Record Attendance            | Employee              | Check-in/out.                                              | Attendance record được tạo.           |
| UC-HR-002  | Run Payroll                  | HR                    | Review inputs, generate payslip, approve.                  | Payslip hợp lệ.                       |
| UC-ACC-001 | Daily Closing                | Cashier/Manager       | Đối soát order và payment.                                 | Daily sales close.                    |
| UC-CRM-001 | Manage Corporate Opportunity | CRM/Sales             | Qualification → Needs → Proposal → Negotiation → Won/Lost. | Opportunity có lịch sử hoạt động.     |

# 12. Quy trình đề xuất (TO-BE)

## 12.1. Quy trình ERP đầu-cuối

Luồng vận hành ERP tổng thể

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Nhu cầu / Khách hàng"] --&gt; B{"Kênh bán hàng"}<br />
B --&gt; C["POS nhà hàng"]<br />
B --&gt; D["Đơn hàng trực tuyến"]<br />
C --&gt; E["Xác định bàn / đơn"]<br />
D --&gt; F["Xác định cơ sở phục vụ"]<br />
E --&gt; G["Pha chế / Chuẩn bị"]<br />
F --&gt; G<br />
G --&gt; H["Phục vụ / Giao hàng"]<br />
H --&gt; I["Thanh toán"]<br />
I --&gt; J["Doanh thu"]<br />
G --&gt; K["Tiêu hao nguyên liệu"]<br />
K --&gt; L["Kho cơ sở"]<br />
L --&gt; M{"Tồn kho dưới ngưỡng?"}<br />
M --&gt;|Có| N{"Nguồn nội bộ đủ?"}<br />
M --&gt;|Không| O["Tiếp tục vận hành"]<br />
N --&gt;|Có| P["Điều chuyển nội bộ"]<br />
N --&gt;|Không| Q["Mua hàng"]<br />
P --&gt; L<br />
Q --&gt; L<br />
L --&gt; R["Giá vốn"]<br />
J --&gt; S["Kế toán / Báo cáo"]<br />
R --&gt; S<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 12.2. Quy trình POS nhà hàng chi tiết

Luồng POS nhà hàng

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách chọn Bàn 02"] --&gt; B["Nhân viên mở Bàn 02"]<br />
B --&gt; C["Tạo đơn"]<br />
C --&gt; D["Thêm Bạc Xỉu x1"]<br />
D --&gt; E["Gửi món"]<br />
E --&gt; F["Quầy pha chế nhận Bàn 02 + món"]<br />
F --&gt; G["Đang pha chế"]<br />
G --&gt; H["Món đã sẵn sàng"]<br />
H --&gt; I["Nhân viên phục vụ"]<br />
I --&gt; J{"Khách gọi thêm?"}<br />
J --&gt;|Có| D<br />
J --&gt;|Không| K["Yêu cầu thanh toán"]<br />
K --&gt; L["Chọn khách hàng nếu có"]<br />
L --&gt; M["Áp dụng ưu đãi hợp lệ nếu có"]<br />
M --&gt; N["Chọn phương thức thanh toán"]<br />
N --&gt; O["Xác nhận thanh toán"]<br />
O --&gt; P["Đóng đơn"]<br />
P --&gt; Q["Bàn 02 trở về trạng thái trống"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 12.3. Quy trình đơn hàng trực tuyến / ứng dụng

Luồng đơn hàng trực tuyến

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách đặt App / Website / Kênh ngoài"] --&gt; B["Đơn hàng vào Odoo /
hệ thống tích hợp"]<br />
B --&gt; C["Xác định cơ sở phục vụ"]<br />
C --&gt; D{"Cơ sở hợp lệ?"}<br />
D --&gt;|Không| X["Ngoại lệ: không xác định được cơ sở"]<br />
D --&gt;|Có| E["Kiểm tra sản phẩm và tồn kho của cơ sở"]<br />
E --&gt; F{"Đủ hàng?"}<br />
F --&gt;|Không| Y["Ngoại lệ: thay thế / hủy / hoàn tiền / chuyển cơ sở
theo chính sách"]<br />
F --&gt;|Có| G["Xác nhận đơn"]<br />
G --&gt; H["Pha chế tại cơ sở"]<br />
H --&gt; I["Sẵn sàng"]<br />
I --&gt; J["Khách nhận / Giao hàng"]<br />
J --&gt; K["Thanh toán / Đối soát"]<br />
K --&gt; L["Kế toán / Báo cáo"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 13. Phân tích khoảng cách

| **Gap ID** | **Need**                      | **Odoo Capability**                             | **Solution Direction**            | **Open Point**                   |
|------------|-------------------------------|-------------------------------------------------|-----------------------------------|----------------------------------|
| GAP-001    | Restaurant table operation    | Odoo Standard                                   | Cấu hình POS/restaurant           | Validate exact preparation flow  |
| GAP-002    | Branch-specific warehouse     | Odoo Standard                                   | Warehouse/location configuration  | Must define access               |
| GAP-003    | Transfer approval             | Standard may not cover exact HIM approval chain | May need Studio/Automation/Custom | Design after policy confirmation |
| GAP-004    | Ingredient consumption        | Depends on recipe/process                       | Standard Inventory/MRP options    | Validate whether MO is used      |
| GAP-005    | Payroll legal localization    | Odoo localization/configuration                 | Parameterize                      | Validate current legal rules     |
| GAP-006    | App integration               | External dependency                             | API/integration                   | Need technical specification     |
| GAP-007    | Advanced KPI profit by branch | Standard + analytic accounting/reporting        | Configuration/custom report       | Define accounting model          |

# 14. Ánh xạ giải pháp Odoo

| **Module**  | **Odoo Area**  | **Purpose**                                | **Approach**                   |
|-------------|----------------|--------------------------------------------|--------------------------------|
| POS         | Restaurant POS | Table/order/preparation/payment            | Standard-first                 |
| Inventory   | Inventory      | Warehouse, location, transfer, stock moves | Standard-first                 |
| Purchase    | Purchase       | Vendor/RFQ/PO/receipt                      | Standard-first                 |
| Accounting  | Accounting     | Payment, journals, vendor bills, reporting | Standard-first                 |
| Employees   | Employees      | Employee master                            | Standard-first                 |
| Attendances | Attendances    | Check-in/out                               | Standard-first                 |
| Time Off    | Time Off       | Leave                                      | Standard-first                 |
| Payroll     | Payroll        | Salary structures/payslips                 | Standard + localization/config |
| CRM         | CRM            | B2B lead/opportunity/activity              | Standard-first                 |
| Sales       | Sales          | Quotation/order for B2B                    | Standard-first                 |
| MRP         | Manufacturing  | Only if production model warrants it       | Validate before enabling       |

# 15. Mô hình dữ liệu

Quan hệ dữ liệu logic

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
erDiagram<br />
CO_SO ||--o{ KHO : "quản lý"<br />
KHO ||--o{ VI_TRI_KHO : "có vị trí"<br />
KHO ||--o{ TON_KHO : "quản lý tồn"<br />
CO_SO ||--o{ CAU_HINH_POS : "sử dụng"<br />
CO_SO ||--o{ NHAN_VIEN : "quản lý"<br />
<br />
KHACH_HANG ||--o{ DON_POS : "mua hàng"<br />
DON_POS ||--|{ DONG_DON_POS : "gồm"<br />
DON_POS ||--o{ THANH_TOAN : "có"<br />
KHACH_HANG ||--o{ CO_HOI_B2B : "có cơ hội"<br />
<br />
SAN_PHAM ||--o{ DONG_DON_POS : "được bán"<br />
SAN_PHAM ||--o{ DINH_MUC : "có định mức"<br />
DINH_MUC ||--o{ THANH_PHAN_DINH_MUC : "gồm"<br />
SAN_PHAM ||--o{ THANH_PHAN_DINH_MUC : "là thành phần"<br />
<br />
KHO ||--o{ PHIEU_NHAP : "nhận hàng"<br />
KHO ||--o{ PHIEU_XUAT : "xuất hàng"<br />
KHO ||--o{ PHIEU_DIEU_CHUYEN : "tham gia điều chuyển"<br />
<br />
NHA_CUNG_CAP ||--o{ DON_MUA : "được mua từ"<br />
DON_MUA ||--o{ PHIEU_NHAP : "phát sinh nhập"<br />
DON_MUA ||--o{ HOA_DON_NCC : "phát sinh hóa đơn"<br />
<br />
NHAN_VIEN ||--o{ CHAM_CONG : "có chấm công"<br />
NHAN_VIEN ||--o{ NGHI_PHEP : "có nghỉ phép"<br />
NHAN_VIEN ||--o{ PHIEU_LUONG : "có phiếu lương"<br />
NHAN_VIEN ||--o{ HOP_DONG : "có hợp đồng"<br />
<br />
DON_POS ||--o{ DOANH_THU : "tạo doanh thu"<br />
TON_KHO ||--o{ GIA_VON : "tạo giá vốn"<br />
PHIEU_LUONG ||--o{ CHI_PHI_LUONG : "tạo chi phí lương"<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 15.1. Từ điển dữ liệu cốt lõi

| **Entity**     | **Vietnamese Meaning** | **Key Fields**                                   |
|----------------|------------------------|--------------------------------------------------|
| Branch         | Cơ sở                  | Branch ID, Name, Address, Status                 |
| Warehouse      | Kho                    | Warehouse Code, Branch, Location                 |
| Product        | Sản phẩm               | SKU, Name, Category, UoM, Sales Price, Cost      |
| Ingredient     | Nguyên liệu            | SKU, Purchase UoM, Stock UoM, Cost               |
| Recipe/BOM     | Định mức               | Product, Component, Qty                          |
| POS Order      | Đơn POS                | Order No, Session, Table, Customer, Date, Status |
| POS Line       | Dòng đơn               | Product, Qty, Price, Discount                    |
| Payment        | Thanh toán             | Method, Amount, Date, Reference                  |
| Transfer       | Điều chuyển            | Source, Destination, Product, Qty, Status        |
| Purchase Order | Đơn mua                | Vendor, Product, Qty, Price, Status              |
| Employee       | Nhân viên              | Employee ID, Branch, Job, Department             |
| Attendance     | Chấm công              | Employee, Check-in, Check-out, Hours             |
| Payslip        | Phiếu lương            | Employee, Period, Gross, Deduction, Net          |
| Opportunity    | Cơ hội                 | Customer, Stage, Expected Revenue, Probability   |

# 16. Thiết kế tồn kho và bổ sung hàng

## 16.1. Các khái niệm tồn kho

| **Metric**   | **Meaning**             | **Decision Use**                   |
|--------------|-------------------------|------------------------------------|
| On Hand      | Tồn thực tế ghi nhận    | Biết đang có bao nhiêu             |
| Reserved     | Đã giữ cho nhu cầu      | Không nên coi toàn bộ là available |
| Available    | Có thể sử dụng/đáp ứng  | Nguồn để quyết định transfer       |
| Incoming     | Đang trên đường về      | Dự báo replenishment               |
| Safety Stock | Mức đệm bảo vệ          | Tránh transfer quá mức             |
| Min Stock    | Ngưỡng cảnh báo/reorder | Kích hoạt nhu cầu replenishment    |

## 16.2. Ví dụ – Kho B

| **Metric**                | **Coffee Beans**                                               |
|---------------------------|----------------------------------------------------------------|
| On Hand                   | 20 kg                                                          |
| Reserved                  | 8 kg                                                           |
| Available                 | 12 kg                                                          |
| Safety Stock              | 5 kg                                                           |
| Requested Transfer from A | 10 kg                                                          |
| Post-transfer Available   | 2 kg                                                           |
| Decision                  | Flag / block under proposed safety-stock rule; manager reviews |

Đây là ví dụ minh họa cho logic ra quyết định, không phải policy chính
thức của HIM. Nếu HIM không dùng Safety Stock, rule phải được điều
chỉnh.

## 16.3. Vòng đời điều chuyển

Vòng đời điều chuyển nội bộ

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Yêu cầu điều chuyển"] --&gt; B["Kho nguồn kiểm tra"]<br />
B --&gt; C{"Được duyệt?"}<br />
C --&gt;|Không| D["Từ chối / điều chỉnh"]<br />
C --&gt;|Có| E["Chuẩn bị hàng tại kho nguồn"]<br />
E --&gt; F["Xác nhận xuất kho"]<br />
F --&gt; G["Hàng đang vận chuyển"]<br />
G --&gt; H["Kho đích nhận hàng"]<br />
H --&gt; I["Kiểm đếm thực nhận"]<br />
I --&gt; J{"Số lượng nhận = số lượng xuất?"}<br />
J --&gt;|Có| K["Xác nhận nhận đủ"]<br />
J --&gt;|Không| L["Lập chênh lệch và xử lý"]<br />
K --&gt; M["Kho nguồn giảm tồn / Kho đích tăng tồn"]<br />
L --&gt; M<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 17. Quản lý mua hàng

## 17.1. Quy trình mua hàng

Luồng mua hàng

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Phát sinh nhu cầu bổ sung"] --&gt; B["Kiểm tra On Hand / Reserved /
Incoming / Available"]<br />
B --&gt; C{"Có cần bổ sung?"}<br />
C --&gt;|Không| Z["Kết thúc"]<br />
C --&gt;|Có| D["Kiểm tra các kho HIM khác"]<br />
D --&gt; E{"Kho khác có Available đủ?"}<br />
E --&gt;|Không| F["Chuyển sang nhu cầu mua hàng"]<br />
E --&gt;|Có| G["Kiểm tra tồn sau điều chuyển"]<br />
G --&gt; H{"Không vi phạm mức tồn an toàn / chính sách?"}<br />
H --&gt;|Có| I["Tạo yêu cầu điều chuyển"]<br />
H --&gt;|Không| F<br />
I --&gt; J["Kho nguồn duyệt / điều chỉnh"]<br />
J --&gt; K["Xuất kho nguồn"]<br />
K --&gt; L["Kho đích nhận hàng"]<br />
L --&gt; M["Cập nhật tồn kho"]<br />
F --&gt; N["Tạo RFQ / Đơn mua hàng"]<br />
N --&gt; O["Nhà cung cấp giao"]<br />
O --&gt; P["Nhập kho"]<br />
P --&gt; M<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Control Point** | **Required Data**                 | **Owner**          |
|-------------------|-----------------------------------|--------------------|
| RFQ               | Vendor, Product, Qty, Target Date | Purchasing         |
| PO Approval       | Vendor, price, qty, terms         | Purchasing/Manager |
| Receipt           | Received Qty, condition           | Warehouse          |
| Bill              | Vendor invoice, amount, tax       | Accounting         |
| Payment           | Payment method, reference         | Accounting         |

# 18. Thiết kế chức năng POS nhà hàng

Nguyên tắc BA: sơ đồ thể hiện luồng nghiệp vụ và nhánh quyết định; bảng
chức năng dùng để chốt quyền, điều kiện, ngoại lệ và tiêu chí cấu hình.
Hai phần phải truy vết được với nhau.

## 18.1. Quản lý bàn

Sơ đồ triển khai chức năng: nên dùng sơ đồ luồng để xác định trạng thái
bàn, đơn hàng, pha chế, thanh toán và các nhánh ngoại lệ trước khi cấu
hình Odoo.

\`\`\`mermaid  
flowchart TD  
A\["Nhân viên mở POS nhà hàng"\] --\> B\["Chọn khu vực / tầng"\]  
B --\> C\["Chọn bàn đang trống"\]  
C --\> D\["Mở bàn và tạo đơn"\]  
  
D --\> E\["Thêm món"\]  
E --\> F{"Món có cần pha chế?"}  
  
F --\>\|Có\| G\["Gửi món đến quầy pha chế"\]  
F --\>\|Không\| H\["Món sẵn sàng phục vụ"\]  
  
G --\> I\["Quầy nhận món + số bàn"\]  
I --\> J\["Đang pha chế"\]  
J --\> K\["Món sẵn sàng"\]  
K --\> L\["Nhân viên phục vụ"\]  
  
H --\> L  
  
L --\> M{"Khách gọi thêm?"}  
M --\>\|Có\| E  
M --\>\|Không\| N\["Yêu cầu thanh toán"\]  
  
N --\> O\["Chọn / xác định khách hàng nếu có"\]  
O --\> P{"Có ưu đãi hợp lệ?"}  
P --\>\|Có\| Q\["Áp dụng ưu đãi theo chính sách"\]  
P --\>\|Không\| R\["Giữ nguyên giá trị đơn"\]  
  
Q --\> S\["Chọn phương thức thanh toán"\]  
R --\> S  
S --\> T\["Xác nhận thanh toán"\]  
  
T --\> U{"Thanh toán thành công?"}  
U --\>\|Không\| V\["Xử lý thanh toán lỗi / chọn lại phương thức"\]  
V --\> S  
U --\>\|Có\| W\["Đóng đơn"\]  
  
W --\> X\["Cập nhật doanh thu / thanh toán"\]  
W --\> Y\["Cập nhật tiêu hao nguyên liệu / tồn kho"\]  
W --\> Z\["Bàn trở về trạng thái trống"\]  
  
E --\> AA{"Cần hủy món?"}  
AA --\>\|Có\| AB\["Kiểm tra trạng thái món"\]  
AB --\> AC{"Đã pha chế chưa?"}  
AC --\>\|Chưa\| AD\["Hủy món theo quyền"\]  
AC --\>\|Đã pha chế\| AE\["Yêu cầu xử lý / phê duyệt ngoại lệ"\]  
AD --\> E  
AE --\> E  
\`\`\`

| **Function**   | **Expected Behavior**                          | **Open Question**                      |
|----------------|------------------------------------------------|----------------------------------------|
| Open table     | Staff selects available table                  | How are tables grouped by floor/area?  |
| Add item       | Item added to current order                    | Can customer add items multiple times? |
| Send order     | Send relevant items to preparation             | Bar screen or printer?                 |
| Transfer table | Move order to another table if needed          | Is this permitted?                     |
| Merge tables   | Combine orders/tables if supported             | Business policy?                       |
| Split bill     | Separate payment responsibility                | Needed?                                |
| Cancel item    | Cancel item with reason                        | Who can approve after preparation?     |
| Refund         | Reverse/return transaction according to policy | Which role can refund?                 |

**Luồng quyết định cấu hình và phân quyền**

\`\`\`mermaid  
flowchart LR  
A\["Mở bàn"\] --\> B{"Bàn đang trống?"}  
B --\>\|Có\| C\["Cho phép mở đơn"\]  
B --\>\|Không\| D\["Mở đơn hiện tại / xác định quyền"\]  
  
C --\> E\["Thêm món"\]  
E --\> F{"Đã gửi pha chế?"}  
F --\>\|Chưa\| G\["Cho phép sửa / xóa"\]  
F --\>\|Rồi\| H\["Kiểm tra quyền hủy / sửa"\]  
  
H --\> I{"Có quyền?"}  
I --\>\|Có\| J\["Sửa / hủy theo chính sách"\]  
I --\>\|Không\| K\["Yêu cầu quản lý phê duyệt"\]  
  
E --\> L\["Thanh toán"\]  
L --\> M{"Thanh toán thành công?"}  
M --\>\|Không\| N\["Giữ đơn mở"\]  
M --\>\|Có\| O\["Đóng đơn + giải phóng bàn"\]  
\`\`\`

## 18.2. Ví dụ giao dịch POS

| **Field**    | **Demo Value**         |
|--------------|------------------------|
| Branch       | HIM Coffee – Branch 02 |
| Table        | Table 02               |
| Customer     | Nguyễn Văn A           |
| Product      | Bạc Xỉu                |
| Qty          | 1                      |
| Unit Price   | 45,000                 |
| Payment      | Cash / Bank / Other    |
| Order Status | Closed after payment   |

# 19. Sản phẩm, định mức và giá thành

Selling Price là giá bán cho khách; Cost/COGS là chi phí/giá vốn phục vụ
mục đích quản trị và kế toán. Hai khái niệm không nên gộp thành một.

## 19.1. Ví dụ định mức pha chế

| **Ingredient**        | **Qty** | **Unit Cost** | **Extended Cost** |
|-----------------------|---------|---------------|-------------------|
| Coffee                | 18 g    | 150,000/kg    | 2,700             |
| Milk                  | 150 ml  | 20,000/litre  | 3,000             |
| Sugar                 | 10 g    | 20,000/kg     | 200               |
| Cup/Lid               | 1 set   | 1,000         | 1,000             |
| Total Direct Material | \-      | \-            | 6,900             |

Nếu có labor, machine/operation và manufacturing overhead được phân bổ,
cost framework có thể mở rộng. Không nên giả định tất cả đồ uống đều cần
Manufacturing Order; cần xác nhận cách HIM thực sự chuẩn bị và ghi nhận
consumption.

## 19.2. Khung tính giá thành

Mô hình giá thành

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart LR<br />
A["Nguyên liệu trực tiếp"] --&gt; D["Giá thành sản xuất / pha
chế"]<br />
B["Nhân công trực tiếp"] --&gt; D<br />
C["Máy móc / công đoạn"] --&gt; D<br />
E["Chi phí sản xuất chung"] --&gt; D<br />
D --&gt; F["Giá vốn / Chi phí sản phẩm"]<br />
G["Giá bán"] --&gt; H["Lợi nhuận gộp"]<br />
F --&gt; H<br />
G --&gt; H<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 20. Doanh thu, giá vốn và lợi nhuận

## 20.1. Định nghĩa doanh thu

Luồng doanh thu

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Giao dịch POS / Đơn trực tuyến"] --&gt; B["Tổng doanh thu bán
hàng"]<br />
B --&gt; C["Trừ chiết khấu hợp lệ"]<br />
C --&gt; D["Trừ hoàn tiền / hủy theo chính sách"]<br />
D --&gt; E["Doanh thu thuần"]<br />
E --&gt; F["Đối soát thanh toán"]<br />
F --&gt; G["Ghi nhận kế toán"]<br />
E --&gt; H["Báo cáo doanh thu"]<br />
E --&gt; I["Trừ giá vốn"]<br />
I --&gt; J["Lợi nhuận gộp"]<br />
J --&gt; K["Trừ chi phí hoạt động"]<br />
K --&gt; L["Lợi nhuận hoạt động"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 20.2. Công thức lợi nhuận

| **Metric**         | **Formula**                                                         |
|--------------------|---------------------------------------------------------------------|
| Gross Sales        | Sum of sales before deductions                                      |
| Net Revenue        | Gross Sales – Discounts – Returns/Refunds (per reporting policy)    |
| COGS               | Cost of consumed/sold products under chosen costing model           |
| Gross Profit       | Net Revenue – COGS                                                  |
| Operating Expenses | Payroll + Rent + Utilities + Marketing + Platform Fees + Other OPEX |
| Operating Profit   | Gross Profit – Operating Expenses                                   |

## 20.3. Ví dụ theo cơ sở

| **Metric**       | **Branch 02 Demo** |
|------------------|--------------------|
| Gross Sales      | 120,000,000        |
| Discounts        | 5,000,000          |
| Refunds          | 1,000,000          |
| Net Revenue      | 114,000,000        |
| COGS             | 34,200,000         |
| Gross Profit     | 79,800,000         |
| Payroll          | 25,000,000         |
| Rent             | 12,000,000         |
| Utilities        | 4,000,000          |
| Marketing        | 3,000,000          |
| Other OPEX       | 2,000,000          |
| Operating Profit | 33,800,000         |

Số liệu trên chỉ là demo để kiểm thử công thức và dashboard, không phải
số liệu thực của HIM.

# 21. Nhân sự và tiền lương

## 21.1. Vòng đời nhân viên

Vòng đời nhân viên

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Tuyển dụng / Tiếp nhận"] --&gt; B["Hồ sơ nhân viên"]<br />
B --&gt; C["Cơ sở / Bộ phận / Chức danh"]<br />
C --&gt; D["Hợp đồng lao động"]<br />
D --&gt; E["Lịch làm việc / Ca"]<br />
E --&gt; F["Chấm công / Nghỉ phép"]<br />
F --&gt; G["Làm thêm giờ / Phụ cấp / Thưởng / Khấu trừ"]<br />
G --&gt; H["Tính lương"]<br />
H --&gt; I["Kiểm tra / Phê duyệt"]<br />
I --&gt; J["Phiếu lương"]<br />
J --&gt; K["Thanh toán / Ghi nhận kế toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 21.2. Dữ liệu đầu vào tính lương

| **Input**         | **Source**          | **Example**          |
|-------------------|---------------------|----------------------|
| Base Salary       | Contract            | 7,000,000            |
| Worked Days/Hours | Attendance          | 26 days              |
| OT Hours          | Approved OT         | 12 hours             |
| Allowance         | Policy              | 500,000              |
| Bonus             | Manager/Policy      | 300,000              |
| Deduction         | Policy/Attendance   | 200,000              |
| Insurance/Tax     | Legal configuration | Configured by period |

## 21.3. Khung công thức tính lương

Công thức tính lương

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Lương cơ bản / Lương theo giờ"] --&gt; E["Tổng thu nhập"]<br />
B["Tiền làm thêm giờ"] --&gt; E<br />
C["Phụ cấp"] --&gt; E<br />
D["Thưởng"] --&gt; E<br />
E --&gt; F["Trừ các khoản khấu trừ"]<br />
F --&gt; G["Thu nhập sau khấu trừ"]<br />
G --&gt; H["Trừ BHXH / BHYT / BHTN theo cấu hình pháp lý"]<br />
H --&gt; I["Trừ thuế TNCN theo cấu hình pháp lý"]<br />
I --&gt; J["Trừ các khoản khác được phê duyệt"]<br />
J --&gt; K["Lương thực nhận"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

Tỷ lệ BHXH/BHYT/BHTN, PIT và các mức giảm trừ phải được cấu hình theo
quy định pháp luật và kỳ áp dụng thực tế. Tài liệu này không hard-code
tỷ lệ pháp lý để tránh làm sai khi luật thay đổi.

## 21.4. Từ chấm công đến tính lương

| **Step** | **Input**           | **Output**            |
|----------|---------------------|-----------------------|
| 1        | Check-in/out        | Attendance record     |
| 2        | Compute hours       | Worked hours          |
| 3        | Apply schedule      | Regular vs late/early |
| 4        | Approve OT          | OT hours              |
| 5        | Add allowance/bonus | Payroll inputs        |
| 6        | Apply deduction     | Deduction lines       |
| 7        | Calculate           | Gross/Net             |
| 8        | Approve             | Payslip               |
| 9        | Post/pay            | Accounting/payment    |

# 22. CRM và bán hàng doanh nghiệp

CRM không phải trung tâm của toàn bộ ERP. CRM chủ yếu có giá trị khi HIM
có khách doanh nghiệp, đơn số lượng lớn, hợp đồng cung cấp định kỳ hoặc
cơ hội cần follow-up.

## 22.1. Quy trình cơ hội khách hàng doanh nghiệp

Quy trình cơ hội khách hàng doanh nghiệp

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart LR<br />
A["MỚI"] --&gt; B["XÁC THỰC"]<br />
B --&gt; C["PHÂN TÍCH NHU CẦU"]<br />
C --&gt; D["ĐỀ XUẤT / BÁO GIÁ"]<br />
D --&gt; E["ĐÀM PHÁN"]<br />
E --&gt; F["ĐÃ CHỐT"]<br />
A --&gt; X["KHÔNG THÀNH CÔNG"]<br />
B --&gt; X<br />
C --&gt; X<br />
D --&gt; X<br />
E --&gt; X<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Stage**      | **Meaning**                    | **Exit Criteria**                            |
|----------------|--------------------------------|----------------------------------------------|
| NEW            | Cơ hội mới                     | Có đủ thông tin cơ bản để qualification      |
| QUALIFICATION  | Xác thực khách hàng và nhu cầu | Có nhu cầu thật + contact + expected value   |
| NEEDS ANALYSIS | Phân tích nhu cầu              | Biết sản phẩm, qty, timing, location, budget |
| PROPOSAL       | Đề xuất/báo giá                | Đã gửi phương án/báo giá                     |
| NEGOTIATION    | Đàm phán                       | Đã xác định điều kiện chốt                   |
| WON            | Đã chốt                        | Giao dịch được xác nhận                      |
| LOST           | Không thành công               | Có Lost Reason                               |

Stage Requirements trong Odoo nên được hiểu là checklist/guidance theo
stage, không mặc định là validation cứng. Nếu HIM muốn không cho chuyển
stage khi thiếu điều kiện, cần Business Rule + Functional Requirement
riêng.

# 23. Vai trò và phân quyền

| **Role**        | **POS**         | **Inventory**  | **Purchase**    | **Accounting**          | **HR**             | **CRM**  | **Branch Scope** |
|-----------------|-----------------|----------------|-----------------|-------------------------|--------------------|----------|------------------|
| Owner/Director  | View            | View           | View            | View                    | View               | View     | All              |
| Store Manager   | Operate/Approve | Manage         | Request/Approve | View                    | View               | Optional | Own Branch       |
| Cashier/Service | Operate         | View limited   | No              | Payment only            | No                 | Optional | Own Branch       |
| Barista         | Preparation     | Limited        | No              | No                      | No                 | No       | Own Branch       |
| Warehouse Staff | No/limited      | Operate        | Receive         | No                      | No                 | No       | Own Branch       |
| Purchasing      | No              | View           | Manage          | Vendor bill handoff     | No                 | No       | All relevant     |
| Accountant      | Payment view    | Valuation view | Bill view       | Manage                  | Payroll accounting | No       | All              |
| HR              | No              | No             | No              | Payroll posting handoff | Manage             | No       | All              |
| CRM/Sales       | No/limited      | View           | No              | No                      | No                 | Manage   | All/assigned     |
| System Admin    | Admin           | Admin          | Admin           | Admin                   | Admin              | Admin    | All              |

# 24. Dashboard và yêu cầu chỉ số KPI

| **KPI ID** | **KPI**            | **Definition**                         | **Dimension**           |
|------------|--------------------|----------------------------------------|-------------------------|
| KP-001     | Gross Sales        | Tổng sales trước deductions            | Date/Branch/POS/Product |
| KP-002     | Net Revenue        | Gross Sales sau deductions theo policy | Date/Branch             |
| KP-003     | COGS               | Giá vốn theo costing model             | Branch/Product          |
| KP-004     | Gross Profit       | Net Revenue - COGS                     | Branch/Period           |
| KP-005     | Operating Profit   | Gross Profit - OPEX                    | Branch/Period           |
| KP-006     | AOV                | Net Sales / Number of Orders           | Branch/Period           |
| KP-007     | Stockout           | Số item hết hàng                       | Branch/Product          |
| KP-008     | Inventory Value    | Giá trị tồn kho                        | Branch/Category         |
| KP-009     | Transfer Volume    | Qty/value transferred                  | From/To Branch          |
| KP-010     | Labor Cost         | Payroll cost                           | Branch/Period           |
| KP-011     | OT Hours           | Approved overtime                      | Employee/Branch         |
| KP-012     | Customer Count     | Unique customers                       | Branch/Period           |
| KP-013     | B2B Pipeline Value | Expected revenue                       | Stage/Salesperson       |

## 24.1. Bố cục Dashboard

**Management Dashboard**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>TOP CARDS:</p>
<p>Revenue | Net Revenue | COGS | Gross Profit | OPEX | Operating
Profit</p>
<p>SALES:</p>
<p>Revenue by Branch</p>
<p>Revenue by Day</p>
<p>AOV</p>
<p>Top Products</p>
<p>INVENTORY:</p>
<p>Low Stock</p>
<p>Stock Value</p>
<p>Pending Transfers</p>
<p>Pending Receipts</p>
<p>PEOPLE:</p>
<p>Headcount</p>
<p>Attendance</p>
<p>OT Hours</p>
<p>Payroll Cost</p>
<p>CRM:</p>
<p>Open Opportunities</p>
<p>Pipeline Value</p>
<p>Activities Due</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 25. UAT / Các ca kiểm thử chấp nhận người dùng

UAT phải kiểm tra nghiệp vụ đầu-cuối, không chỉ kiểm tra màn hình. Một
test case đạt khi kết quả hệ thống đáp ứng Acceptance Criteria và dữ
liệu liên kết sang module tiếp theo đúng.

| **Mã kiểm thử** | **Mã yêu cầu** | **Kịch bản kiểm thử** | **Điều kiện trước kiểm thử** | **Các bước thực hiện**                 | **Kết quả mong đợi**                 |
|-----------------|----------------|-----------------------|------------------------------|----------------------------------------|--------------------------------------|
| TC-POS-001      | FR-POS-001     | Create table order    | Bàn đang trống               | Mở Bàn 02 → thêm món                   | Order linked to Table 02             |
| TC-POS-002      | FR-POS-002     | Add product qty       | Đơn đang mở                  | Thêm Bạc Xỉu x2                        | Qty=2 and amount calculated          |
| TC-POS-003      | FR-POS-003     | Send preparation      | Order contains item          | Gửi món                                | Preparation receives item            |
| TC-POS-004      | FR-POS-005     | Payment               | Đơn sẵn sàng thanh toán      | Chọn phương thức thanh toán → xác nhận | Payment registered                   |
| TC-POS-005      | FR-POS-006     | Đóng đơn              | Thanh toán thành công        | Đóng đơn                               | Order closed/table released          |
| TC-INV-001      | FR-INV-001     | View branch stock     | Kho đã cấu hình              | Mở báo cáo tồn kho                     | Hiển thị đúng tồn kho cơ sở          |
| TC-INV-002      | FR-INV-003     | Create transfer       | Destination needs stock      | Tạo yêu cầu B→A                        | Yêu cầu được lưu                     |
| TC-INV-003      | FR-INV-004     | Validate source stock | Có yêu cầu điều chuyển       | Kiểm tra kho nguồn                     | Hiển thị Available để ra quyết định  |
| TC-INV-004      | FR-INV-005     | Receive transfer      | Có phiếu xuất                | Xác nhận nhận hàng                     | Tồn kho đích tăng                    |
| TC-INV-005      | BRULE-INV-005  | Quantity discrepancy  | Shipped \> received          | Nhập số lượng thực nhận thấp hơn       | Ghi nhận chênh lệch và ngoại lệ      |
| TC-PUR-001      | FR-PUR-001     | Create PO             | Vendor/product exists        | Tạo RFQ → PO                           | PO được tạo                          |
| TC-PUR-002      | FR-PUR-002     | Receive purchase      | PO đã xác nhận               | Xác nhận số lượng nhận                 | Tồn kho tăng                         |
| TC-PUR-003      | FR-PUR-003     | Vendor bill           | Đã hoàn tất nhập hàng        | Tạo hóa đơn                            | Hóa đơn sẵn sàng cho kế toán         |
| TC-HR-001       | FR-HR-001      | Tạo hồ sơ nhân viên   | User has HR access           | Tạo hồ sơ nhân viên                    | Hồ sơ nhân viên được lưu             |
| TC-HR-002       | FR-HR-002      | Attendance            | Nhân viên đang hoạt động     | Chấm công vào/ra                       | Ghi nhận chấm công                   |
| TC-HR-003       | FR-HR-003      | Payroll input         | Chấm công đã duyệt           | Tạo dữ liệu đầu vào tính lương         | Giờ công/OT được phản ánh            |
| TC-HR-004       | FR-HR-004      | Payslip               | Dữ liệu đầu vào đã duyệt     | Tạo phiếu lương                        | Tính được Gross/khấu trừ/Net         |
| TC-ACC-001      | FR-ACC-001     | Revenue report        | Có giao dịch POS             | Chạy báo cáo ngày                      | Tổng số liệu đối soát được           |
| TC-ACC-002      | FR-ACC-002     | COGS report           | Có dữ liệu giá vốn           | Chạy báo cáo                           | COGS được tính theo mô hình          |
| TC-CRM-001      | FR-CRM-001     | Tạo cơ hội            | Có khách hàng B2B            | Tạo cơ hội                             | Cơ hội xuất hiện ở NEW               |
| TC-CRM-002      | FR-CRM-001     | Move pipeline         | Có cơ hội                    | Chuyển qua các giai đoạn               | Lịch sử giai đoạn/hoạt động được lưu |

## 25.1. Tiêu chí chấp nhận UAT

- Critical flow POS → Payment → Revenue phải pass.

- Critical inventory flow Transfer/Purchase → Receipt → Stock phải pass.

- Payroll phải reconcile với approved attendance/input data.

- Revenue dashboard phải reconcile với source transactions trong test
  period.

- Permission test phải chứng minh user không thấy/chỉnh sửa dữ liệu
  ngoài scope.

- Defect Severity Critical/High phải được xử lý trước Go-Live theo
  agreed acceptance policy.

# 26. Ma trận truy vết yêu cầu (RTM)

| **BR**     | **FR**             | **Business Rule** | **UC**         | **Odoo Solution**    | **UAT**            |
|------------|--------------------|-------------------|----------------|----------------------|--------------------|
| BR-POS-001 | FR-POS-001/002/006 | BRULE-POS-001/002 | UC-POS-001/002 | Restaurant POS       | TC-POS-001/002/005 |
| BR-POS-002 | FR-POS-003/004     | BRULE-POS-001     | UC-POS-003     | POS Preparation      | TC-POS-003         |
| BR-INV-001 | FR-INV-001/002     | BRULE-INV-001     | UC-INV-001     | Inventory            | TC-INV-001         |
| BR-INV-002 | FR-INV-004         | BRULE-INV-002/003 | UC-INV-002     | Inventory + Approval | TC-INV-003         |
| BR-INV-003 | FR-INV-003/005     | BRULE-INV-004/005 | UC-INV-001/003 | Internal Transfer    | TC-INV-002/004/005 |
| BR-PUR-001 | FR-PUR-001/002/003 | BRULE-PUR-001/002 | UC-PUR-001     | Purchase             | TC-PUR-001/002/003 |
| BR-HR-002  | FR-HR-002/003      | BRULE-HR-001/002  | UC-HR-001/002  | Attendances/Payroll  | TC-HR-002/003      |
| BR-ACC-001 | FR-ACC-001         | BRULE-ACC-001     | UC-ACC-001     | POS/Accounting       | TC-ACC-001         |
| BR-CRM-001 | FR-CRM-001         | BRULE-CRM-001     | UC-CRM-001     | CRM                  | TC-CRM-001/002     |

# 27. Yêu cầu thay đổi (CR)

| **CR ID** | **Change**                     | **Reason**                 | **Impact**                | **Decision**       |
|-----------|--------------------------------|----------------------------|---------------------------|--------------------|
| CR-001    | Add transfer approval chain    | Control inter-branch stock | Inventory workflow, roles | Pending validation |
| CR-002    | Add split bill                 | Customer payment scenario  | POS/UI/UAT                | Pending            |
| CR-003    | Integrate online order channel | Digital sales              | API, store routing, stock | Pending            |
| CR-004    | Advanced branch profitability  | Management reporting       | Accounting/analytic model | Pending            |
| CR-005    | Automated loyalty              | Retention                  | CRM/POS/promotion         | Pending            |

## 27.1. Quy trình xử lý yêu cầu thay đổi

**Change Control**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Phát sinh yêu cầu thay đổi"] --&gt; B["Phân tích tác động"]<br />
B --&gt; C{"Có được phê duyệt?"}<br />
C --&gt;|Không| D["Từ chối / Đóng yêu cầu"]<br />
C --&gt;|Có| E["BA cập nhật đặc tả"]<br />
E --&gt; F["Cấu hình / Phát triển"]<br />
F --&gt; G["Kiểm thử"]<br />
G --&gt; H{"Đạt UAT?"}<br />
H --&gt;|Không| F<br />
H --&gt;|Có| I["Triển khai / Cập nhật tài liệu"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 28. Chuyển đổi và chất lượng dữ liệu

| **Data Set**  | **Source**        | **Target**                    | **Validation**          |
|---------------|-------------------|-------------------------------|-------------------------|
| Branches      | Existing list     | Odoo Branch/Company structure | Unique code/address     |
| Warehouses    | Stock records     | Inventory                     | Opening qty/value       |
| Products      | Product master    | Products                      | SKU/name/UoM/category   |
| Ingredients   | Recipe list       | Products + BOM/recipe         | Qty/UoM                 |
| Vendors       | Supplier list     | Contacts/Vendors              | Tax/bank/contact        |
| Customers     | Customer database | Contacts                      | Duplicate check         |
| Employees     | HR file           | Employees                     | Employee ID/branch      |
| Opening Stock | Stock count       | Inventory adjustment          | Physical reconciliation |

## 28.1. Quy tắc chất lượng dữ liệu

- Không trùng Product SKU.

- Customer duplicate phải được phát hiện trước migration.

- UoM phải thống nhất giữa Purchase, Stock và Recipe.

- Opening stock phải có người chịu trách nhiệm xác nhận.

- Employee phải gắn đúng branch/department/job.

- Opening balances phải reconcile với accounting.

# 29. Lộ trình triển khai

| **Phase** | **Focus**          | **Deliverables**                                     |
|-----------|--------------------|------------------------------------------------------|
| Phase 1   | Discovery          | AS-IS, requirements, open questions                  |
| Phase 2   | Master Data        | Branch, warehouse, products, UoM, vendors, customers |
| Phase 3   | POS                | Tables, products, preparation, payment               |
| Phase 4   | Inventory/Purchase | Stock, transfer, replenishment, PO                   |
| Phase 5   | Accounting         | Payment, revenue, COGS, vendor bills                 |
| Phase 6   | HR                 | Employee, attendance, time off, payroll              |
| Phase 7   | CRM                | B2B pipeline, activities, quotation                  |
| Phase 8   | Reporting          | Dashboard/KPI                                        |
| Phase 9   | Testing            | SIT, UAT, defect fixing                              |
| Phase 10  | Go-Live            | Migration, training, cutover, hypercare              |

# 30. Rủi ro, giả định và câu hỏi cần xác nhận

| **Risk** | **Impact**                   | **Mitigation**   |
|----------|------------------------------|------------------|
| R-001    | Sai mô hình branch/warehouse | Stock/report sai |

# 30. Rủi ro, giả định và câu hỏi cần xác nhận

## 30.1. Rủi ro

| **Risk** | **Impact**                        | **Mitigation**                 | **Field 4**                       |
|----------|-----------------------------------|--------------------------------|-----------------------------------|
| R-001    | Sai mô hình branch/warehouse      | Stock/report sai               | Validate physical operating model |
| R-002    | Không có recipe/consumption chuẩn | COGS sai                       | Define recipe/UoM                 |
| R-003    | Approval không rõ                 | Transfer/purchase uncontrolled | Define authority matrix           |
| R-004    | Attendance không chính xác        | Payroll sai                    | Attendance policy + approval      |
| R-005    | Online integration thiếu spec     | Order không route đúng         | Integration workshop              |
| R-006    | Custom quá sớm                    | Chi phí bảo trì                | Standard-first                    |

## 30.2. Câu hỏi cần xác nhận

| **ID** | **Open Question**                                                     |
|--------|-----------------------------------------------------------------------|
| Q-001  | HIM dùng màn hình/bar printer hay phương thức nào để nhận order?      |
| Q-002  | Có cần transfer table, merge table, split bill không?                 |
| Q-003  | Ai được cancel/refund sau khi món đã bắt đầu pha?                     |
| Q-004  | Khi kho A thiếu, B/C được ưu tiên theo rule nào?                      |
| Q-005  | Có Safety Stock/Min Stock chính thức cho từng nguyên liệu không?      |
| Q-006  | Có central purchasing nhưng branch receiving hay mỗi branch tự mua?   |
| Q-007  | Recipe/định lượng được quản lý ở đâu và ai chịu trách nhiệm cập nhật? |
| Q-008  | HIM có tạo thành phẩm trước hay pha chế theo order?                   |
| Q-009  | Có online/app/third-party order không? Nếu có, nguồn nào?             |
| Q-010  | Chính sách discount/refund/loyalty hiện tại là gì?                    |
| Q-011  | Payroll full-time/part-time được tính theo rule nào?                  |
| Q-012  | OT cần ai phê duyệt?                                                  |
| Q-013  | Doanh thu được ghi nhận theo branch/POS/payment method như thế nào?   |
| Q-014  | COGS dùng standard cost, average cost hay phương pháp khác?           |
| Q-015  | Branch profitability cần theo analytic account nào?                   |

# 31. Danh mục sơ đồ để tự vẽ

| **Diagram ID** | **Diagram**             | **Main Content**                                                   |
|----------------|-------------------------|--------------------------------------------------------------------|
| D-001          | ERP End-to-End          | Business → POS/Online → Inventory → Purchase/Transfer → Accounting |
| D-002          | Restaurant POS          | Table → Order → Preparation → Serve → Payment                      |
| D-003          | Online Order            | App → Odoo → Branch → Stock → Preparation → Delivery               |
| D-004          | Inventory Replenishment | Low Stock → Source Check → Transfer/Purchase                       |
| D-005          | Internal Transfer       | Request → Review → Approve → Ship → Receive                        |
| D-006          | Purchase                | Need → RFQ → PO → Receipt → Bill → Payment                         |
| D-007          | Product Costing         | Recipe → Consumption → COGS → Margin                               |
| D-008          | Payroll                 | Employee → Attendance → OT → Payslip → Payment                     |
| D-009          | Revenue                 | POS → Gross → Deductions → Net → Accounting                        |
| D-010          | Profitability           | Revenue → COGS → Gross Profit → OPEX → Operating Profit            |
| D-011          | CRM                     | New → Qualification → Needs → Proposal → Negotiation → Won/Lost    |
| D-012          | Data Model              | Branch/Product/Order/Stock/Purchase/Employee/Accounting            |
| D-013          | UAT Lifecycle           | Requirement → Test → Defect → Retest → Acceptance                  |
| D-014          | Access Control          | Role → Module → Branch Scope                                       |

# 32. Thuật ngữ

| **Term**     | **Meaning**                                             |
|--------------|---------------------------------------------------------|
| AS-IS        | Quy trình hiện tại                                      |
| TO-BE        | Quy trình đề xuất                                       |
| BR           | Business Requirement – Yêu cầu nghiệp vụ                |
| FR           | Functional Requirement – Yêu cầu chức năng              |
| NFR          | Non-Functional Requirement – Yêu cầu phi chức năng      |
| BRULE        | Business Rule – Quy tắc nghiệp vụ                       |
| UC           | Use Case – Kịch bản sử dụng                             |
| UAT          | User Acceptance Testing – Kiểm thử chấp nhận người dùng |
| RTM          | Requirement Traceability Matrix – Ma trận truy vết      |
| POS          | Point of Sale – Điểm bán hàng                           |
| COGS         | Cost of Goods Sold – Giá vốn hàng bán                   |
| OPEX         | Operating Expenses – Chi phí vận hành                   |
| AOV          | Average Order Value – Giá trị đơn hàng trung bình       |
| RFQ          | Request for Quotation – Yêu cầu báo giá                 |
| PO           | Purchase Order – Đơn mua hàng                           |
| BOM          | Bill of Materials – Định mức nguyên vật liệu            |
| SKU          | Stock Keeping Unit – Mã quản lý sản phẩm                |
| OT           | Overtime – Làm thêm giờ                                 |
| Gross        | Tổng trước khấu trừ                                     |
| Net          | Giá trị sau khấu trừ                                    |
| Safety Stock | Tồn kho an toàn                                         |
| Available    | Tồn có thể sử dụng/đáp ứng                              |

# 33. Kết luận và Checklist bàn giao BA

Bộ tài liệu này được thiết kế như baseline để tiếp tục discovery và cấu
hình Odoo. Trước Go-Live, BA cần biến các Assumption/Open Question thành
confirmed requirements, sau đó cập nhật FR, Business Rules, UAT và RTM.

| **Deliverable**         | **Status for Review**              |
|-------------------------|------------------------------------|
| Business Context        | Draft – validate                   |
| AS-IS                   | Working model – interview required |
| Business Requirements   | Draft baseline                     |
| Functional Requirements | Draft baseline                     |
| Business Rules          | Proposed rules clearly marked      |
| TO-BE                   | Proposed solution                  |
| Odoo Mapping            | Standard-first baseline            |
| Data Model              | Logical model                      |
| UAT                     | Initial test suite                 |
| RTM                     | Initial traceability               |
| Open Questions          | Workshop required                  |
| Go-Live Readiness       | Not yet assessed                   |

## Final BA Principle

**Business → Process → Problem → Requirement → Rule → Odoo Solution →
Configuration → Test/UAT → Measurement**

**QUY ƯỚC TÊN MỤC / BẢNG (Tên tiếng Anh – Nghĩa tiếng Việt)**

| **Thuật ngữ**                         | **Nghĩa tiếng Việt**                        |
|---------------------------------------|---------------------------------------------|
| Project Overview                      |                                             |
|                                       | Tổng quan dự án                             |
| Business Context                      |                                             |
|                                       | Bối cảnh nghiệp vụ                          |
| Stakeholder Analysis                  |                                             |
|                                       | Phân tích các bên liên quan                 |
| Scope                                 |                                             |
|                                       | Phạm vi                                     |
| AS-IS Process                         |                                             |
|                                       | Quy trình hiện tại                          |
| Pain Points                           |                                             |
|                                       | Vấn đề / điểm đau                           |
| Business Requirements                 |                                             |
|                                       | Yêu cầu nghiệp vụ                           |
| Functional Requirements               |                                             |
|                                       | Yêu cầu chức năng                           |
| Non-Functional Requirements           |                                             |
|                                       | Yêu cầu phi chức năng                       |
| Business Rules                        |                                             |
|                                       | Quy tắc nghiệp vụ                           |
| Use Cases                             |                                             |
|                                       | Kịch bản sử dụng                            |
| TO-BE Process                         |                                             |
|                                       | Quy trình đề xuất                           |
| Gap Analysis                          |                                             |
|                                       | Phân tích khoảng cách                       |
| Odoo Solution Mapping                 |                                             |
|                                       | Ánh xạ giải pháp Odoo                       |
| Data Model                            |                                             |
|                                       | Mô hình dữ liệu                             |
| UAT / Test Cases                      |                                             |
|                                       | Kiểm thử chấp nhận người dùng / Ca kiểm thử |
| Dashboard & KPI                       |                                             |
|                                       | Bảng điều khiển & Chỉ số đo lường           |
| Change Request                        |                                             |
|                                       | Yêu cầu thay đổi                            |
| Requirement Traceability Matrix – RTM |                                             |
|                                       | Ma trận truy vết yêu cầu                    |
| Assumptions / Risks / Open Questions  |                                             |
|                                       | Giả định / Rủi ro / Câu hỏi mở              |
| Implementation Roadmap                |                                             |
|                                       | Lộ trình triển khai                         |
| Glossary                              |                                             |
|                                       | Từ điển thuật ngữ                           |

# 16A. Quy trình kho

Phần kho được tách thành các luồng độc lập để tránh nhầm giữa 'nhập hàng
vào kho', 'HIM nhận hàng', và 'HIM xuất hàng'. Với mô hình HIM không có
kho trung tâm, mỗi cơ sở/kho phải xác định rõ nguồn và đích của từng
giao dịch.

## 16A.1. Quy trình nhập kho từ nhà cung cấp

**D-INV-001 – Mermaid: Quy trình nhập kho từ nhà cung cấp**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Nhu cầu bổ sung nguyên liệu"] --&gt; B["Kiểm tra tồn kho và nguồn nội
bộ"]<br />
B --&gt; C{"Kho nội bộ có đủ?"}<br />
C --&gt;|Có| D["Tạo yêu cầu điều chuyển nội bộ"]<br />
C --&gt;|Không| E["Tạo yêu cầu báo giá"]<br />
E --&gt; F["Chọn nhà cung cấp"]<br />
F --&gt; G["Tạo đơn mua hàng"]<br />
G --&gt; H{"Đơn mua được phê duyệt?"}<br />
H --&gt;|Không| G<br />
H --&gt;|Có| I["Nhà cung cấp giao hàng"]<br />
I --&gt; J["Kho HIM nhận hàng"]<br />
J --&gt; K["Kiểm đếm số lượng / chất lượng"]<br />
K --&gt; L{"Hàng đạt yêu cầu?"}<br />
L --&gt;|Không| M["Lập chênh lệch / trả hàng / xử lý ngoại lệ"]<br />
L --&gt;|Có| N["Xác nhận nhập kho"]<br />
N --&gt; O["Tăng tồn kho"]<br />
O --&gt; P["Đối chiếu đơn mua - phiếu nhập - hóa đơn"]<br />
P --&gt; Q["Kế toán ghi nhận công nợ"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Bước** | **Thao tác**          | **Dữ liệu cần ghi nhận**               | **Người thực hiện**       | **Kết quả**                       |
|----------|-----------------------|----------------------------------------|---------------------------|-----------------------------------|
| 1        |                       |                                        |                           |                                   |
|          | Xác định nhu cầu      |                                        |                           |                                   |
|          |                       | Sản phẩm, số lượng, cơ sở              |                           |                                   |
|          |                       |                                        | Quản lý kho/Store Manager |                                   |
|          |                       |                                        |                           | Replenishment Need                |
| 2        |                       |                                        |                           |                                   |
|          | Kiểm tra nguồn nội bộ |                                        |                           |                                   |
|          |                       | On Hand, Reserved, Available, Incoming |                           |                                   |
|          |                       |                                        | Kho                       |                                   |
|          |                       |                                        |                           | Quyết định transfer hoặc purchase |
| 3        |                       |                                        |                           |                                   |
|          | Tạo RFQ/PO            |                                        |                           |                                   |
|          |                       | Vendor, SKU, Qty, Price, Date          |                           |                                   |
|          |                       |                                        | Purchasing                |                                   |
|          |                       |                                        |                           | PO được phê duyệt                 |
| 4        |                       |                                        |                           |                                   |
|          | HIM nhận hàng         |                                        |                           |                                   |
|          |                       | PO, thực nhận, tình trạng hàng         |                           |                                   |
|          |                       |                                        | Kho cơ sở                 |                                   |
|          |                       |                                        |                           | Hàng được kiểm tra                |
| 5        |                       |                                        |                           |                                   |
|          | Xác nhận nhập         |                                        |                           |                                   |
|          |                       | Received Qty, Location                 |                           |                                   |
|          |                       |                                        | Kho                       |                                   |
|          |                       |                                        |                           | Stock tăng                        |
| 6        |                       |                                        |                           |                                   |
|          | Đối chiếu             |                                        |                           |                                   |
|          |                       | PO/Receipt/Bill                        |                           |                                   |
|          |                       |                                        | Kế toán                   |                                   |
|          |                       |                                        |                           | Công nợ hợp lệ                    |

## 16A.2. Quy trình kho HIM nhận hàng

**D-INV-002 – Mermaid: HIM nhận hàng**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Hàng đến kho HIM"] --&gt; B["Kiểm tra đơn mua / điều chuyển / chứng
từ"]<br />
B --&gt; C{"Nguồn giao hàng?"}<br />
C --&gt;|Nhà cung cấp| D["Đối chiếu đơn mua"]<br />
C --&gt;|Kho HIM khác| E["Đối chiếu phiếu điều chuyển"]<br />
D --&gt; F["Kiểm đếm thực tế"]<br />
E --&gt; F<br />
F --&gt; G["Kiểm tra sản phẩm / quy cách / hạn sử dụng nếu có"]<br />
G --&gt; H{"Số lượng thực nhận khớp?"}<br />
H --&gt;|Có| I["Xác nhận nhận đủ"]<br />
H --&gt;|Không| J["Ghi nhận chênh lệch"]<br />
J --&gt; K["Xác định nguyên nhân và xử lý theo chính sách"]<br />
I --&gt; L["Đưa hàng vào vị trí kho"]<br />
K --&gt; L<br />
L --&gt; M["Xác nhận nhập kho"]<br />
M --&gt; N["Cập nhật tồn kho"]<br />
N --&gt; O["Hoàn tất giao dịch nhận hàng"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 16A.3. Quy trình kho HIM xuất hàng

**D-INV-003 – Mermaid: HIM xuất hàng**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Phát sinh nhu cầu xuất kho"] --&gt; B{"Mục đích xuất?"}<br />
B --&gt;|Bổ sung cho cơ sở khác| C["Điều chuyển nội bộ"]<br />
B --&gt;|Bán / giao khách| D["Bán hàng / giao hàng"]<br />
B --&gt;|Pha chế / tiêu hao| E["Tiêu hao theo định mức"]<br />
B --&gt;|Hủy / hao hụt| F["Hủy hàng / điều chỉnh tồn"]<br />
C --&gt; G["Kiểm tra Available tại kho xuất"]<br />
D --&gt; G<br />
E --&gt; G<br />
F --&gt; G<br />
G --&gt; H{"Đủ hàng?"}<br />
H --&gt;|Không| I["Tạo nhu cầu bổ sung / xử lý thiếu hụt"]<br />
H --&gt;|Có| J["Tạo phiếu xuất / dịch chuyển tồn"]<br />
J --&gt; K["Kiểm đếm và chuẩn bị hàng"]<br />
K --&gt; L["Xác nhận xuất kho"]<br />
L --&gt; M["Giảm tồn kho tại kho xuất"]<br />
M --&gt; N{"Có kho đích?"}<br />
N --&gt;|Có| O["Hàng đang vận chuyển"]<br />
O --&gt; P["Kho đích xác nhận nhận"]<br />
N --&gt;|Không| Q["Hoàn tất xuất / tiêu hao"]<br />
P --&gt; R["Tăng tồn kho tại kho đích"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 16A.4. Quy trình điều chuyển giữa các kho HIM

**D-INV-004 – Mermaid: Điều chuyển kho**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Kho A thiếu nguyên liệu"] --&gt; B["Kiểm tra mức tồn tối thiểu / nhu
cầu"]<br />
B --&gt; C["Kiểm tra kho B và C: On Hand / Reserved / Available /
Incoming"]<br />
C --&gt; D{"Có kho nội bộ đáp ứng?"}<br />
D --&gt;|Không| E["Chuyển sang mua hàng"]<br />
D --&gt;|Có| F["Tạo yêu cầu điều chuyển"]<br />
F --&gt; G["Kho nguồn kiểm tra khả năng cấp"]<br />
G --&gt; H{"Sau điều chuyển còn đủ tồn an toàn?"}<br />
H --&gt;|Không| I["Điều chỉnh số lượng / từ chối / xin duyệt ngoại
lệ"]<br />
H --&gt;|Có| J["Phê duyệt điều chuyển"]<br />
J --&gt; K["Kho nguồn xuất hàng"]<br />
K --&gt; L["Hàng đang vận chuyển"]<br />
L --&gt; M["Kho đích nhận hàng"]<br />
M --&gt; N["Kiểm đếm thực nhận"]<br />
N --&gt; O["Xác nhận nhập kho"]<br />
O --&gt; P["Kho nguồn giảm tồn / kho đích tăng tồn"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Chỉ số**              | **Công thức / Ý nghĩa**                                                   |
|-------------------------|---------------------------------------------------------------------------|
| On Hand                 |                                                                           |
|                         | Tồn thực tế đang ghi nhận tại kho.                                        |
| Reserved                |                                                                           |
|                         | Số lượng đã được giữ cho nhu cầu khác.                                    |
| Available               |                                                                           |
|                         | Available = On Hand - Reserved + các yếu tố được Odoo tính theo cấu hình. |
| Projected Stock         |                                                                           |
|                         | Tồn dự kiến sau khi tính Incoming/Outgoing theo mô hình hoạch định.       |
| Safety Stock            |                                                                           |
|                         | Mức tồn tối thiểu để bảo vệ hoạt động; phải được HIM phê duyệt.           |
| Post-transfer Available |                                                                           |
|                         | Available của kho nguồn sau khi trừ lượng dự kiến điều chuyển.            |

# 20A. Công thức doanh thu và tiền lương

## 20A.1. Công thức tính doanh thu

Để tránh nhầm giữa doanh số, doanh thu thuần và lợi nhuận, tài liệu sử
dụng chuỗi công thức sau:

**Công thức doanh thu**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Gross Sales = Tổng tiền hàng trước giảm giá/hoàn tiền</p>
<p>Discount = Tổng chiết khấu hợp lệ</p>
<p>Refund = Tổng tiền hoàn trả</p>
<p>Net Revenue = Gross Sales - Discount - Refund</p>
<p>Gross Profit = Net Revenue - COGS</p>
<p>Operating Profit = Gross Profit - Operating Expenses</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Chỉ tiêu**                          | **Công thức**                                  | **Ví dụ**                          |
|---------------------------------------|------------------------------------------------|------------------------------------|
| Doanh số gộp (Gross Sales)            |                                                |                                    |
|                                       | Σ Giá bán × Số lượng                           |                                    |
|                                       |                                                | 120.000.000                        |
| Chiết khấu (Discount)                 |                                                |                                    |
|                                       | Σ các khoản giảm giá hợp lệ                    |                                    |
|                                       |                                                | 5.000.000                          |
| Hoàn tiền (Refund)                    |                                                |                                    |
|                                       | Σ giá trị hoàn tiền                            |                                    |
|                                       |                                                | 1.000.000                          |
| Doanh thu thuần (Net Revenue)         |                                                |                                    |
|                                       | Gross Sales - Discount - Refund                |                                    |
|                                       |                                                | 114.000.000                        |
| Giá vốn (COGS)                        |                                                |                                    |
|                                       | Σ Chi phí hàng hóa/nguyên liệu tiêu thụ        |                                    |
|                                       |                                                | 34.200.000                         |
| Lợi nhuận gộp (Gross Profit)          |                                                |                                    |
|                                       | Net Revenue - COGS                             |                                    |
|                                       |                                                | 79.800.000                         |
| Chi phí vận hành (OPEX)               |                                                |                                    |
|                                       | Payroll + Rent + Utilities + Marketing + Other |                                    |
|                                       |                                                | 46.000.000                         |
| Lợi nhuận vận hành (Operating Profit) |                                                |                                    |
|                                       | Gross Profit - OPEX                            |                                    |
|                                       |                                                | 33.800.000                         |
| AOV                                   |                                                |                                    |
|                                       | Net Revenue / Số đơn hoàn tất                  |                                    |
|                                       |                                                | Ví dụ 114.000.000 / 3.000 = 38.000 |

## 20A.2. Công thức doanh thu theo cơ sở

**Mermaid: Luồng tính doanh thu theo cơ sở**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Đơn POS"] --&gt; B["Dòng hàng"]<br />
B --&gt; C["Tính tiền hàng"]<br />
C --&gt; D["Chiết khấu / Hoàn tiền"]<br />
D --&gt; E["Doanh thu thuần"]<br />
E --&gt; F["Gắn cơ sở / POS"]<br />
F --&gt; G["Tổng hợp doanh thu theo ngày"]<br />
G --&gt; H["Dashboard doanh thu từng cơ sở"]<br />
H --&gt; I["Đối soát với thanh toán"]<br />
I --&gt; J["Kế toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## 20A.3. Công thức tiền lương nhân viên

Các công thức dưới đây là khung nghiệp vụ. Tỷ lệ bảo hiểm, thuế và giảm
trừ phải được cấu hình theo quy định pháp luật và kỳ áp dụng thực tế,
không hard-code trong tài liệu.

**Công thức lương tổng quát**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Lương cơ bản / Lương theo giờ"] --&gt; E["Tổng thu nhập trước khấu
trừ"]<br />
B["Tiền làm thêm giờ"] --&gt; E<br />
C["Phụ cấp"] --&gt; E<br />
D["Thưởng"] --&gt; E<br />
E --&gt; F["Các khoản khấu trừ"]<br />
F --&gt; G["Lương thực nhận"]<br />
G --&gt; H["Đối soát phiếu lương / thanh toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

| **Khoản**  | **Công thức khung**                                                      | **Ví dụ**                  |
|------------|--------------------------------------------------------------------------|----------------------------|
| Lương giờ  |                                                                          |                            |
|            | Đơn giá giờ × Giờ làm hợp lệ                                             |                            |
|            |                                                                          | 25.000 × 176 = 4.400.000   |
| Lương ngày |                                                                          |                            |
|            | Đơn giá ngày × Ngày công hợp lệ                                          |                            |
|            |                                                                          | 300.000 × 26 = 7.800.000   |
| OT         |                                                                          |                            |
|            | Giờ OT × Đơn giá OT theo policy                                          |                            |
|            |                                                                          | 12 × 35.000 = 420.000      |
| Phụ cấp    |                                                                          |                            |
|            | Σ các khoản phụ cấp được duyệt                                           |                            |
|            |                                                                          | 500.000                    |
| Thưởng     |                                                                          |                            |
|            | Σ khoản thưởng được duyệt                                                |                            |
|            |                                                                          | 300.000                    |
| Gross      |                                                                          |                            |
|            | Lương + OT + Phụ cấp + Thưởng - khấu trừ trước gross nếu policy quy định |                            |
|            |                                                                          | 8.820.000 (ví dụ)          |
| Net Pay    |                                                                          |                            |
|            | Gross - bảo hiểm - thuế - khấu trừ khác                                  |                            |
|            |                                                                          | Phụ thuộc cấu hình pháp lý |

## 20A.4. Luồng kiểm soát tiền lương

**D-HR-001 – Mermaid: Chấm công → tính lương**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Nhân viên"] --&gt; B["Chấm công"]<br />
B --&gt; C["Tổng hợp giờ công"]<br />
C --&gt; D["Tính giờ làm chuẩn"]<br />
C --&gt; E["Tổng hợp giờ làm thêm"]<br />
E --&gt; F["Quản lý phê duyệt giờ làm thêm"]<br />
D --&gt; G["Tập hợp dữ liệu tính lương"]<br />
F --&gt; G<br />
G --&gt; H["Tính lương cơ bản"]<br />
H --&gt; I["Cộng giờ làm thêm + phụ cấp + thưởng"]<br />
I --&gt; J["Trừ bảo hiểm / thuế / khấu trừ"]<br />
J --&gt; K["Lương thực nhận"]<br />
K --&gt; L["HR kiểm tra"]<br />
L --&gt; M{"Dữ liệu đúng?"}<br />
M --&gt;|Không| G<br />
M --&gt;|Có| N["Phê duyệt bảng lương"]<br />
N --&gt; O["Tạo phiếu lương"]<br />
O --&gt; P["Thanh toán / Ghi nhận kế toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 34. Mã Mermaid để vẽ sơ đồ

Các đoạn mã dưới đây được viết để sao chép trực tiếp vào Mermaid Live
Editor, Mermaid trong Markdown hoặc công cụ hỗ trợ Mermaid. Tên bước
nghiệp vụ được ưu tiên bằng tiếng Việt.

Các đoạn mã dưới đây có thể được dán vào Mermaid Live Editor, Markdown
hỗ trợ Mermaid hoặc công cụ vẽ tương thích Mermaid. Các sơ đồ sử dụng ID
D-\* để dễ truy vết với tài liệu.

**D-001 – ERP tổng thể**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách hàng / Nhu cầu"] --&gt; B{"Kênh bán hàng"}<br />
B --&gt; C["POS nhà hàng"]<br />
B --&gt; D["Đơn trực tuyến / Ứng dụng"]<br />
C --&gt; E["Pha chế / Phục vụ"]<br />
D --&gt; F["Xác định cơ sở"]<br />
F --&gt; E<br />
E --&gt; G["Thanh toán"]<br />
G --&gt; H["Doanh thu / Kế toán"]<br />
E --&gt; I["Tiêu hao nguyên liệu"]<br />
I --&gt; J["Kho cơ sở"]<br />
J --&gt; K{"Cần bổ sung?"}<br />
K --&gt;|Có| L{"Nguồn nội bộ đủ?"}<br />
K --&gt;|Không| J<br />
L --&gt;|Có| M["Điều chuyển"]<br />
L --&gt;|Không| N["Mua hàng"]<br />
M --&gt; J<br />
N --&gt; J<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-002 – POS nhà hàng**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách đến"] --&gt; B["Chọn bàn"]<br />
B --&gt; C["Mở bàn"]<br />
C --&gt; D["Tạo đơn"]<br />
D --&gt; E["Thêm món"]<br />
E --&gt; F["Gửi món"]<br />
F --&gt; G["Quầy pha chế / chuẩn bị"]<br />
G --&gt; H["Đang pha chế"]<br />
H --&gt; I["Món sẵn sàng"]<br />
I --&gt; J["Phục vụ"]<br />
J --&gt; K{"Khách gọi thêm?"}<br />
K --&gt;|Có| E<br />
K --&gt;|Không| L["Yêu cầu thanh toán"]<br />
L --&gt; M["Thanh toán"]<br />
M --&gt; N["Đóng đơn"]<br />
N --&gt; O["Bàn trở về trạng thái trống"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-003 – Online/App**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Khách đặt App / Website"] --&gt; B["Tạo đơn"]<br />
B --&gt; C["Odoo / Hệ thống tích hợp"]<br />
C --&gt; D["Xác định cơ sở"]<br />
D --&gt; E["Kiểm tra tồn kho của cơ sở"]<br />
E --&gt; F{"Có thể đáp ứng?"}<br />
F --&gt;|Có| G["Xác nhận đơn"]<br />
F --&gt;|Không| H["Ngoại lệ: thay thế / hủy / hoàn tiền / chuyển cơ
sở"]<br />
G --&gt; I["Pha chế"]<br />
I --&gt; J["Khách nhận / Giao hàng"]<br />
J --&gt; K["Thanh toán"]<br />
K --&gt; L["Kế toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-004 – Bổ sung tồn kho**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Tồn kho thấp / phát sinh nhu cầu"] --&gt; B["Kiểm tra mức tồn tối
thiểu"]<br />
B --&gt; C["Kiểm tra B / C: Available + Tồn an toàn"]<br />
C --&gt; D{"Nguồn nội bộ đủ?"}<br />
D --&gt;|Có| E["Yêu cầu điều chuyển"]<br />
D --&gt;|Không| F["Yêu cầu mua hàng"]<br />
E --&gt; G["Phê duyệt"]<br />
G --&gt; H["Xuất kho nguồn"]<br />
H --&gt; I["Kho đích nhận"]<br />
I --&gt; J["Tăng tồn kho"]<br />
F --&gt; K["Yêu cầu báo giá → Đơn mua"]<br />
K --&gt; L["Nhận hàng"]<br />
L --&gt; J<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-005 – Điều chuyển nội bộ**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Kho A yêu cầu"] --&gt; B["Kiểm tra kho B / C"]<br />
B --&gt; C["Kiểm tra Available"]<br />
C --&gt; D["Kiểm tra tồn an toàn sau điều chuyển"]<br />
D --&gt; E{"Đủ điều kiện?"}<br />
E --&gt;|Không| F["Điều chỉnh / Từ chối / Xin ngoại lệ"]<br />
E --&gt;|Có| G["Phê duyệt"]<br />
G --&gt; H["Soạn hàng"]<br />
H --&gt; I["Xuất hàng"]<br />
I --&gt; J["Đang vận chuyển"]<br />
J --&gt; K["Kho A nhận"]<br />
K --&gt; L["Xác nhận nhập"]<br />
L --&gt; M["Kho B giảm tồn / Kho A tăng tồn"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-006 – Nhập kho mua hàng**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Phát sinh nhu cầu mua"] --&gt; B["Yêu cầu báo giá"]<br />
B --&gt; C["Chọn nhà cung cấp"]<br />
C --&gt; D["Đơn mua hàng"]<br />
D --&gt; E{"Được duyệt?"}<br />
E --&gt;|Không| D<br />
E --&gt;|Có| F["Nhà cung cấp giao hàng"]<br />
F --&gt; G["Kho HIM nhận hàng"]<br />
G --&gt; H["Kiểm đếm / kiểm tra"]<br />
H --&gt; I{"Đạt yêu cầu?"}<br />
I --&gt;|Không| J["Ngoại lệ / Trả hàng / Khiếu nại"]<br />
I --&gt;|Có| K["Xác nhận nhập kho"]<br />
K --&gt; L["Đưa hàng vào vị trí"]<br />
L --&gt; M["Tăng tồn kho"]<br />
M --&gt; N["Hóa đơn nhà cung cấp"]<br />
N --&gt; O["Thanh toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-007 – Giá vốn sản phẩm**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Sản phẩm bán"] --&gt; B["Định mức / Công thức"]<br />
B --&gt; C["Nguyên liệu"]<br />
C --&gt; D["Định lượng"]<br />
D --&gt; E["Đơn giá nguyên liệu"]<br />
E --&gt; F["Chi phí nguyên liệu trực tiếp"]<br />
F --&gt; G["Cộng nhân công / công đoạn / chi phí chung nếu áp
dụng"]<br />
G --&gt; H["Giá thành / Giá vốn sản phẩm"]<br />
H --&gt; I["Giá vốn bán hàng"]<br />
I --&gt; J["Biên lợi nhuận gộp"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-008 – Payroll**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Nhân viên"] --&gt; B["Hợp đồng"]<br />
B --&gt; C["Lịch làm việc"]<br />
C --&gt; D["Chấm công"]<br />
D --&gt; E["Giờ công"]<br />
D --&gt; F["Giờ làm thêm"]<br />
F --&gt; G["Quản lý duyệt giờ làm thêm"]<br />
E --&gt; H["Lương cơ bản"]<br />
G --&gt; I["Dữ liệu tính lương"]<br />
H --&gt; I<br />
I --&gt; J["Cộng giờ làm thêm + phụ cấp + thưởng"]<br />
J --&gt; K["Trừ bảo hiểm / thuế / khấu trừ"]<br />
K --&gt; L["Lương thực nhận"]<br />
L --&gt; M["Phê duyệt"]<br />
M --&gt; N["Phiếu lương / Thanh toán"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-009 – Doanh thu**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Đơn POS / Đơn trực tuyến"] --&gt; B["Tổng doanh thu bán hàng"]<br />
B --&gt; C["Chiết khấu"]<br />
C --&gt; D["Hoàn tiền / Hoàn hàng"]<br />
D --&gt; E["Doanh thu thuần"]<br />
E --&gt; F["Đối soát thanh toán"]<br />
F --&gt; G["Kế toán"]<br />
E --&gt; H["Giá vốn"]<br />
H --&gt; I["Lợi nhuận gộp"]<br />
I --&gt; J["Chi phí hoạt động"]<br />
J --&gt; K["Lợi nhuận hoạt động"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-010 – CRM B2B**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart LR<br />
A["MỚI"] --&gt; B["XÁC THỰC"]<br />
B --&gt; C["PHÂN TÍCH NHU CẦU"]<br />
C --&gt; D["ĐỀ XUẤT / BÁO GIÁ"]<br />
D --&gt; E["ĐÀM PHÁN"]<br />
E --&gt; F["ĐÃ CHỐT"]<br />
A --&gt; G["KHÔNG THÀNH CÔNG"]<br />
B --&gt; G<br />
C --&gt; G<br />
D --&gt; G<br />
E --&gt; G<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**D-011 – UAT**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>```mermaid<br />
flowchart TD<br />
A["Yêu cầu nghiệp vụ"] --&gt; B["Yêu cầu chức năng"]<br />
B --&gt; C["Ca kiểm thử UAT"]<br />
C --&gt; D["Thực hiện kiểm thử"]<br />
D --&gt; E{"Đạt?"}<br />
E --&gt;|Không| F["Ghi nhận lỗi"]<br />
F --&gt; G["Sửa lỗi / Cập nhật cấu hình"]<br />
G --&gt; D<br />
E --&gt;|Có| H["Nghiệm thu"]<br />
```</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# 26. Bộ mã Mermaid – Sơ đồ nghiệp vụ hoàn chỉnh

Mục này bổ sung và chuẩn hóa các sơ đồ dưới dạng Mermaid code để có thể
copy trực tiếp vào Mermaid Live Editor hoặc công cụ hỗ trợ Mermaid. Bản
v2 có các luồng tổng quát nhưng một số sơ đồ còn thiếu actor, decision
point, exception và điểm kiểm soát. Bản v3 mở rộng thành bộ sơ đồ
đầu-cuối và giữ nguyên nguyên tắc Business → Process → Requirement →
Odoo Solution → UAT.

Lưu ý: các nhánh có ghi “policy HIM” hoặc “cần xác nhận” là điểm nghiệp
vụ chưa được coi là fact chính thức. Không tự động biến các nhánh này
thành chính sách của HIM.

| Mã    | Sơ đồ                                                         | Mục đích                               |
|-------|---------------------------------------------------------------|----------------------------------------|
| D-001 | ERP End-to-End Architecture (Kiến trúc vận hành ERP tổng thể) | Dùng để mô tả quy trình / traceability |
| D-002 | Restaurant POS – Quản lý bàn và order                         | Dùng để mô tả quy trình / traceability |
| D-003 | Preparation / Bar – Nhận và xử lý món                         | Dùng để mô tả quy trình / traceability |
| D-004 | Payment & Daily Closing – Thanh toán và chốt ca/ngày          | Dùng để mô tả quy trình / traceability |
| D-005 | Online/App Order – Phân bổ đơn về đúng cơ sở                  | Dùng để mô tả quy trình / traceability |
| D-006 | Goods Receipt – Quy trình nhập kho từ nhà cung cấp            | Dùng để mô tả quy trình / traceability |
| D-007 | HIM Warehouse Receive & Issue – Kho HIM nhận và xuất          | Dùng để mô tả quy trình / traceability |
| D-008 | Replenishment Decision – Quyết định điều chuyển hay mua       | Dùng để mô tả quy trình / traceability |
| D-009 | Internal Transfer – Điều chuyển giữa các kho HIM              | Dùng để mô tả quy trình / traceability |
| D-010 | Purchase Replenishment – Mua hàng khi nguồn nội bộ không đủ   | Dùng để mô tả quy trình / traceability |
| D-011 | Recipe/BOM & Ingredient Consumption – Định mức và tiêu hao    | Dùng để mô tả quy trình / traceability |
| D-012 | Revenue → COGS → Gross Profit → Operating Profit              | Dùng để mô tả quy trình / traceability |
| D-013 | Employee → Attendance → OT → Payroll → Accounting             | Dùng để mô tả quy trình / traceability |
| D-014 | Corporate CRM – B2B Opportunity Pipeline                      | Dùng để mô tả quy trình / traceability |
| D-015 | Cross-Module Traceability – Từ bán hàng đến quản trị          | Dùng để mô tả quy trình / traceability |
| D-016 | Exception Handling – Các nhánh lỗi quan trọng                 | Dùng để mô tả quy trình / traceability |
| D-017 | UAT End-to-End – Luồng kiểm thử nghiệp vụ                     | Dùng để mô tả quy trình / traceability |

## D-001. ERP End-to-End Architecture (Kiến trúc vận hành ERP tổng thể)

Mermaid code:

> flowchart LR  
> C\[Khách hàng\] --\> POS\[Restaurant POS  
> Bán tại bàn / tại quầy\]  
> C --\> APP\[App / Web / Kênh Online\]  
> POS --\> PREP\[Bar / Preparation  
> Pha chế - phục vụ\]  
> APP --\> ROUTE\[Phân bổ cơ sở  
> Branch Routing\]  
> ROUTE --\> PREP  
> PREP --\> INV\[Kho cơ sở  
> Branch Warehouse\]  
> INV --\> REP{Nhu cầu bổ sung?}  
> REP --\>\|Điều chuyển\| TR\[Internal Transfer  
> Điều chuyển nội bộ\]  
> REP --\>\|Mua ngoài\| PUR\[Purchase  
> Mua hàng\]  
> PUR --\> INV  
> TR --\> INV  
> POS --\> PAY\[Payment  
> Thanh toán\]  
> APP --\> PAY  
> PAY --\> ACC\[Accounting  
> Kế toán\]  
> INV --\> COGS\[COGS / Giá vốn\]  
> ACC --\> DASH\[Dashboard  
> Báo cáo quản trị\]  
> INV --\> DASH  
> POS --\> CRM\[Customer History / CRM  
> Lịch sử khách hàng / CRM\]  
> CRM --\> DASH  
> HR\[Employees / Attendance / Payroll  
> Nhân sự / Chấm công / Tiền lương\] --\> ACC  
> HR --\> DASH

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-002. Restaurant POS – Quản lý bàn và order

Mermaid code:

> flowchart TD  
> A\[Khách đến quán\] --\> B{Bàn còn trống?}  
> B --\>\|Có\| C\[Nhân viên mở Table  
> Chọn bàn\]  
> B --\>\|Không\| Z\[Thông báo / chờ bàn\]  
> C --\> D\[Tạo Order  
> Gắn Table + POS Session\]  
> D --\> E\[Thêm món + số lượng + ghi chú\]  
> E --\> F{Khách gọi thêm?}  
> F --\>\|Có\| E  
> F --\>\|Không\| G\[Gửi Order tới Preparation\]  
> G --\> H\[Bar nhận món + số bàn\]  
> H --\> I\[Chuẩn bị món\]  
> I --\> J\[Ready / Sẵn sàng\]  
> J --\> K\[Nhân viên phục vụ\]  
> K --\> L{Còn món bổ sung?}  
> L --\>\|Có\| E  
> L --\>\|Không\| M\[Yêu cầu thanh toán\]  
> M --\> N\[Kiểm tra Order + Discount/Promotion nếu hợp lệ\]  
> N --\> O\[Chọn phương thức thanh toán\]  
> O --\> P\[Đăng ký Payment\]  
> P --\> Q\[Đóng Order\]  
> Q --\> R\[Bàn trở về Available / Trống\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-003. Preparation / Bar – Nhận và xử lý món

Mermaid code:

> flowchart LR  
> A\[POS gửi Order\] --\> B\[Preparation Queue  
> Hàng chờ pha chế\]  
> B --\> C{Kiểm tra món}  
> C --\>\|Có đủ nguyên liệu\| D\[Start / Preparing  
> Bắt đầu pha chế\]  
> C --\>\|Thiếu nguyên liệu\| X\[Exception  
> Báo thiếu / xử lý theo policy\]  
> D --\> E\[Hoàn tất món\]  
> E --\> F\[Ready  
> Sẵn sàng\]  
> F --\> G\[Nhân viên nhận món\]  
> G --\> H\[Phục vụ khách\]  
> D --\> Y{Có lỗi / hủy?}  
> Y --\>\|Có\| Z\[Cancel / Rework  
> Theo quyền hạn\]  
> Y --\>\|Không\| E

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-004. Payment & Daily Closing – Thanh toán và chốt ca/ngày

Mermaid code:

> flowchart TD  
> A\[Order hoàn tất\] --\> B\[Kiểm tra tổng tiền\]  
> B --\> C\[Áp dụng Discount/Promotion nếu đủ điều kiện\]  
> C --\> D\[Chọn Payment Method\]  
> D --\> E\[Thu tiền / xác nhận thanh toán\]  
> E --\> F{Thanh toán thành công?}  
> F --\>\|Không\| X\[Xử lý lỗi / đổi phương thức\]  
> X --\> D  
> F --\>\|Có\| G\[Đóng Order\]  
> G --\> H\[Table Available\]  
> H --\> I\[Đối soát POS Orders\]  
> I --\> J\[Đối soát Payments\]  
> J --\> K\[Cash / Bank / Other Reconciliation\]  
> K --\> L\[Daily Closing  
> Chốt ca/ngày\]  
> L --\> M\[Accounting / Revenue Report\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-005. Online/App Order – Phân bổ đơn về đúng cơ sở

Mermaid code:

> flowchart TD  
> A\[Khách đặt App / Web / Kênh ngoài\] --\> B\[Order vào Odoo /
> Integration\]  
> B --\> C\[Xác định Branch phục vụ\]  
> C --\> D{Có Branch hợp lệ?}  
> D --\>\|Không\| X\[Exception: không xác định được cơ sở\]  
> D --\>\|Có\| E\[Kiểm tra Product + Stock của Branch\]  
> E --\> F{Đủ hàng?}  
> F --\>\|Không\| Y\[Business Exception:  
> Substitute / Cancel / Refund / Reroute  
> Cần policy HIM\]  
> F --\>\|Có\| G\[Accept Order\]  
> G --\> H\[Preparation tại Branch\]  
> H --\> I\[Ready\]  
> I --\> J\[Pickup / Delivery\]  
> J --\> K\[Payment / Reconciliation\]  
> K --\> L\[Accounting + Reporting + Customer History\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-006. Goods Receipt – Quy trình nhập kho từ nhà cung cấp

Mermaid code:

> flowchart TD  
> A\[Nhu cầu nguyên liệu\] --\> B\[Purchase Request / RFQ\]  
> B --\> C\[So sánh NCC / giá / điều kiện\]  
> C --\> D\[PO được phê duyệt\]  
> D --\> E\[NCC giao hàng\]  
> E --\> F\[Kho HIM kiểm đếm\]  
> F --\> G{Đúng sản phẩm + số lượng + chất lượng?}  
> G --\>\|Không\| H\[Ghi nhận chênh lệch / từ chối / xử lý với NCC\]  
> G --\>\|Có\| I\[Validate Receipt  
> Xác nhận nhập kho\]  
> I --\> J\[Cập nhật On Hand\]  
> J --\> K\[Đối chiếu PO - Receipt\]  
> K --\> L\[NCC gửi Invoice\]  
> L --\> M\[Vendor Bill\]  
> M --\> N\[Accounting / Payment theo policy\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-007. HIM Warehouse Receive & Issue – Kho HIM nhận và xuất

Mermaid code:

> flowchart TD  
> subgraph RECEIVE\[HIM Warehouse Receive – Kho HIM nhận hàng\]  
> R1\[Hàng đến kho HIM\] --\> R2\[Kiểm đếm + kiểm tra chứng từ\]  
> R2 --\> R3{Đạt yêu cầu?}  
> R3 --\>\|Không\| R4\[Ghi nhận thiếu / hỏng / sai\]  
> R3 --\>\|Có\| R5\[Putaway vào Location\]  
> R5 --\> R6\[Validate Receipt\]  
> R6 --\> R7\[Stock tăng  
> On Hand cập nhật\]  
> end  
> subgraph ISSUE\[HIM Warehouse Issue – Kho HIM xuất hàng\]  
> I1\[Nhu cầu xuất  
> POS / Transfer / Internal Request\] --\> I2\[Kiểm tra Available\]  
> I2 --\> I3{Đủ hàng?}  
> I3 --\>\|Không\| I4\[Exception / Replenishment\]  
> I3 --\>\|Có\| I5\[Picking / chuẩn bị hàng\]  
> I5 --\> I6\[Kiểm đếm trước xuất\]  
> I6 --\> I7\[Validate Delivery / Issue\]  
> I7 --\> I8\[Stock giảm  
> On Hand cập nhật\]  
> end  
> R7 --\> S\[Stock Ledger / Inventory Reporting\]  
> I8 --\> S

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-008. Replenishment Decision – Quyết định điều chuyển hay mua

Mermaid code:

> flowchart TD  
> A\[Kho A phát sinh nhu cầu bổ sung\] --\> B\[Kiểm tra On Hand /
> Reserved / Incoming / Available\]  
> B --\> C{Có nhu cầu replenishment?}  
> C --\>\|Không\| Z\[Kết thúc\]  
> C --\>\|Có\| D\[Kiểm tra các kho HIM khác\]  
> D --\> E{Kho khác có Available đủ?}  
> E --\>\|Có\| F\[Đánh giá sau điều chuyển  
> Safety Stock / policy\]  
> F --\> G{Có thể điều chuyển?}  
> G --\>\|Có\| H\[Tạo Internal Transfer Request\]  
> G --\>\|Không\| I\[Chuyển sang Purchase\]  
> E --\>\|Không\| I  
> I --\> J\[Tạo RFQ / PO\]  
> H --\> K\[Source Warehouse Review\]  
> K --\> L\[Approve / Adjust / Reject\]  
> L --\> M\[Issue → In Transit → Receive\]  
> J --\> N\[Vendor Delivery → Receipt\]  
> M --\> O\[Stock A tăng\]  
> N --\> O

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-009. Internal Transfer – Điều chuyển giữa các kho HIM

Mermaid code:

> flowchart TD  
> A\[Kho A yêu cầu 10kg\] --\> B\[Tạo Transfer Request\]  
> B --\> C\[Chỉ định Source B + Destination A\]  
> C --\> D\[Source B kiểm tra Available\]  
> D --\> E{Đủ và không vi phạm policy?}  
> E --\>\|Không\| F\[Adjust Qty / Reject / Chọn kho khác\]  
> F --\> G{Có nguồn khác?}  
> G --\>\|Có\| C  
> G --\>\|Không\| H\[Purchase Requirement\]  
> E --\>\|Có\| I\[Approve\]  
> I --\> J\[Picking tại B\]  
> J --\> K\[Validate Issue / Shipped\]  
> K --\> L\[In Transit\]  
> L --\> M\[Kho A nhận hàng\]  
> M --\> N{Received = Shipped?}  
> N --\>\|Có\| O\[Validate Receipt → Done\]  
> N --\>\|Không\| P\[Discrepancy  
> Thiếu / hỏng / lệch\]  
> P --\> Q\[Điều chỉnh + Reason + Approval theo policy\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-010. Purchase Replenishment – Mua hàng khi nguồn nội bộ không đủ

Mermaid code:

> flowchart TD  
> A\[Replenishment Need\] --\> B\[Internal Source Check\]  
> B --\> C{Nguồn nội bộ đủ?}  
> C --\>\|Có\| D\[Internal Transfer\]  
> C --\>\|Không\| E\[Tạo RFQ\]  
> E --\> F\[Chọn NCC / thương lượng\]  
> F --\> G\[PO Approval\]  
> G --\> H\[PO Sent\]  
> H --\> I\[NCC giao hàng\]  
> I --\> J\[Warehouse Receipt\]  
> J --\> K\[Quality / Quantity Check\]  
> K --\> L{Đạt?}  
> L --\>\|Không\| M\[Discrepancy / Return / Claim\]  
> L --\>\|Có\| N\[Validate Receipt\]  
> N --\> O\[Stock tăng\]  
> O --\> P\[Vendor Bill\]  
> P --\> Q\[Payment / Accounting\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-011. Recipe/BOM & Ingredient Consumption – Định mức và tiêu hao

Mermaid code:

> flowchart TD  
> A\[Product: Bạc Xỉu\] --\> B\[Recipe / BOM  
> Định mức\]  
> B --\> C\[Coffee 18g\]  
> B --\> D\[Milk 150ml\]  
> B --\> E\[Sugar 10g\]  
> B --\> F\[Cup/Lid 1 set\]  
> G\[POS Sale\] --\> H\[Consumption Trigger  
> Theo mô hình HIM được xác nhận\]  
> H --\> I\[Trừ nguyên liệu tại Branch Warehouse\]  
> I --\> J\[Update Stock + Cost\]  
> J --\> K\[COGS / Margin Reporting\]  
> B --\> L{Có cần Manufacturing Order?}  
> L --\>\|Không\| H  
> L --\>\|Có\| M\[MRP / MO / Work Order\]  
> M --\> I

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-012. Revenue → COGS → Gross Profit → Operating Profit

Mermaid code:

> flowchart LR  
> A\[POS / Online Sales\] --\> B\[Gross Sales  
> Tổng bán\]  
> B --\> C\[- Discounts  
> Chiết khấu\]  
> C --\> D\[- Returns / Refunds / Voids  
> Hoàn / hủy\]  
> D --\> E\[Net Revenue  
> Doanh thu thuần\]  
> E --\> F\[- COGS  
> Giá vốn\]  
> F --\> G\[Gross Profit  
> Lợi nhuận gộp\]  
> G --\> H\[- OPEX  
> Payroll + Rent + Utilities + Marketing + Fees + Other\]  
> H --\> I\[Operating Profit  
> Lợi nhuận hoạt động\]  
> E --\> J\[Revenue Report\]  
> F --\> K\[COGS Report\]  
> I --\> L\[Management Dashboard\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-013. Employee → Attendance → OT → Payroll → Accounting

Mermaid code:

> flowchart TD  
> A\[Employee Master\] --\> B\[Contract / Salary Structure\]  
> B --\> C\[Work Schedule / Shift\]  
> C --\> D\[Check-in / Check-out\]  
> D --\> E\[Attendance Calculation\]  
> E --\> F{Có OT?}  
> F --\>\|Không\| G\[Payroll Inputs\]  
> F --\>\|Có\| H\[OT Request / Approval\]  
> H --\> G  
> G --\> I\[Allowance / Bonus / Deduction\]  
> I --\> J\[Gross Earnings\]  
> J --\> K\[Statutory / Configured Deductions\]  
> K --\> L\[Net Pay\]  
> L --\> M\[Review / Approval\]  
> M --\> N\[Payslip\]  
> N --\> O\[Accounting Entry / Payment\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-014. Corporate CRM – B2B Opportunity Pipeline

Mermaid code:

> flowchart LR  
> A\[Lead / Khách doanh nghiệp\] --\> B\[NEW  
> Mới\]  
> B --\> C\[QUALIFICATION  
> Xác thực nhu cầu\]  
> C --\> D\[NEEDS ANALYSIS  
> Phân tích nhu cầu\]  
> D --\> E\[PROPOSAL  
> Đề xuất / Báo giá\]  
> E --\> F\[NEGOTIATION  
> Đàm phán\]  
> F --\> G\[WON  
> Đã chốt\]  
> B --\> X\[LOST  
> Không thành công + Lost Reason\]  
> C --\> X  
> D --\> X  
> E --\> X  
> F --\> X  
> G --\> H\[Sales Order / Quotation / Service Fulfillment\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-015. Cross-Module Traceability – Từ bán hàng đến quản trị

Mermaid code:

> flowchart TD  
> A\[Customer / Demand\] --\> B\[POS / Online Order\]  
> B --\> C\[Preparation / Fulfillment\]  
> C --\> D\[Ingredient Consumption\]  
> D --\> E\[Branch Inventory\]  
> E --\> F{Stock Below Threshold?}  
> F --\>\|Yes\| G\[Replenishment\]  
> G --\> H\[Internal Transfer or Purchase\]  
> H --\> E  
> B --\> I\[Payment\]  
> I --\> J\[Revenue\]  
> E --\> K\[COGS\]  
> J --\> L\[Gross Profit\]  
> K --\> L  
> L --\> M\[OPEX / Payroll\]  
> M --\> N\[Operating Profit\]  
> N --\> O\[Dashboard / Management Decision\]  
> B --\> P\[Customer History\]  
> P --\> Q\[CRM / Loyalty / Segmentation if applicable\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-016. Exception Handling – Các nhánh lỗi quan trọng

Mermaid code:

> flowchart TD  
> A\[Business Transaction\] --\> B{Exception?}  
> B --\>\|Không\| Z\[Continue Standard Flow\]  
> B --\>\|POS: món hết\| C\[Notify Staff → Policy: Substitute /
> Cancel\]  
> B --\>\|Online: branch thiếu hàng\| D\[Substitute / Cancel / Refund /
> Reroute\]  
> B --\>\|Warehouse: received ≠ shipped\| E\[Discrepancy Record +
> Approval\]  
> B --\>\|Transfer: source không đủ\| F\[Adjust Qty / Other Source /
> Purchase\]  
> B --\>\|Purchase: hàng sai/hỏng\| G\[Return / Claim / Adjustment\]  
> B --\>\|Payment failed\| H\[Retry / Change Payment Method\]  
> B --\>\|Payroll input sai\| I\[Correct Attendance/OT → Recalculate\]  
> C --\> Z  
> D --\> Z  
> E --\> Z  
> F --\> Z  
> G --\> Z  
> H --\> Z  
> I --\> Z

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

## D-017. UAT End-to-End – Luồng kiểm thử nghiệp vụ

Mermaid code:

> flowchart TD  
> A\[Chuẩn bị Master Data\] --\> B\[TC: Bán tại bàn\]  
> B --\> C\[Kiểm tra Preparation\]  
> C --\> D\[Kiểm tra Payment\]  
> D --\> E\[Kiểm tra Stock Consumption\]  
> E --\> F\[TC: Kho thiếu hàng\]  
> F --\> G\[Kiểm tra Transfer / Purchase\]  
> G --\> H\[TC: Nhập kho\]  
> H --\> I\[TC: Xuất kho / Điều chuyển\]  
> I --\> J\[TC: Doanh thu + COGS\]  
> J --\> K\[TC: Attendance + OT + Payroll\]  
> K --\> L\[TC: Dashboard\]  
> L --\> M\[Đối chiếu dữ liệu liên module\]  
> M --\> N{Tất cả Acceptance Criteria đạt?}  
> N --\>\|Có\| O\[UAT Passed / Go-Live Approval\]  
> N --\>\|Không\| P\[Defect / Change Request → Retest\]

Kiểm soát BA: Xác định actor/đầu vào → decision → transaction → output →
exception → dữ liệu liên module. Khi triển khai Odoo, đối chiếu từng
node với Standard, Studio/Automation hoặc Custom Module trước khi cấu
hình.

# 27. Diagram Completeness Checklist – Checklist kiểm tra tính đầy đủ của sơ đồ

- Có actor hoặc vai trò chịu trách nhiệm ở các bước quan trọng.

- Có điểm bắt đầu và điểm kết thúc rõ ràng.

- Có decision point đối với các nghiệp vụ có điều kiện.

- Có exception flow cho thiếu hàng, sai hàng, thanh toán lỗi, chênh lệch
  nhận/xuất và dữ liệu sai.

- Có dữ liệu đầu vào/đầu ra hoặc transaction chính: Order, Payment,
  Receipt, Transfer, PO, Attendance, Payslip.

- Có liên kết giữa POS → Inventory → Purchase/Transfer → Accounting →
  Dashboard.

- Kho được tách theo từng cơ sở; không giả định kho trung tâm.

- Quy trình kho bao gồm ít nhất: nhập kho từ NCC và HIM Warehouse
  Receive & Issue; điều chuyển nội bộ được tách riêng vì có
  source/destination và approval.

- Quy trình nhân sự liên kết Attendance → OT → Payroll → Accounting.

- Quy trình doanh thu phân biệt Gross Sales, Discounts, Returns/Refunds,
  Net Revenue, COGS, Gross Profit và OPEX.

- UAT kiểm thử đầu-cuối và có nhánh Defect → Retest / Change Request.

# 28. Recommended Diagram Placement – Vị trí nên đặt sơ đồ trong tài liệu

| Phần tài liệu                    | Sơ đồ                             |
|----------------------------------|-----------------------------------|
| Project Overview                 | D-001                             |
| Restaurant POS Functional Design | D-002, D-003, D-004               |
| Online/App                       | D-005                             |
| Inventory & Warehouse            | D-006, D-007, D-008, D-009, D-010 |
| Product / Recipe / Costing       | D-011                             |
| Revenue & Profitability          | D-012                             |
| HR & Payroll                     | D-013                             |
| CRM & B2B                        | D-014                             |
| Traceability / Architecture      | D-015                             |
| Risks / Exceptions               | D-016                             |
| UAT                              | D-017                             |

# 29. BA Review Notes – Các điểm cần xác nhận trước khi coi TO-BE là chính thức

- Luồng Bar nhận order: màn hình Preparation hay máy in/thiết bị khác.

- Có một hay nhiều khu vực Preparation (Bar/Kitchen) và cách phân tuyến
  món.

- Cho phép add item nhiều lần, chuyển bàn, gộp bàn, tách bill hay không.

- Quyền cancel/refund sau khi món đã bắt đầu pha chế.

- Quy tắc khi online order vào thời điểm một branch hết nguyên liệu.

- Quy tắc chọn source warehouse khi branch thiếu hàng.

- Ngưỡng Min Stock/Safety Stock và quyền override khi điều chuyển.

- Quy trình xử lý chênh lệch Shipped vs Received.

- Cách HIM ghi nhận tiêu hao nguyên liệu: trực tiếp theo POS, Inventory
  adjustment, Recipe/BOM, hay MRP.

- Chính sách discount, loyalty, refund và payment reconciliation.

- Chính sách ca làm, OT, phụ cấp, thưởng và phê duyệt payroll.
