from typing import Dict, Any

# Vietnamese translations
vi = {
    "common": {
        "login": "Đăng nhập",
        "logout": "Đăng xuất",
        "username": "Tên đăng nhập",
        "password": "Mật khẩu",
        "welcome": "Xin chào",
        "role": "Vai trò",
        "submit": "Gửi",
        "cancel": "Hủy",
        "save": "Lưu",
        "add": "Thêm",
        "edit": "Sửa",
        "delete": "Xóa",
        "success": "Thành công",
        "error": "Lỗi",
        "select_language": "Chọn ngôn ngữ"
    },
    "navigation": {
        "main": "Trang chính",
        "admin": "Quản trị",
        "medical": "Y tế",
        "psychology": "Tâm lý",
        "students": "Sinh viên",
        "veterans": "Cựu chiến binh",
        "data_import": "Nhập Dữ Liệu"
    },
    "roles": {
        "admin": "Quản trị viên",
        "doctor": "Bác sĩ",
        "teacher": "Giáo viên",
        "counselor": "Tư vấn viên"
    },
    "login": {
        "title": "Đăng nhập",
        "success": "Đăng nhập thành công!",
        "error": "Tên đăng nhập hoặc mật khẩu không đúng"
    },
    "dashboard": {
        "admin": {
            "title": "Bảng Điều Khiển Quản Trị",
            "welcome": "Chào mừng đến với bảng điều khiển quản trị. Sử dụng thanh bên để điều hướng đến các phần khác nhau."
        },
        "doctor": {
            "title": "Bảng Điều Khiển Y Tế",
            "welcome": "Truy cập hồ sơ y tế và thông tin bệnh nhân thông qua menu bên."
        },
        "teacher": {
            "title": "Bảng Điều Khiển Giáo Viên",
            "welcome": "Xem và quản lý thông tin sinh viên bằng menu bên."
        },
        "counselor": {
            "title": "Bảng Điều Khiển Tư Vấn",
            "welcome": "Truy cập đánh giá tâm lý và thông tin hỗ trợ sinh viên."
        }
    },
    "students": {
        "title": "Quản Lý Sinh Viên",
        "list_title": "Danh Sách Sinh Viên",
        "add_title": "Thêm Sinh Viên Mới",
        "fields": {
            "full_name": "Họ và tên",
            "birth_date": "Ngày sinh",
            "address": "Địa chỉ",
            "email": "Email",
            "admission_date": "Ngày nhập học",
            "health_status": "Tình trạng sức khỏe",
            "academic_status": "Tình trạng học tập"
        },
        "health_status_options": ["Tốt", "Bình thường", "Cần chú ý"],
        "academic_status_options": ["Xuất sắc", "Tốt", "Trung bình", "Cần cải thiện"]
    },
    "veterans": {
        "title": "Quản Lý Cựu Chiến Binh",
        "list_title": "Danh Sách Cựu Chiến Binh",
        "add_title": "Thêm Cựu Chiến Binh Mới",
        "fields": {
            "full_name": "Họ và tên",
            "birth_date": "Ngày sinh",
            "service_period": "Thời gian phục vụ",
            "health_condition": "Tình trạng sức khỏe",
            "address": "Địa chỉ",
            "contact_info": "Thông tin liên hệ"
        }
    }
}

# English translations
en = {
    "common": {
        "login": "Login",
        "logout": "Logout",
        "username": "Username",
        "password": "Password",
        "welcome": "Welcome",
        "role": "Role",
        "submit": "Submit",
        "cancel": "Cancel",
        "save": "Save",
        "add": "Add",
        "edit": "Edit",
        "delete": "Delete",
        "success": "Success",
        "error": "Error",
        "select_language": "Select Language"
    },
    "navigation": {
        "main": "Main",
        "admin": "Admin",
        "medical": "Medical",
        "psychology": "Psychology",
        "students": "Students",
        "veterans": "Veterans",
        "data_import": "Data Import"
    },
    "roles": {
        "admin": "Administrator",
        "doctor": "Doctor",
        "teacher": "Teacher",
        "counselor": "Counselor"
    },
    "login": {
        "title": "Login",
        "success": "Login successful!",
        "error": "Invalid username or password"
    },
    "dashboard": {
        "admin": {
            "title": "Admin Dashboard",
            "welcome": "Welcome to the admin dashboard. Use the sidebar to navigate to different sections."
        },
        "doctor": {
            "title": "Medical Dashboard",
            "welcome": "Access medical records and patient information through the sidebar menu."
        },
        "teacher": {
            "title": "Teacher Dashboard",
            "welcome": "View and manage student information using the sidebar menu."
        },
        "counselor": {
            "title": "Counselor Dashboard",
            "welcome": "Access psychological evaluations and student support information."
        }
    },
    "students": {
        "title": "Student Management",
        "list_title": "Student List",
        "add_title": "Add New Student",
        "fields": {
            "full_name": "Full Name",
            "birth_date": "Birth Date",
            "address": "Address",
            "email": "Email",
            "admission_date": "Admission Date",
            "health_status": "Health Status",
            "academic_status": "Academic Status"
        },
        "health_status_options": ["Good", "Fair", "Needs Attention"],
        "academic_status_options": ["Excellent", "Good", "Average", "Needs Improvement"]
    },
    "veterans": {
        "title": "Veteran Management",
        "list_title": "Veteran List",
        "add_title": "Add New Veteran",
        "fields": {
            "full_name": "Full Name",
            "birth_date": "Birth Date",
            "service_period": "Service Period",
            "health_condition": "Health Condition",
            "address": "Address",
            "contact_info": "Contact Information"
        }
    }
}

class Translator:
    def __init__(self):
        self.translations = {
            'vi': vi,
            'en': en
        }
        self.current_language = 'vi'  # Default language

    def set_language(self, language: str):
        if language in self.translations:
            self.current_language = language

    def get_text(self, key_path: str, default: str = None) -> str:
        """
        Get translated text using dot notation for nested keys
        Example: translator.get_text('common.login')
        """
        keys = key_path.split('.')
        value = self.translations[self.current_language]

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default if default is not None else key_path

        return value

# Create a global translator instance
translator = Translator()

# Helper function to get current language
def get_current_language() -> str:
    return translator.current_language

# Helper function to set language
def set_language(language: str):
    translator.set_language(language)

# Helper function to get text
def get_text(key_path: str, default: str = None) -> str:
    return translator.get_text(key_path, default)