# 🛡️ JOO AI DARK - Vercel & GitHub Deployment Guide

مشروع **JOO AI DARK** مهيأ الآن بنسبة 100% للرفع على **GitHub** والربط مع **Vercel** بضغطة زر واحدة!

---

## 🚀 طريقة الرفع على GitHub والربط بـ Vercel:

### الخطوة 1: الرفع على GitHub (من جهازك)
افتح مجلد المشروع في الـ Terminal أو VS Code:
```bash
git init
git add .
git commit -m "Initial commit - JOO AI DARK for Vercel"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/joo-ai-dark.git
git push -u origin main
```
*(أو يمكنك سحب الملفات يدوياً وإفلاتها في موقع GitHub في مستودع جديد).*

---

### الخطوة 2: الربط بـ Vercel
1. ادخل على حسابك في **[Vercel.com](https://vercel.com)**.
2. اضغط **Add New...** ➔ **Project**.
3. اختر مستودع **`joo-ai-dark`** من GitHub واضغط **Import**.
4. (اختياري) في قسم **Environment Variables**، يمكنك إضافة:
   - `GEMINI_API_KEY`: مفتاح الـ API الخاص بـ Gemini (أو يمكنك إدخاله لاحقاً مباشرة من واجهة الموقع عبر زر "ربط الـ AI").
5. اضغط **Deploy**!

خلال أقل من 30 ثانية سيعطيك Vercel رابطاً رسمياً وشغالاً عالمياً بشهادة SSL مثل:
👉 `https://joo-ai-dark.vercel.app`

---

## 🛠️ كيف تم تجهيز المشروع لـ Vercel؟

1. **`vercel.json`:** ملف التوجيه والـ Rewrites لربط الـ Frontend مع دوال البايثون السحابية (Serverless Functions).
2. **`api/index.py`:** كود السيرفر السحابي المتوافق مع معايير Vercel Python Runtime لمعالجة الشات وفحص الـ SSL والهيدرز والهاشات.
3. **حفظ المحادثات (Dual Persistence):**
   - حفظ محلي في `localStorage` بالمتصفح ليضمن عدم ضياع أي شات على Vercel Serverless.
   - دعم قاعدة بيانات SQLite (`database.py`) أثناء التشغيل على السيرفرات الخاصة أو أجهزة الكمبيوتر.
4. **توصيل الـ AI الحي:**
   - يمكنك ربط Google Gemini أو Groq LLaMA عبر زر `[ربط الـ AI]` من الواجهة وسيعمل مباشرة على Vercel.
