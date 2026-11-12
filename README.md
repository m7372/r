# 🎬 Savita Media Viewer

موقع ويب لتشفير/فك تشفير طلبات Savita API، مع دعم PWA وسجل محلي.

## 🌐 الموقع
https://USERNAME.github.io/REPO-NAME/

## ✨ الميزات
- 🔐 تشفير AES-128-ECB + RSA + MD5 في المتصفح
- 🧩 3 أوضاع: Cloudflare Worker / Python Backend / Direct
- 💾 سجل محلي (localStorage) مع تصدير JSON
- 📱 PWA قابل للتثبيت
- 🤖 CI/CD عبر GitHub Actions
- ✅ اختبارات JS + Python

## 🚀 النشر السريع

### الموقع (GitHub Pages)
1. ارفع الملفات
2. Settings → Pages → Source: **Deploy from a branch** → **main / root**
3. انتظر دقيقة → الموقع جاهز

### Cloudflare Worker
1. https://workers.cloudflare.com → Create Worker
2. الصق `worker/worker.js` → Deploy
3. انسخ الرابط → ضعه في الموقع

### Python Backend (Render)
1. render.com → New Web Service
2. اربط المستودع → يقرأ `backend/render.yaml` تلقائياً
3. انسخ الرابط → ضعه في الموقع

## ⚠️ ملاحظة
للاستخدام التعليمي فقط.
