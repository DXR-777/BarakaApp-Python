[app]
title = Baraka Foundation
package.name = baraka
package.domain = org.baraka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المكتبات المطلوبة للعمل
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests,urllib3,android

# الصلاحيات المطلوبة (ستظهر للمستخدم عند فتح التطبيق)
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CALL_PHONE

android.api = 34
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
