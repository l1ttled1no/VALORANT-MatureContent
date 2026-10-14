# VALORANT Mature Content Manager

Turn on blood and corpses in VALORANT for accounts where the **Mature Content** option is hidden (Vietnam, Australia, etc.).

**Note:** This project is not affiliated with Riot Games or VALORANT in any way. It is intended for educational purposes only.

**Update:** 15-10-2026 (Patch 13.08)

---

## 🌐 Language / Ngôn ngữ

- [🇺🇸 **English**](#english-version)
- [🇻🇳 **Tiếng Việt**](#phiên-bản-tiếng-việt)

📄 A step-by-step guide with screenshots is in [`docs/HuongDan.docx`](docs/HuongDan.docx) (Vietnamese).

---

## English Version

### 📋 How it works

Blood and corpses need **two things**, and the tool handles both:

1. **Account settings**: the blood and corpse settings are stored on Riot's servers for your account. On VN accounts they are switched off and the in-game option is hidden. The tool switches them on again.
2. **Game files**: the game needs the `MatureData-WindowsClient.*` files. Each time you press Play on a VN account, Riot Client swaps them for `VNGLogo-WindowsClient.*`. The tool puts them back right after Riot Client finishes checking files and before the game loads them.

### 🚀 Quick start

1. Open **Riot Client** and log in.
2. Run `VALORANT-MatureContent-Manager.exe`.
3. Under **② Account settings**, turn on **Show blood** and/or **Show corpses**, then click **Save**. VALORANT must be closed for this step.
4. Leave **Apply automatically when pressing Play** on, and keep the tool open.
5. Press **Play** in Riot Client. The tool swaps the files for you.

You only need to save the account settings once per account. The files have to be swapped each time you play, which is why the tool should stay open.

### 🖥️ The window

| Section | What it shows |
|---|---|
| Top banner | What to do next |
| ① Riot Client | Whether Riot Client is open and which account is logged in |
| ② Account settings | Current blood / corpse state on your account, with switches and a **Save** button |
| ③ Game files | Whether the Mature files are installed, the auto-apply switch and an **Apply now** button |
| Details | A log of everything the tool did |

The **Advanced** menu has: change game folder, restore account settings from a backup, open the backup folder. Each **Save** backs up your previous account settings first. **Language** switches between Tiếng Việt and English.

### 💻 Command line

```
VALORANT-MatureContent-CLI.exe status
VALORANT-MatureContent-CLI.exe enable | disable
VALORANT-MatureContent-CLI.exe blood on|off
VALORANT-MatureContent-CLI.exe corpses on|off
VALORANT-MatureContent-CLI.exe apply [paks_folder]
VALORANT-MatureContent-CLI.exe restore [backup_file]
```

### 🛠️ Running from source / building

```
python app.py                              # GUI
python cli.py status                       # command line
python -m unittest discover -s tests       # tests
pyinstaller VALORANT-MatureContent.spec    # builds both .exe into dist/
```

The sources are organised as follows:
- `core/`: settings API, pak files, game paths and the Riot Client log watcher.
- `app.py`, `theme.py`, `i18n.py`: the GUI.
- `cli.py`: the command-line version.
- `old_script/`: the previous version of the tool.

Python 3.9+ is required, with no third-party packages. PyInstaller is needed only to build.

GitHub Actions ([`.github/workflows/build.yml`](.github/workflows/build.yml)) runs the tests and builds both `.exe` on every push to `main` or `release`, on pull requests into `main`, and when a GitHub Release is published. The artifact contains only `VALORANT-MatureContent-Manager.exe`, `VALORANT-MatureContent-CLI.exe` and `HuongDan.docx`; the data files are bundled inside the `.exe`. A published Release also gets these files attached as a `.zip`.

### 🔄 After a game patch

If the top banner says the Mature files are outdated, or you see grey boxes in game, the files in `data/` no longer match the patch. To get new ones, log in to a non-VN account, let Riot Client update, and copy `MatureData-WindowsClient.*` from `...\VALORANT\live\ShooterGame\Content\Paks` into `data/`. A `data` folder next to the `.exe` takes priority over the bundled one.

### ⚠️ Important notes

- **Windows Defender warning**: if SmartScreen appears, click "More info" → "Run anyway". The source code is available here to check.
- Account settings are saved through Riot's player-preferences service, the same way the crosshair tool [ValorantCC](https://github.com/weedeej/ValorantCC) works.

### 📜 Disclaimer

**I WILL NOT BE RESPONSIBLE IF YOUR ACCOUNT IS BANNED FOR USING THIS TOOL. I HAVE BEEN USING IT SINCE SEPTEMBER 2022 WITHOUT ANY ISSUES.**

- Modification of game files can lead to account suspension
- The data files in this project are obtained from a valid Singapore Riot account
- Use at your own risk

### 🎥 Video tutorials (previous version)

[![How this trick works](https://img.youtube.com/vi/DXQOpayNVkY/maxresdefault.jpg)](https://youtu.be/DXQOpayNVkY)

### 🤝 Contribution

**Created by:** @l1ttled1no

- Bank Transfer (Vietnam): dinong175 (MB Bank) | 593895 (OCB)
- PayPal (Global): duynguyendang04@gmail.com
- YouTube: [youtube.com/@l1ttled1no](https://youtube.com/@l1ttled1no)

---

## Phiên Bản Tiếng Việt

### 📋 Cách hoạt động

Muốn có máu và xác cần **hai thứ**, tool lo cả hai:

1. **Cài đặt tài khoản**: tuỳ chọn máu và xác được lưu trên máy chủ Riot theo tài khoản. Tài khoản VN bị tắt các tuỳ chọn này và bị ẩn chỗ chỉnh trong game. Tool bật lại giúp bạn.
2. **File game**: game cần các file `MatureData-WindowsClient.*`. Mỗi lần bấm Play bằng acc VN, Riot Client đổi chúng thành `VNGLogo-WindowsClient.*`. Tool chép lại ngay sau khi Riot Client kiểm tra file xong, trước khi game nạp file.

### 🚀 Bắt đầu nhanh

1. Mở **Riot Client** và đăng nhập.
2. Chạy `VALORANT-MatureContent-Manager.exe`.
3. Ở mục **② Cài đặt tài khoản**, bật **Hiện máu** và/hoặc **Hiện xác**, rồi bấm **Lưu**. Lúc này VALORANT phải đang tắt.
4. Để nguyên công tắc **Tự động áp dụng khi bấm Play** và giữ tool mở.
5. Bấm **Play** trong Riot Client. Tool sẽ tự chép file.

Mỗi tài khoản chỉ cần lưu cài đặt một lần. Riêng file game phải chép lại mỗi lần chơi, nên cần để tool mở.

### 🖥️ Giao diện

| Mục | Nội dung |
|---|---|
| Dải hướng dẫn trên cùng | Việc cần làm tiếp theo |
| ① Riot Client | Riot Client đã mở chưa, đang đăng nhập tài khoản nào |
| ② Cài đặt tài khoản | Trạng thái máu / xác hiện tại của tài khoản, công tắc bật tắt và nút **Lưu** |
| ③ File game | File Mature đã có chưa, công tắc tự động áp dụng và nút **Áp dụng ngay** |
| Chi tiết | Nhật ký các thao tác của tool |

Menu **Nâng cao** có: đổi thư mục cài game, khôi phục cài đặt tài khoản từ backup, mở thư mục backup. Mỗi lần **Lưu**, tool tự backup cài đặt cũ trước. Menu **Ngôn ngữ** chuyển giữa Tiếng Việt và English.

### 💻 Dòng lệnh

Xem phần [Command line](#-command-line) ở trên, các lệnh giống nhau.

### 🔄 Sau mỗi bản cập nhật game

Có thể file trong `data/` đã cũ so với bản game. Dấu hiệu là dải hướng dẫn báo file Mature đã cũ, hoặc trong game xuất hiện ô xám. Khi đó:
1. Đăng nhập một acc không phải VN.
2. Để Riot Client cập nhật xong.
3. Chép `MatureData-WindowsClient.*` từ `...\VALORANT\live\ShooterGame\Content\Paks` vào thư mục `data/`.

Thư mục `data` đặt cạnh file `.exe` được ưu tiên hơn bản đóng gói sẵn.

### ⚠️ Lưu ý

- **Cảnh báo Windows Defender**: nếu SmartScreen hiện ra, bấm "More info" → "Run anyway". Mã nguồn có sẵn ở đây để bạn kiểm tra.

### 📜 Tuyên bố miễn trừ trách nhiệm

**TÔI SẼ KHÔNG CHỊU TRÁCH NHIỆM NẾU TÀI KHOẢN CỦA BẠN BỊ CẤM DO SỬ DỤNG CÔNG CỤ NÀY. TÔI ĐÃ SỬ DỤNG KỂ TỪ THÁNG 9 NĂM 2022 MÀ KHÔNG CÓ VẤN ĐỀ GÌ.**

- Việc sửa đổi tệp trò chơi có thể dẫn đến việc đình chỉ tài khoản
- Các tệp dữ liệu trong dự án này được lấy từ tài khoản Riot hợp lệ từ Singapore
- Sử dụng tự chịu rủi ro

### 🤝 Đóng góp

**Tác giả:** @l1ttled1no. Thông tin ủng hộ xem ở phần [Contribution](#-contribution) phía trên.
