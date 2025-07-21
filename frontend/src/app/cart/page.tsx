"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';// Предполагаемый хелпер для проверки сессии
import { fetchProduct, fetchCart, addToCart, removeFromCart } from "@/lib/api"; // API-функции для корзины
import styles from "./Cart.module.css";

interface CartItem {
  productId: string;
  name: string;
  price: number;
  image: string;
  quantity: number;
}

export default function CartPage() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Загрузка корзины при монтировании
  useEffect(() => {
    const loadCart = async () => {
      setLoading(true);
      try {
        const session = await getServerSession(authOptions);
        let items: CartItem[] = [];

        if (session) {
          // Если пользователь авторизован, загружаем корзину с бэкенда
          const cart = await fetchCart(session.user?.id) 
        } else {
          // Для гостей: загружаем из localStorage
          const localCart = localStorage.getItem("cart");
          items = localCart ? JSON.parse(localCart) : [];
        }

        setCartItems(items);
      } catch (error) {
        console.error("Ошибка загрузки корзины:", error);
      } finally {
        setLoading(false);
      }
    };

    loadCart();
  }, []);

  const handleAddItem = async (productId: string, quantity: number = 1) => {
  try {
    const session = await getServerSession(authOptions);
    if (session) {
      const cartId = (await fetchCart(session.user?.id)).id; // Получи из бэкенда или состояния (например, fetchCart)
      const product = await fetchProduct(productId); // Предполагаемая функция для получения продукта
      const newCartItem = {
        cart_id: cartId,
        product_id: parseInt(productId),
        price_per_unit: product.price || 0,
        quantity,
      };
      const addedItemRaw = await addToCart(newCartItem); // Добавляем товар в корзину на бэкенде
      const addedItem: CartItem = {
        productId: String(addedItemRaw.product_id ?? productId),
        name: product.name ?? "",
        price: addedItemRaw.price_per_unit ?? product.price ?? 0,
        image: product.image_url ?? "",
        quantity: addedItemRaw.quantity ?? quantity,
      };
      setCartItems((prevItems) => [...prevItems, addedItem]); // Обновляем с данными от бэкенда
    } else { 
      const newItem: CartItem = {
        productId: productId,
        name: "", // Можно добавить логику для получения имени
        price: 0, // Замени на реальную цену, если доступна
        image: "", // Можно добавить логику для получения изображения
        quantity,
      };
      const updatedItems = [...cartItems, newItem];
      localStorage.setItem("cart", JSON.stringify(updatedItems));
      setCartItems(updatedItems);
    }
  } catch (error) {
    console.error("Ошибка добавления товара:", error);
  }
};

  // Обновление количества товара
  const handleUpdateQuantity = async (productId: string, quantity: number) => {
    if (quantity < 1) return;
    const session = await getServerSession(authOptions);

    const updatedItems = cartItems.map((item) =>
      item.productId === productId ? { ...item, quantity } : item
    );
    setCartItems(updatedItems);

    if (session) {
      // Синхронизация с бэкендом
      const cartId = (await fetchCart(session.user?.id)).id;
      const product = await fetchProduct(productId);
      const updatedCartItem = {
        cart_id: cartId,
        product_id: parseInt(productId),
        price_per_unit: product.price || 0,
        quantity,
      };
      await addToCart(updatedCartItem);
    } else {
      // Обновление в localStorage
      localStorage.setItem("cart", JSON.stringify(updatedItems));
    }
  };

  // Удаление товара из корзины
  const handleRemoveItem = async (productId: string) => {
    const session = await getServerSession(authOptions);
    const updatedItems = cartItems.filter((item) => item.productId !== productId);
    setCartItems(updatedItems);

    if (session) {
      // Удаление на бэкенде
      await removeFromCart(session.userId, productId);
    } else {
      // Обновление в localStorage
      localStorage.setItem("cart", JSON.stringify(updatedItems));
    }
  };

  // Подсчёт общей стоимости
  const total = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  if (loading) {
    return <div className={styles.container}>Загрузка...</div>;
  }

  return (
    <div className={styles.container}>
      <h1>Корзина</h1>
      {cartItems.length > 0 ? (
        <div className={styles.cart}>
          <ul className={styles.itemList}>
            {cartItems.map((item) => (
              <li key={item.productId} className={styles.item}>
                <img
                  src={item.image || "/placeholder.jpg"}
                  alt={item.name}
                  className={styles.image}
                />
                <div className={styles.details}>
                  <Link href={`/products/${item.productId}`}>
                    <h2 className={styles.itemName}>{item.name}</h2>
                  </Link>
                  <p className={styles.itemPrice}>{item.price} ₽</p>
                  <div className={styles.quantity}>
                    <button
                      onClick={() =>
                        handleUpdateQuantity(item.productId, item.quantity - 1)
                      }
                      disabled={item.quantity <= 1}
                      className={styles.quantityButton}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button
                      onClick={() =>
                        handleUpdateQuantity(item.productId, item.quantity + 1)
                      }
                      className={styles.quantityButton}
                    >
                      +
                    </button>
                  </div>
                  <p className={styles.itemTotal}>
                    Итого: {item.price * item.quantity} ₽
                  </p>
                  <button
                    onClick={() => handleAddItem(item.productId)}
                    className={styles.addButton}
                  >
                    Добавить ещё
                  </button>
                  <button
                    onClick={() => handleRemoveItem(item.productId)}
                    className={styles.removeButton}
                  >
                    Удалить
                  </button>
                </div>
              </li>
            ))}
          </ul>
          <div className={styles.summary}>
            <h2>Итого: {total} ₽</h2>
            <Link href="/checkout" className={styles.checkoutButton}>
              Оформить заказ
            </Link>
          </div>
        </div>
      ) : (
        <p className={styles.empty}>Ваша корзина пуста.</p>
      )}
      <Link href="/products" className={styles.backLink}>
        Продолжить покупки
      </Link>
    </div>
  );
}