// app/products/page.tsx
import Link from "next/link";
import { fetchProducts } from "@/lib/api"; // Функция для получения списка продуктов
import styles from "./Products.module.css";

export default async function ProductsPage() {
  // Получение списка продуктов с бэкенда
  const products = await fetchProducts();

  return (
    <div className={styles.container}>
      <h1>Каталог товаров</h1>
      <div className={styles.grid}>
        {products.length > 0 ? (
          products.map((product: any) => (
            <div key={product.id} className={styles.card}>
              <Link href={`/products/${product.id}`}>
                <img
                  src={product.image || "/placeholder.jpg"}
                  alt={product.name}
                  className={styles.image}
                />
                <h2 className={styles.title}>{product.name}</h2>
                <p className={styles.price}>{product.price} ₽</p>
              </Link>
              <button
                onClick={() => {
                  // Логика добавления в корзину (например, через глобальное состояние или API)
                  console.log(`Добавлен в корзину: ${product.name}`);
                }}
                className={styles.addButton}
              >
                Добавить в корзину
              </button>
            </div>
          ))
        ) : (
          <p>Товары не найдены.</p>
        )}
      </div>
    </div>
  );
}