# IPv4/IPv6 File Transfer Project

## Giới thiệu
Dự án này cung cấp một cách đơn giản để truyền tệp qua mạng sử dụng giao thức IPv4 và IPv6. Hỗ trợ các phương thức truyền:
- **Unicast**: Gửi tệp đến một thiết bị đích cụ thể.
- **Broadcast**: Gửi tệp đến tất cả các thiết bị trong mạng.
- **Multicast**: Gửi tệp đến các thiết bị trong nhóm.
- **Anycast**: Gửi tệp đến thiết bị có đường đi ngắn nhất (Mô phỏng bằng Unicast).

## Yêu cầu hệ thống
- Python 3.x
- Hệ điều hành hỗ trợ IPv6 (Linux, macOS, Windows 10 trở lên)
- Mạng hỗ trợ IPv6

---

## Hướng dẫn chạy thử nghiệm đối với IPv4

### 1. Di chuyển vào thư mục IPv4
```bash
cd IPv4
```

### 2. Khởi động máy nhận
Chạy chương trình nhận trên thiết bị nhận tệp:
```bash
python receiving_ipv4.py
```
Máy này sẽ lắng nghe các gói tin trên cổng 5007.

### 3. Gửi tệp bằng Unicast
Trên máy gửi, chạy:
```bash
python sending_ipv4.py
```
Chọn **1** để gửi theo Unicast, nhập địa chỉ **IPv4** của máy nhận và đường dẫn tệp.

### 4. Gửi tệp bằng Broadcast
```bash
python sending_ipv4.py
```
Chọn **2** để gửi theo Broadcast, nhập đường dẫn tệp.

### 5. Gửi tệp bằng Multicast
```bash
python sending_ipv4.py
```
Chọn **3**, nhập địa chỉ multicast và đường dẫn tệp.


## Hướng dẫn chạy thử nghiệm đối với IPv6

Tương tự như đối với IPv4.

---

