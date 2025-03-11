# buildozer.spec

[app]
title = MatCoin  # Название приложения
package.name = MatCoin  # Имя пакета (без пробелов)
package.domain = org.example  # Домен (замени на свой)
source.include_exts = py,png,jpg,kv,atlas

# Основной Python-файл приложения
source.main = app.py

# Версия и версия кода
version = 1.0.0
version_code = 1

# Поддерживаемые архитектуры
android.archs = arm64-v8a, armeabi-v7a

# Разрешения
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# Python и зависимости
requirements = python3, kivy

# Выходной формат
android.p4a_dir = .p4a
android.p4a_whl_dir = .whl
android.p4a_bootstrap = sdl2
android.ndk = 23b
android.api = 31
android.minapi = 21

# Опции сборки
p4a.branch = master
android.accept_sdk_license = True
