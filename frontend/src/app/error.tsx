// app/error.tsx
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./error.module.css";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  const router = useRouter();
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    console.error("Error occurred:", error.message, error.stack);
    // Определение темы
    setIsDarkMode(window.matchMedia("(prefers-color-scheme: dark)").matches);
  }, [error]);

  const handleReset = () => {
    reset();
  };

  const handleGoHome = () => {
    router.push("/");
  };

  const handleGoToCart = () => {
    router.push("/cart");
  };

  return (
    <div className={`${styles.container} ${isDarkMode ? styles.dark : ""}`}>
      <h1 className={styles.title}>Ой, что-то пошло не так!</h1>
      <p className={styles.message}>
        Произошла ошибка: {error.message || "Unexpected "}
      </p>
      {process.env.NODE_ENV === "development" && (
        <p className={styles.stack}>Стек вызовов: {error.stack}</p>
      )}
      <div className={styles.actions}>
        <button onClick={handleReset} className={styles.button}>
          Попробовать снова
        </button>
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