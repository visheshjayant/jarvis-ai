[app]

title = JARVIS AI
package.name = jarvisai
package.domain = org.vishesh

source.dir = .
source.main = jarvis_pro.py

source.include_exts = py,png,jpg,jpeg,kv,atlas,mp4
source.include_patterns = *.mp4

version = 0.1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
