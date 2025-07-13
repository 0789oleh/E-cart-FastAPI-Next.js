import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { email, password } = await request.json();

  // Пример: запрос к бэкенду для проверки учетных данных
  const res = await fetch("backend:8000/users/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (res.ok) {
    const data = await res.json();
    // Установить сессию (например, с помощью cookies или NextAuth.js)
    return NextResponse.json({ success: true });
  } else {
    const error = await res.json();
    return NextResponse.json({ message: error.message }, { status: res.status });
  }
}