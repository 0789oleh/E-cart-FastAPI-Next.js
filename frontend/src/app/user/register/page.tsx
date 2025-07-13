// app/user/register/page.tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import styles from "./Register.module.css";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      if (res.ok) {
        router.push("/user/login"); // Редирект на логин после регистрации
      } else {
        const data = await res.json();
        setError(data.message || "Ошибка регистрации");
      }
    } catch (err) {
      setError("Произошла ошибка. Попробуйте снова.");
    }
  };

  return (
    <div className={styles.container}>
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.field}>
          <label htmlFor="name">Имя</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className={styles.input}
          />
        </div>
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
          Зарегистрироваться
        </button>
      </form>
      <p className={styles.link}>
        Уже есть аккаунт? <Link href="/user/login">Войти</Link>
      </p>
    </div>
  );
}