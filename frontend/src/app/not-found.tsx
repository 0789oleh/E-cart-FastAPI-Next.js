"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./error.module.css";



export default function NotFound() {
  const router = useRouter();
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    console.error("Error 404 occurred:");
    // Определение темы
    setIsDarkMode(window.matchMedia("(prefers-color-scheme: dark)").matches);
  },[]);

  const handleGoHome = () => {
    router.push("/");
  };

  const handleGoToCart = () => {
    router.push("/cart");
  };

  return (
    <div className={`${styles.container} ${isDarkMode ? styles.dark : ""}`}>
      <h1 className={styles.title}>Ой, а документ не документ!</h1>
      <p className={styles.message}>
        Страница, которую вы ищете, не найдена. Возможно, она была удалена или перемещена.
      </p>
      {process.env.NODE_ENV === "development" && (
        <p className={styles.stack}>Сhech if the URL correct</p>
      )}
      <div className={styles.actions}>
        <button onClick={handleGoHome} className={styles.button}>
          На главную
        </button>
        <button onClick={handleGoToCart} className={styles.button}>
          В корзину
        </button>
      </div>
    </div>
  );
}