# Sao Chép Tệp Mature Content

Dự án này chứa các tập lệnh để sao chép tệp mature content cho VALORANT nếu tùy chọn 'Mature Content' không được bật trong trò chơi đối với một số tài khoản (Khu vực Việt Nam/Úc/v.v.).

Lưu ý: Dự án này không liên kết với Riot Games hoặc VALORANT theo bất kỳ cách nào. Nó chỉ nhằm mục đích giáo dục.

Cập nhật: 31-07-2025 (Patch 11.02 - UE5)

Hãy cho một Star nếu bạn thấy dự án này thú vị.

## Mô Tả

Các tập lệnh được cung cấp sẽ:
1. Kiểm tra xem các tệp dữ liệu cần thiết có tồn tại không.
2. Xác minh đường dẫn đích từ tệp `path.txt`.
3. Sao chép các tệp cần thiết đến đường dẫn đích.
4. Xóa các tệp đã sao chép khỏi đường dẫn đích.

Thủ thuật này cần thiết cho một số tài khoản không thể truy cập để bật Mature Content trong menu Tổng quát.

## Video hướng dẫn cách thức hoạt động của thủ thuật này (Chỉ tiếng Việt)

[![Video hướng dẫn cách thức hoạt động](https://img.youtube.com/vi/DXQOpayNVkY/maxresdefault.jpg)](https://youtu.be/DXQOpayNVkY)

## Video hướng dẫn cách sử dụng batch này (Chỉ phụ đề tiếng Việt) 
[![Video hướng dẫn cách thức hoạt động](https://img.youtube.com/vi/GyZfE7pt7pA/maxresdefault.jpg)](https://youtu.be/GyZfE7pt7pA)

## Cách Sử Dụng
1. Đảm bảo bạn đã nhấn nút **CẬP NHẬT** trong trò chơi (khuyến nghị tắt Tự động Cập nhật cho Valorant)
2. Đảm bảo bạn có các tệp dữ liệu cần thiết:

- `MatureData-WindowsClient.pak`, 
- `MatureData-WindowsClient.sig`, 
- `MatureData-WindowsClient.ucas`,
- `MatureData-WindowsClient.utoc`

trong thư mục `data`.

3. Cập nhật tệp `path.txt` với đường dẫn đích chính xác.

4. Bạn có thể chạy dự án này bằng 2 cách:
- **Chạy tập lệnh**: Mở terminal, điều hướng đến thư mục dự án và chạy `python script.py`.
- **Chạy tệp thực thi**: Chạy tệp `VALORANT-MatureContent.exe` trực tiếp. Tệp này được xây dựng từ tập lệnh Python trong trường hợp bạn không biết cách sử dụng Python.

**Lưu ý**: Trong trường hợp hiển thị Windows Defender SmartScreen, nhấp vào "More info" và sau đó "Run anyway". (*Đây là cảnh báo sai, vì tệp không có hại. Bạn có thể kiểm tra mã nguồn để xác minh.*)

## Tuyên Bố Miễn Trừ Trách Nhiệm

**TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM:** TÔI SẼ KHÔNG CHỊU TRÁCH NHIỆM NẾU TÀI KHOẢN BỊ CẤM DO SỬ DỤNG THỦ THUẬT NÀY, VÌ TÔI ĐÃ SỬ DỤNG KỂ TỪ THÁNG 9 NĂM 2022 VÀ CHƯA BỊ CẤM.

VIỆC CHỈNH SỬA CÁC TỆP TRÒ CHƠI CÓ THỂ DẪN ĐẾN VIỆC ĐÌNH CHỈ.

CÁC TỆP DỮ LIỆU TRONG DỰ ÁN NÀY ĐƯỢC LẤY TỪ MỘT TÀI KHOẢN RIOT HỢP LỆ TỪ SINGAPORE.

Tôi đang làm giao diện người dùng cho dự án này, vậy nên hãy kiên nhẫn hehe. Nếu bạn có thể giúp tôi với giao diện người dùng, đừng ngần ngại liên hệ với tôi qua thông tin liên lạc bên dưới nhé :)?

## Đóng Góp

Tạo bởi: @l1ttled1no

Đóng góp cho tác giả qua:
- Chuyển khoản ngân hàng (Việt Nam): dinong175 (MB Bank) | 593895 (OCB)
- PayPal (Toàn cầu): duynguyendang04@gmail.com
- Đăng ký kênh YouTube của tôi: [youtube.com/@l1ttled1no](https://youtube.com/@l1ttled1no)

Mọi đóng góp đều được đánh giá cao.