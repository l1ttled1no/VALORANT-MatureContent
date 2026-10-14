"""UI strings in Vietnamese (default) and English."""

LANGUAGES = {'vi': 'Tiếng Việt', 'en': 'English'}

STRINGS = {
    'vi': {
        'app_title': 'VALORANT Mature Content',
        'subtitle': 'Bật máu và xác cho tài khoản VALORANT bị ẩn tuỳ chọn Mature Content',

        # Guide banner
        'guide_no_client': 'Mở Riot Client và đăng nhập tài khoản của bạn.',
        'guide_not_logged_in': 'Đăng nhập tài khoản trong Riot Client.',
        'guide_game_running': 'VALORANT đang chạy. Tắt game nếu muốn đổi cài đặt máu / xác.',
        'guide_unsaved': 'Bạn đã đổi lựa chọn, bấm "Lưu" để áp dụng cho tài khoản.',
        'guide_data_outdated': 'File Mature trong thư mục data đã cũ so với bản game, hãy tải bản mới của tool.',
        'guide_ready_auto': 'Mọi thứ đã sẵn sàng. Bấm Play trong Riot Client, tool sẽ tự áp dụng file.',
        'guide_ready_manual': 'Bấm "Áp dụng ngay" sau khi Riot Client kiểm tra file xong, rồi vào game.',

        # Step 1
        'step_client': '① Riot Client',
        'client_no_client': 'Chưa mở Riot Client',
        'client_not_logged_in': 'Đang chờ đăng nhập...',
        'client_logged_in': 'Đã đăng nhập: {riot_id}',
        'client_game_running': 'Đã đăng nhập: {riot_id} (VALORANT đang chạy)',

        # Step 2
        'step_account': '② Cài đặt tài khoản',
        'blood': 'Hiện máu',
        'corpses': 'Hiện xác',
        'save': 'Lưu',
        'account_loading': 'Đang đọc cài đặt...',
        'account_saved': 'Đã lưu lên tài khoản',
        'account_unknown': 'Chưa đọc được cài đặt',

        # Step 3
        'step_files': '③ File game',
        'files_ready': 'Đã có file Mature',
        'files_vng': 'Đang là file bản VN (sẽ được thay khi bấm Play)',
        'files_different': 'File Mature khác phiên bản trong data',
        'files_no_paks': 'Không tìm thấy thư mục cài VALORANT',
        'auto_apply': 'Tự động áp dụng khi bấm Play',
        'apply_now': 'Áp dụng ngay',

        # Log / details
        'details': 'Chi tiết',
        'log_auto_on': 'Đã bật tự động áp dụng. Bấm Play trong Riot Client.',
        'log_auto_off': 'Đã tắt tự động áp dụng.',
        'log_play_pressed': 'Đã bấm Play, chờ Riot Client kiểm tra file...',
        'log_repairing': 'Riot Client đang sửa file, chờ lần khởi động tiếp theo...',
        'log_applying': 'Đang chép file Mature...',
        'log_applied': 'Đã áp dụng file Mature.',
        'log_saving': 'Đang lưu Máu: {blood}, Xác: {corpses}...',
        'log_restored': 'Đã khôi phục cài đặt từ {path}',
        'on': 'BẬT',
        'off': 'TẮT',

        # Menus and dialogs
        'menu_advanced': 'Nâng cao',
        'menu_change_path': 'Đổi thư mục cài game...',
        'menu_restore': 'Khôi phục cài đặt tài khoản từ backup',
        'menu_open_backups': 'Mở thư mục backup',
        'menu_language': 'Ngôn ngữ',
        'menu_help': 'Trợ giúp',
        'menu_about': 'Giới thiệu',
        'confirm_restore': 'Khôi phục cài đặt tài khoản về bản backup lúc {date}?',
        'backup_title': 'Khôi phục cài đặt tài khoản',
        'backup_choose': 'Chọn bản backup muốn khôi phục. Mỗi bản ghi lại trạng thái máu / xác của tài khoản trước một lần Lưu.',
        'backup_date': 'Thời điểm',
        'restore': 'Khôi phục',
        'cancel': 'Huỷ',
        'game_path': 'Thư mục game: {path}',
        'not_found': 'chưa tìm thấy',
        'change': 'Đổi...',
        'invalid_paks': 'Thư mục này không phải thư mục Paks của VALORANT.\n\nThư mục đúng có dạng:\n...\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Paks',
        'select_paks': 'Chọn thư mục Paks của VALORANT',
        'about': 'VALORANT Mature Content\n\nTác giả: @l1ttled1no\nhttps://github.com/l1ttled1no\n\nCông cụ không liên quan tới Riot Games.',

        # Tooltips
        'tip_blood': 'Hiện máu khi bắn trúng người chơi.',
        'tip_corpses': 'Giữ lại xác người chơi sau khi bị hạ gục.',
        'tip_save': 'Lưu lựa chọn máu / xác lên tài khoản Riot. Cài đặt cũ được tự động backup trước.',
        'tip_save_no_change': 'Chưa có thay đổi nào để lưu. Gạt công tắc Hiện máu / Hiện xác trước.',
        'tip_save_game_running': 'Hãy tắt VALORANT trước khi lưu, nếu không game sẽ ghi đè cài đặt.',
        'tip_save_no_login': 'Cần mở Riot Client và đăng nhập trước.',
        'tip_auto': 'Theo dõi Riot Client. Khi bạn bấm Play và Riot Client kiểm tra file xong, tool tự chép file Mature trước khi game mở. Hãy để tool mở khi chơi.',
        'tip_apply': 'Chép file Mature vào thư mục game ngay bây giờ. Dùng sau khi Riot Client kiểm tra file xong và trước khi game mở.',
        'tip_apply_auto': 'Đang bật tự động áp dụng nên không cần bấm nút này. Tắt công tắc tự động để dùng.',
        'tip_change': 'Chọn thư mục Paks khác nếu tool tìm sai chỗ cài VALORANT.',
        'tip_details': 'Hiện / ẩn nhật ký thao tác của tool.',
        'tip_credit': 'Mở trang GitHub của tác giả.',
        'tip_open_backups': 'Mở thư mục chứa các file backup trong File Explorer.',
        'tip_restore': 'Ghi bản backup đã chọn lên tài khoản. VALORANT phải đang tắt.',

        # Errors (by exception code)
        'err_no_client': 'Chưa mở Riot Client. Hãy mở và đăng nhập.',
        'err_not_logged_in': 'Riot Client chưa đăng nhập.',
        'err_game_running': 'Hãy tắt VALORANT rồi thử lại (chỉ để Riot Client mở).',
        'err_no_version': 'Chưa tìm thấy phiên bản game. Hãy vào game một lần rồi thử lại.',
        'err_network': 'Không kết nối được tới máy chủ Riot. Kiểm tra mạng rồi thử lại.',
        'err_no_backup': 'Chưa có bản backup nào cho tài khoản này.',
        'err_backup_mismatch': 'Bản backup thuộc tài khoản khác.',
        'err_missing_data': 'Thiếu file trong thư mục data. Hãy tải lại tool.',
        'err_bad_paks': 'Thư mục cài game không hợp lệ. Vào Nâng cao → Đổi thư mục cài game.',
        'err_remove_failed': 'Không xoá được file VNGLogo (game có thể đang chạy).',
        'err_copy_failed': 'Không chép được file Mature (game có thể đang chạy).',
        'err_unknown': 'Có lỗi xảy ra: {message}',
    },
    'en': {
        'app_title': 'VALORANT Mature Content',
        'subtitle': 'Turn on blood and corpses for VALORANT accounts without the Mature Content option',

        'guide_no_client': 'Open Riot Client and log in to your account.',
        'guide_not_logged_in': 'Log in to your account in Riot Client.',
        'guide_game_running': 'VALORANT is running. Close it to change blood / corpse settings.',
        'guide_unsaved': 'You changed the options, click "Save" to apply them to your account.',
        'guide_data_outdated': 'The Mature files in the data folder are older than the game, please get the latest tool.',
        'guide_ready_auto': 'All set. Press Play in Riot Client and the files will be applied automatically.',
        'guide_ready_manual': 'Click "Apply now" after Riot Client finishes checking files, then start the game.',

        'step_client': '① Riot Client',
        'client_no_client': 'Riot Client is not running',
        'client_not_logged_in': 'Waiting for login...',
        'client_logged_in': 'Logged in: {riot_id}',
        'client_game_running': 'Logged in: {riot_id} (VALORANT is running)',

        'step_account': '② Account settings',
        'blood': 'Show blood',
        'corpses': 'Show corpses',
        'save': 'Save',
        'account_loading': 'Reading settings...',
        'account_saved': 'Saved to your account',
        'account_unknown': 'Settings not loaded yet',

        'step_files': '③ Game files',
        'files_ready': 'Mature files installed',
        'files_vng': 'VN files installed (replaced when you press Play)',
        'files_different': 'Mature files differ from the data folder',
        'files_no_paks': 'VALORANT install folder not found',
        'auto_apply': 'Apply automatically when pressing Play',
        'apply_now': 'Apply now',

        'details': 'Details',
        'log_auto_on': 'Auto-apply is on. Press Play in Riot Client.',
        'log_auto_off': 'Auto-apply is off.',
        'log_play_pressed': 'Play pressed, waiting for Riot Client to check files...',
        'log_repairing': 'Riot Client is repairing files, waiting for the next launch...',
        'log_applying': 'Copying Mature files...',
        'log_applied': 'Mature files applied.',
        'log_saving': 'Saving Blood: {blood}, Corpses: {corpses}...',
        'log_restored': 'Restored settings from {path}',
        'on': 'ON',
        'off': 'OFF',

        'menu_advanced': 'Advanced',
        'menu_change_path': 'Change game folder...',
        'menu_restore': 'Restore account settings from backup',
        'menu_open_backups': 'Open backup folder',
        'menu_language': 'Language',
        'menu_help': 'Help',
        'menu_about': 'About',
        'confirm_restore': 'Restore the account settings to the backup from {date}?',
        'backup_title': 'Restore account settings',
        'backup_choose': 'Pick the backup to restore. Each one holds the blood / corpse state of your account before a Save.',
        'backup_date': 'Date',
        'restore': 'Restore',
        'cancel': 'Cancel',
        'game_path': 'Game folder: {path}',
        'not_found': 'not found',
        'change': 'Change...',
        'invalid_paks': 'This is not the VALORANT Paks folder.\n\nThe right folder looks like:\n...\\Riot Games\\VALORANT\\live\\ShooterGame\\Content\\Paks',
        'select_paks': 'Select the VALORANT Paks folder',
        'about': 'VALORANT Mature Content\n\nBy @l1ttled1no\nhttps://github.com/l1ttled1no\n\nNot affiliated with Riot Games.',

        'tip_blood': 'Show blood when players are hit.',
        'tip_corpses': 'Keep player bodies on the ground after they die.',
        'tip_save': 'Save the blood / corpse choice to your Riot account. The old settings are backed up first.',
        'tip_save_no_change': 'Nothing to save yet. Flip Show blood / Show corpses first.',
        'tip_save_game_running': 'Close VALORANT before saving, otherwise the game overwrites your settings.',
        'tip_save_no_login': 'Open Riot Client and log in first.',
        'tip_auto': 'Watches Riot Client. When you press Play and Riot Client has checked the files, the Mature files are copied before the game starts. Keep the tool open while playing.',
        'tip_apply': 'Copy the Mature files into the game folder now. Use it after Riot Client has checked the files and before the game starts.',
        'tip_apply_auto': 'Auto-apply is on, so this button is not needed. Turn auto-apply off to use it.',
        'tip_change': 'Pick another Paks folder if the tool found the wrong VALORANT install.',
        'tip_details': "Show / hide the tool's activity log.",
        'tip_credit': "Open the author's GitHub page.",
        'tip_open_backups': 'Open the folder with the backup files in File Explorer.',
        'tip_restore': 'Write the selected backup to your account. VALORANT must be closed.',

        'err_no_client': 'Riot Client is not running. Please open it and log in.',
        'err_not_logged_in': 'Riot Client is not logged in.',
        'err_game_running': 'Please close VALORANT and try again (keep only Riot Client open).',
        'err_no_version': 'Game version not found. Please launch the game once, then try again.',
        'err_network': "Could not reach Riot's servers. Check your connection and try again.",
        'err_no_backup': 'No backup found for this account yet.',
        'err_backup_mismatch': 'The backup belongs to another account.',
        'err_missing_data': 'Files are missing in the data folder. Please download the tool again.',
        'err_bad_paks': 'Invalid game folder. Go to Advanced → Change game folder.',
        'err_remove_failed': 'Could not remove the VNGLogo files (the game may be running).',
        'err_copy_failed': 'Could not copy the Mature files (the game may be running).',
        'err_unknown': 'Something went wrong: {message}',
    },
}


class Translator:
    def __init__(self, language='vi'):
        self.language = language if language in STRINGS else 'vi'

    def __call__(self, key, **kwargs):
        text = STRINGS[self.language].get(key) or STRINGS['en'].get(key, key)
        return text.format(**kwargs) if kwargs else text

    def error(self, exc):
        """Friendly message for a core exception"""
        code = getattr(exc, 'code', None)
        if code and f'err_{code}' in STRINGS[self.language]:
            return self(f'err_{code}')
        return self('err_unknown', message=str(exc))
