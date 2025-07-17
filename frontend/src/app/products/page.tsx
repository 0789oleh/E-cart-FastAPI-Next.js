import Link from "next/link";
import { fetchProducts } from "@/lib/api";
import styles from "./Products.module.css";
import { Product } from "@/lib/api"; // Импортируй интерфейс

export default async function ProductsPage() {
  const products = await fetchProducts();

  return (
    <div className={styles.container}>
      <h1>Каталог товаров</h1>
      <div className={styles.grid}>
        {products.length > 0 ? (
          products.map((product: Product) => (
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