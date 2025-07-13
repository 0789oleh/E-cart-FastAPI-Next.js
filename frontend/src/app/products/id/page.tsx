// app/products/[id]/page.tsx
import { notFound } from "next/navigation";
import { fetchProductById } from "@/lib/api"; // Функция для получения продукта по ID
import styles from "./Product.module.css";

export default async function ProductPage({ params }: { params: { id: string } }) {
  // Получение данных продукта по ID
  const product = await fetchProductById(params.id);

  if (!product) {
    notFound(); // Показать 404, если продукт не найден
  }

  return (
    <div className={styles.container}>
      <div className={styles.product}>
        <img
          src={product.image || "/placeholder.jpg"}
          alt={product.name}
          className={styles.image}
        />
        <div className={styles.details}>
          <h1 className={styles.title}>{product.name}</h1>
          <p className={styles.price}>{product.price} ₽</p>
          <p className={styles.description}>{product.description || "Нет описания"}</p>
          <button
            onClick={() => {
              // Логика добавления в корзину
              console.log(`Добавлен в корзину: ${product.name}`);
            }}
            className={styles.addButton}
          >
            Добавить в корзину
          </button>
        </div>
      </div>
    </div>
  );
}