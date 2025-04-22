# ecommerce
This project is a special project developed for an online store, that is, for e-commerce.



### Hozirgi modellar nimalarni qamrab oladi?
✅ Oddiy onlayn do‘kon uchun kerakli asoslar:

User: Foydalanuvchilar (oddiy va adminlar)

Product, Category: Mahsulotlar va toifalar

Cart, CartItem: Savatcha va mahsulotlar

Order, OrderItem: Buyurtmalar

Payment: To‘lovlar

Review: Fikr-mulohazalar

## 🔸 Kengroq e-commerceuchun nima kerak bo‘ladi?

1. 🏬 Seller (sotuvchi) tizimi
Har bir foydalanuvchi mahsulot sotishi mumkin.

SellerProfile model: do‘kon nomi, tasviri, reytingi va boshqalar.

2. 🖼️ Mahsulotga ko‘proq media
ProductImage model: har bir mahsulotga bir nechta rasm/video yuklash.

3. 📦 Ombor (stock management)
Mahsulot har bir hududda mavjud yoki yo‘qligini ko‘rsatish.

Inventory modeli orqali boshqarish.

4. 🧾 Invoice va To‘lov tarixi
Har bir to‘lov uchun hujjat (PDF yoki ma’lumotlar).

PaymentHistory modeli.

5. 🚚 Yetkazib berish (Delivery/Shipping)
Yetkazib beruvchi xizmat, narx, taxminiy vaqt.

ShippingMethod, DeliveryStatus kabi modellar.

6. 📢 Kupon/Promo kodlar
Chegirmalar yoki promo kodlar.

Coupon, Discount modellari.

7. 🧑‍💼 Admin panel uchun alohida funksiya
Barcha mahsulotlar, foydalanuvchilar, buyurtmalarni boshqarish.

8. 📊 Statistika va analitika
Adminlar yoki sotuvchilar uchun grafiklar, sotuvlar statistikasi.

9. 🌐 Ko‘p til va ko‘p valyuta qo‘llab-quvvatlash
Translation va Currency modellar orqali amalga oshiriladi.

10. ❤️ Wishlist yoki Favorites
Foydalanuvchilar yoqtirgan mahsulotlarini saqlashi.

### Har bir modelning vazifalari

cart.py
→ Cart modeli: foydalanuvchining xarid savati haqida ma'lumotlarni saqlaydi.

cart_item.py
→ CartItem modeli: xarid savatidagi mahsulotlar ro‘yxatini saqlaydi.

category.py
→ Category modeli: mahsulot kategoriyalari bilan ishlaydi.

coupon.py
→ Coupon modeli: chegirmali kuponlar haqidagi ma'lumotlarni saqlaydi.

inventory.py
→ Inventory modeli: mahsulot zaxiralari (ombor holati)ni saqlaydi.

invoice.py
→ Invoice modeli: foydalanuvchiga yuborilgan hisob-faktura (invoice) ma’lumotlarini saqlaydi.

order.py
→ Order modeli: foydalanuvchi bergan buyurtmalar haqidagi umumiy ma'lumotlar.

order_item.py
→ OrderItem modeli: buyurtmadagi alohida mahsulotlarni ifodalaydi.

payment.py
→ Payment modeli: to‘lovlar haqida umumiy ma'lumotlarni saqlaydi.

payment_history.py
→ PaymentHistory modeli: foydalanuvchining to‘lovlar tarixini yozadi.

product.py
→ Product modeli: mahsulotlar haqida asosiy ma'lumotlarni saqlaydi.

product_media.py
→ ProductImage modeli: mahsulotga tegishli rasm yoki videolarni saqlaydi.

review.py
→ Review modeli: foydalanuvchilarning mahsulot haqidagi izohlari va reytinglarini saqlaydi.

seller.py
→ SellerProfile modeli: sotuvchining profil va ma'lumotlarini saqlaydi.

shipping.py
→ ShippingMethod modeli: yetkazib berish usullari va tafsilotlarini ifodalaydi.

translation.py
→ ProductTranslation modeli: mahsulotlarning ko‘p tilli tarjimalarini saqlaydi.

user.py
→ User modeli: foydalanuvchilar haqida umumiy ma’lumotlarni saqlaydi (login, email, h.k.).

wishlist.py
→ Wishlist modeli: foydalanuvchining “xohlovchilar ro‘yxati”dagi mahsulotlarni saqlaydi.

