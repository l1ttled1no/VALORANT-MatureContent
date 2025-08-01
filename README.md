# VALORANT Mature Content Manager

![VALORANT Logo](logo/vlr.jpg)

This project contains tools to copy mature content files for VALORANT if the 'Mature Content' option is not enabled in the game for certain accounts (Vietnam, Australia, etc. regions).

**Note:** This project is not affiliated with Riot Games or VALORANT in any way. It is intended for educational purposes only.

**Update:** 31-07-2025 (Patch 11.02 - UE5)

---

## 🌐 Language / Ngôn ngữ

This README is available in both English and Vietnamese. / README này có sẵn bằng cả tiếng Anh và tiếng Việt.

- [🇺🇸 **English**](#english-version) (scroll down)
- [🇻🇳 **Tiếng Việt**](#phiên-bản-tiếng-việt) (scroll down)

---

## English Version

### 📋 Description

The provided tools will:
1. Check if the required data files exist
2. Verify the destination path 
3. Copy the necessary files to the destination path
4. Apply mature content settings to your VALORANT installation

This solution is needed for accounts that cannot access the Mature Content option in the General menu.

### 🎥 Video Tutorials

**How this trick works (Vietnamese with subtitles):**
[![Video tutorial how this trick works](https://img.youtube.com/vi/DXQOpayNVkY/maxresdefault.jpg)](https://youtu.be/DXQOpayNVkY)

**How to use this tool (Vietnamese subtitles):**
[![Video tutorial how to use this tool](https://img.youtube.com/vi/GyZfE7pt7pA/maxresdefault.jpg)](https://youtu.be/GyZfE7pt7pA)

### 🚀 Available Versions

This project offers both **GUI** and **Non-GUI** versions to suit different user preferences:

#### GUI Version (Recommended)
- **File:** `VALORANT-MatureContent-Manager.exe`
- **Features:** User-friendly interface with buttons, progress bars, and visual feedback
- **Best for:** Users who prefer point-and-click interfaces

#### Non-GUI Version
- **File:** `NON_GUI.exe` or `script.py`
- **Features:** Command-line interface for advanced users
- **Best for:** Users comfortable with terminal/command prompt

### 🖥️ GUI Version Usage

#### Requirements
- Python 3.6 or higher (if running from source)
- tkinter (usually comes with Python)

#### How to Run
**Method 1: Executable (Easiest)**
1. Double-click `VALORANT-MatureContent-Manager.exe`

**Method 2: From Source**
1. Open Command Prompt or PowerShell
2. Navigate to this directory
3. Run: `python gui_script.py`

**Method 3: Batch File**
1. Double-click `run_gui.bat`

#### GUI Features
- **User-friendly Interface**: Easy-to-use buttons and visual indicators
- **Path Selection**: Browse and select your VALORANT installation directory
- **File Checking**: Verify that all required files are present
- **Real-time Output**: See progress and results in the output window
- **Progress Bar**: Visual indication of operation progress
- **Error Handling**: Clear error messages and confirmations
- **Safety Features**: Confirmation dialogs before making changes

#### Using the GUI
1. **Launch the application** using one of the methods above
2. **Read the contribution message** that appears in a popup window
3. **Select your VALORANT installation path** using the Browse button
4. **Check files** to verify everything is ready
5. **Apply Mature Content** to copy the files and enable mature content

### 💻 Non-GUI Version Usage

#### How to Run
**Method 1: Executable**
1. Double-click `NON_GUI.exe`

**Method 2: Python Script**
1. Open terminal/command prompt
2. Navigate to the project directory
3. Run: `python script.py`

### 📁 Required Files

Ensure you have these required data files in the `data` folder:
- `MatureData-WindowsClient.pak`
- `MatureData-WindowsClient.sig`
- `MatureData-WindowsClient.ucas`
- `MatureData-WindowsClient.utoc`

### 📋 Setup Instructions

1. **Update VALORANT**: Make sure you have pressed the **UPDATE** button in the game (disabling Auto-Update for VALORANT is recommended)

2. **Verify Data Files**: Ensure all required files are present in the `data` folder

3. **Choose Your Method**: Run either the GUI or Non-GUI version based on your preference

### ⚠️ Important Notes

**Windows Defender Warning**: If Windows Defender SmartScreen appears, click "More info" and then "Run anyway". This is a false positive - the files are not harmful. You can check the source code to verify.

### 📜 Disclaimer

**DISCLAIMER:** I WILL NOT BE RESPONSIBLE IF YOUR ACCOUNT IS BANNED FOR USING THIS TOOL. I HAVE BEEN USING IT SINCE SEPTEMBER 2022 WITHOUT ANY ISSUES.

- Modification of game files can lead to account suspension
- The data files in this project are obtained from a valid Singapore Riot account
- Use at your own risk

### 🤝 Contribution

**Created by:** @l1ttled1no

**Support the developer:**
- Bank Transfer (Vietnam): dinong175 (MB Bank) | 593895 (OCB)
- PayPal (Global): duynguyendang04@gmail.com
- Subscribe to YouTube: [youtube.com/@l1ttled1no](https://youtube.com/@l1ttled1no)

Any contributions are appreciated! ⭐

---

## Phiên Bản Tiếng Việt

### 📋 Mô Tả

Các công cụ được cung cấp sẽ:
1. Kiểm tra xem các tệp dữ liệu cần thiết có tồn tại không
2. Xác minh đường dẫn đích
3. Sao chép các tệp cần thiết đến đường dẫn đích
4. Áp dụng cài đặt mature content cho VALORANT

Giải pháp này cần thiết cho các tài khoản không thể truy cập tùy chọn Mature Content trong menu Tổng quát.

### 🎥 Video Hướng Dẫn

**Cách thức hoạt động của thủ thuật:**
[![Video hướng dẫn cách thức hoạt động](https://img.youtube.com/vi/DXQOpayNVkY/maxresdefault.jpg)](https://youtu.be/DXQOpayNVkY)

**Cách sử dụng công cụ này:**
[![Video hướng dẫn cách sử dụng](https://img.youtube.com/vi/GyZfE7pt7pA/maxresdefault.jpg)](https://youtu.be/GyZfE7pt7pA)

### 🚀 Các Phiên Bản Có Sẵn

Dự án này cung cấp cả phiên bản **GUI** và **Non-GUI** để phù hợp với sở thích khác nhau:

#### Phiên Bản GUI (Khuyến Nghị)
- **Tệp:** `VALORANT-MatureContent-Manager.exe`
- **Tính năng:** Giao diện thân thiện với nút bấm, thanh tiến trình và phản hồi trực quan
- **Phù hợp cho:** Người dùng thích giao diện đồ họa

#### Phiên Bản Non-GUI
- **Tệp:** `NON_GUI.exe` hoặc `script.py`
- **Tính năng:** Giao diện dòng lệnh cho người dùng nâng cao
- **Phù hợp cho:** Người dùng quen thuộc với terminal/command prompt

### 🖥️ Sử Dụng Phiên Bản GUI

#### Yêu Cầu Hệ Thống
- Python 3.6 trở lên (nếu chạy từ mã nguồn)
- tkinter (thường đi kèm với Python)

#### Cách Chạy
**Phương pháp 1: Tệp thực thi (Dễ nhất)**
1. Double-click `VALORANT-MatureContent-Manager.exe`

**Phương pháp 2: Từ mã nguồn**
1. Mở Command Prompt hoặc PowerShell
2. Điều hướng đến thư mục này
3. Chạy: `python gui_script.py`

**Phương pháp 3: Tệp batch**
1. Double-click `run_gui.bat`

#### Tính Năng GUI
- **Giao diện thân thiện**: Nút bấm và chỉ báo trực quan dễ sử dụng
- **Chọn đường dẫn**: Duyệt và chọn thư mục cài đặt VALORANT
- **Kiểm tra tệp**: Xác minh tất cả tệp cần thiết có sẵn
- **Đầu ra thời gian thực**: Xem tiến trình và kết quả trong cửa sổ đầu ra
- **Thanh tiến trình**: Chỉ báo trực quan về tiến trình hoạt động
- **Xử lý lỗi**: Thông báo lỗi rõ ràng và xác nhận
- **Tính năng an toàn**: Hộp thoại xác nhận trước khi thực hiện thay đổi

#### Sử Dụng GUI
1. **Khởi chạy ứng dụng** bằng một trong các phương pháp trên
2. **Đọc thông báo đóng góp** xuất hiện trong cửa sổ popup
3. **Chọn đường dẫn cài đặt VALORANT** bằng nút Browse
4. **Kiểm tra tệp** để xác minh mọi thứ đã sẵn sàng
5. **Áp dụng Mature Content** để sao chép tệp và bật mature content

### 💻 Sử Dụng Phiên Bản Non-GUI

#### Cách Chạy
**Phương pháp 1: Tệp thực thi**
1. Double-click `NON_GUI.exe`

**Phương pháp 2: Script Python**
1. Mở terminal/command prompt
2. Điều hướng đến thư mục dự án
3. Chạy: `python script.py`

### 📁 Tệp Bắt Buộc

Đảm bảo bạn có các tệp dữ liệu cần thiết trong thư mục `data`:
- `MatureData-WindowsClient.pak`
- `MatureData-WindowsClient.sig`
- `MatureData-WindowsClient.ucas`
- `MatureData-WindowsClient.utoc`

### 📋 Hướng Dẫn Thiết Lập

1. **Cập nhật VALORANT**: Đảm bảo bạn đã nhấn nút **CẬP NHẬT** trong trò chơi (khuyến nghị tắt Tự động Cập nhật cho VALORANT)

2. **Xác minh tệp dữ liệu**: Đảm bảo tất cả tệp cần thiết có trong thư mục `data`

3. **Chọn phương pháp**: Chạy phiên bản GUI hoặc Non-GUI tùy theo sở thích

### ⚠️ Lưu Ý Quan Trọng

**Cảnh báo Windows Defender**: Nếu Windows Defender SmartScreen xuất hiện, nhấp "More info" rồi "Run anyway". Đây là cảnh báo sai - các tệp không có hại. Bạn có thể kiểm tra mã nguồn để xác minh.

### 📜 Tuyên Bố Miễn Trừ Trách Nhiệm

**TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM:** TÔI SẼ KHÔNG CHỊU TRÁCH NHIỆM NẾU TÀI KHOẢN CỦA BẠN BỊ CẤM DO SỬ DỤNG CÔNG CỤ NÀY. TÔI ĐÃ SỬ DỤNG KỂ TỪ THÁNG 9 NĂM 2022 MÀ KHÔNG CÓ VẤN ĐỀ GÌ.

- Việc sửa đổi tệp trò chơi có thể dẫn đến việc đình chỉ tài khoản
- Các tệp dữ liệu trong dự án này được lấy từ tài khoản Riot hợp lệ từ Singapore
- Sử dụng tự chịu rủi ro

### 🤝 Đóng Góp

**Tạo bởi:** @l1ttled1no

**Hỗ trợ nhà phát triển:**
- Chuyển khoản ngân hàng (Việt Nam): dinong175 (MB Bank) | 593895 (OCB)
- PayPal (Toàn cầu): duynguyendang04@gmail.com
- Đăng ký YouTube: [youtube.com/@l1ttled1no](https://youtube.com/@l1ttled1no)

Mọi đóng góp đều được đánh giá cao! ⭐

---

**Created by:** @l1ttled1no | **Give a Star ⭐ if you found this project interesting!**