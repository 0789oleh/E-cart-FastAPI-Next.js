import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const { name, email, password } = await request.json();

  // Пример: запрос к бэкенду для создания пользователя
  const res = await fetch("backend:8000/users/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });

  if (res.ok) {
    return NextResponse.json({ success: true });
  } else {
    const error = await res.json();
    return NextResponse.json({ message: error.message }, { status: res.status });
  }
}