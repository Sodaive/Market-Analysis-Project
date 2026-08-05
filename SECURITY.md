# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

اگر آسیب‌پذیری امنیتی پیدا کردید، لطفاً از طریق ایمیل زیر گزارش دهید:

**security@map-engine.local**

(برای پروژه‌های عمومی، به جای ایمیل می‌توانید از GitHub Security Advisories استفاده کنید)

ما در غضون ۴۸ ساعت به گزارش شما پاسخ خواهیم داد و در صورت تایید، در طول ۷ روزه 패چ را منتشر می‌کنیم.

## Security Best Practices

### متغیرهای محیطی
- توکن‌های API در فایل `.env` ذخیره می‌شوند (نه در کد)
- فایل `.env` در `.gitignore` قرار دارد
- توکن‌ها هرگز در لاگ‌ها یا خروجی‌ها نمایش داده نمی‌شوند

### تعامل با APIها
- تمام درخواست‌ها با HTTPS انجام می‌شوند
- Timeout برای تمام درخواست‌ها تنظیم شده (20 ثانیه)
- Rate limiting سمت کلاینت (DELAY_SEC = 0.1 ثانیه)

### داده‌ها
- داده‌های تاریخی فقط به صورت محلی (CSV) ذخیره می‌شوند
- هیچ داده حساس کاربری جمع‌آوری نمی‌شود
- خروجی‌ها فقط شامل داده‌های بازار عمومی هستند

## Dependency Security

```bash
# بررسی آسیب‌پذیری‌ها
pip audit

# به‌روزرسانیDependencies
pip install --upgrade -r requirements.txt
```

## Reporting

برای گزارش مشکلات امنیتی، لطفاً Issue با برچسب `security` باز کنید یا مستقیماً ایمیل بفرستید.