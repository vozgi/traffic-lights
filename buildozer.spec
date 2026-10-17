[app]
title = Traffic Lights World
package.name = trafficlights
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 2.0

requirements = python3==3.11.9,kivy==2.3.0,cython==0.29.36

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b
p4a.branch = master

