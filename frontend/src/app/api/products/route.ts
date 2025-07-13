import { NextResponse } from "next/server";
import { getServerSession } from 'next-auth';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get("name") || "";
  const limit = parseInt(searchParams.get("limit") || "10", 10);
  const sort = searchParams.get("sort") || "name";

  // Валидация
  if (isNaN(limit) || limit < 1 || limit > 100) {
    return NextResponse.json({ error: "Недопустимое значение limit" }, { status: 400 });
  }
  if (!["name", "price", "-price"].includes(sort)) {
    return NextResponse.json({ error: "Недопустимое значение sort" }, { status: 400 });
  }

  try {
    const query = new URLSearchParams({ name, limit: limit.toString(), sort }).toString();
    const res = await fetch(`backend:8000/api/products?${query}`, {
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      return NextResponse.json({ error: "Ошибка получения продуктов" }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: "Внутренняя ошибка сервера" }, { status: 500 });
  }
}


export async function PATCH(request: Request, { params }: { params: { productId: string } }) {
  // Проверка авторизации (например, только админ)
  const session = await getServerSession();
  if (!session || !session.user || !session.user.isAdmin) {
    return NextResponse.json({ error: "Доступ запрещён" }, { status: 403 });
  }

  const { name, price, description } = await request.json();

  // Валидация
  if (price && (typeof price !== "number" || price < 0)) {
    return NextResponse.json({ error: "Недопустимая цена" }, { status: 400 });
  }

  try {
    const res = await fetch(`backend:8000/api/products/${params.productId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, price, description }),
    });

    if (!res.ok) {
      return NextResponse.json({ error: "Ошибка обновления продукта" }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json({ success: true, data });
  } catch (error) {
    return NextResponse.json({ error: "Внутренняя ошибка сервера" }, { status: 500 });
  }
}

export async function DELETE(request: Request, { params }: { params: { productId: string } }) {
    const { productId } = await request.json();
    const res = await fetch(`backend:8000/api/products/${params.productId}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ productId }),
    });
    return NextResponse.json({ success: res.ok });
  }