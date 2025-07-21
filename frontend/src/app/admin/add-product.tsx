// app/admin/add-product.tsx
"use client";

import { useState } from "react";
import { revalidatePath } from "next/cache";
import styles from "./Admin.module.css";
import { Product } from "@/lib/types";

async function addProduct(formData: FormData) {
  const product: Omit<Product, "id"> = {
    name: formData.get("name") as string,
    price: parseFloat(formData.get("price") as string),
    description: formData.get("description") as string,
    category: (formData.get("category") as "electronics" | "clothing" | "books") || undefined,
    stock_quantity: parseInt(formData.get("stock_quantity") as string) || 0,
    image_url: formData.get("image_url") as string || "/placeholder.jpg",
    is_active: formData.get("is_active") === "on",
  };

  const response = await fetch("/api/products", {
    method: "POST",
    body: JSON.stringify(product),
    headers: { "Content-Type": "application/json" },
  });

  if (response.ok) revalidatePath("/products");
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
        <input type="text" name="name" placeholder="Название" required className={styles.input} />
        <input type="number" name="price" placeholder="Цена" step="0.01" required className={styles.input} />
        <input type="text" name="description" placeholder="Описание" className={styles.input} />
        <select name="category" className={styles.input}>
          <option value="">Выберите категорию</option>
          <option value="electronics">Электроника</option>
          <option value="clothing">Одежда</option>
          <option value="books">Книги</option>
        </select>
        <input type="number" name="stock_quantity" placeholder="Количество на складе" className={styles.input} />
        <input type="text" name="image_url" placeholder="URL изображения" className={styles.input} />
        <label>
          <input type="checkbox" name="is_active" /> Активен
        </label>
        <button type="submit" className={styles.button}>
          Добавить
        </button>
      </form>
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
}