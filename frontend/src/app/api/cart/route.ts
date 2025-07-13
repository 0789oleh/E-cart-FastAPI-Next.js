// app/api/cart/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  try {
    const res = await fetch(`http://backend:8000/cart`, {
      headers: {
        "Authorization": `Bearer ${request.headers.get("authorization")}`,
      },
    });
    if (!res.ok) throw new Error("Failed to fetch cart");
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const { productId, quantity } = await request.json();
    if (!productId || quantity < 1) throw new Error("Product ID and positive quantity are required");
    const res = await fetch(`http://backend:8000/cart/items`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${request.headers.get("authorization")}`,
      },
      body: JSON.stringify({ productId, quantity }),
    });
    if (!res.ok) throw new Error("Failed to add item to cart");
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 400 });
  }
}

export async function PUT(request: Request) {
  try {
    const { productId, quantity } = await request.json();
    if (quantity < 1) throw new Error("Quantity must be positive");
    const res = await fetch(`http://backend:8000/cart/items/${productId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${request.headers.get("authorization")}`,
      },
      body: JSON.stringify({ productId, quantity }),
    });
    if (!res.ok) throw new Error("Failed to update cart item");
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 400 });
  }
}

export async function DELETE(request: Request) {
  try {
    const { productId } = await request.json();
    const res = await fetch(`http://backend:8000/cart/items/${productId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${request.headers.get("authorization")}`,
      },
    });
    if (!res.ok) throw new Error("Failed to remove cart item");
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: (error as Error).message }, { status: 400 });
  }
}