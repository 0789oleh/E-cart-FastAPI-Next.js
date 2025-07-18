// app/admin/add-product.tsx
"use client"; // Клиентский компонент для формы

import { useState } from "react";
import { revalidatePath } from "next/cache";
import styles from "./Admin.module.css";

async function addProduct(formData: FormData) {
  const name = formData.get("name") as string;
  const price = parseFloat(formData.get("price") as string);
  const image = formData.get("image") as string || "/placeholder.jpg";

  const response = await fetch("/api/products", {
    method: "POST",
    body: JSON.stringify({ name, price, image }),
    headers: { "Content-Type": "application/json" },
  });

  if (response.ok) revalidatePath("/products"); // Обновляем кэш
  return response.ok;
}

export default function AddProductForm() {
  const [message, setMessage] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const success = await addProduct(formData);
    setMessage(success ? "Товар добавлен!" : "Ошибка добавления.");
  };

  return (
    <div className={styles.section}>
      <h2 className={styles.subtitle}>Добавить товар</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="text"
          name="name"
          placeholder="Название"
          required
          className={styles.input}
        />
        <input
          type="number"
          name="price"
          placeholder="Цена"
          step="0.01"
          required
          className={styles.input}
        />
        <input
          type="text"
          name="image"
          placeholder="URL изображения"
          className={styles.input}
        />
        <button type="submit" className={styles.button}>
          Добавить
        </button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}