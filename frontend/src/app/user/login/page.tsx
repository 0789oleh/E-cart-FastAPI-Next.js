// app/user/login/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import styles from "./Login.module.css";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        router.push("/user/profile"); // Редирект на страницу профиля
      } else {
        const data = await res.json();
        setError(data.message || "Ошибка входа");
      }
    } catch (err) {
      setError("Произошла ошибка. Попробуйте снова.");
    }
  };

  return (
    <div className={styles.container}>
      <h1>Вход</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.field}>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className={styles.input}
          />
        </div>
        <div className={styles.field}>
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className={styles.input}
          />
        </div>
        {error && <p className={styles.error}>{error}</p>}
        <button type="submit" className={styles.submitButton}>
          Войти
        </button>
      </form>
      <p className={styles.link}>
        Нет аккаунта? <Link href="/user/register">Зарегистрироваться</Link>
      </p>
    </div>
  );
}