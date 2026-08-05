# Contributing to MAP Engine

مشارکت در پروژه MAP Engine بسیار ساده و خوش‌آمد است!

## چطور مشارکت کنیم؟

1. **Fork** ریپازیتوری
2. **Branch** جدید بسازید: `git checkout -b feature/amazing-feature`
3. **Commit** تغییرات: `git commit -m 'Add amazing feature'`
4. **Push** به برنچ: `git push origin feature/amazing-feature`
5. **Pull Request** باز کنید

## استانداردهای کد

- **Python 3.11+** با type hints
- **Black** برای فرمت‌بندی: `black Engine/`
- **Type hints** برای توابع جدید
- **Docstring** برای توابع عمومی
- **Logging** به جای print

## تست

```bash
# اجرای تست‌ها (وقتی اضافه شوند)
python -m pytest tests/

# چک فرمت‌بندی
black --check Engine/

# چک نوع‌ها
mypy Engine/
```

## استانداردهای کامیت

```
feat: ویژگی جدید
fix: رفع باگ
docs: تغییرات مستندات
refactor: بازنویسی کد
test: اضافه/تغییر تست
chore: کارهای نگهداری
```

مثال: `feat: add MACD fallback for gold/dollar`

## گزارش باگ

لطفاً در Issue شامل موارد زیر باشید:
- نسخه Python
- سیستم عامل
- مراحل تکرار باگ
- لاگ‌های خطا
- رفتار مورد انتظار vs واقعی

## درخواست ویژگی

برای ویژگی‌های جدید، ابتدا Issue باز کنید تا طراحی بررسی شود.