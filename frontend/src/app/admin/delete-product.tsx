// app/admin/delete-product.tsx
"use client"; // Клиентский компонент

import { useState, useEffect } from "react";
import { fetchProducts } from "@/lib/api";
import styles from "./Admin.module.css";
import { revalidatePath } from "next/cache";

async function deleteProduct(id: number) {
  const response = await fetch(`/api/products/${id}`, {
    method: "DELETE",
  });
  if (response.ok) revalidatePath("/products"); // Обновляем кэш
  return response.ok;
}

export default function DeleteProduct() {
  const [products, setProducts] = useState<any[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadProducts() {
      const data = await fetchProducts();
      setProducts(data);
    }
    loadProducts();
  }, []);

  const handleDelete = async (id: number) => {
    const success = await deleteProduct(id);
    setMessage(success ? "Товар удалён!" : "Ошибка удаления.");
    if (success) setProducts(products.filter((p) => p.id !== id));
  };

  return (
    <div className={styles.section}>
      <h2 className={styles.subtitle}>Удалить товар</h2>
      {products.length > 0 ? (
        <ul className={styles.list}>
          {products.map((product) => (
            <li key={product.id} className={styles.item}>
              {product.name}
              <button
                onClick={() => handleDelete(product.id)}
                className={styles.deleteButton}
              >
                Удалить
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>Нет товаров для удаления.</p>
      )}
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}