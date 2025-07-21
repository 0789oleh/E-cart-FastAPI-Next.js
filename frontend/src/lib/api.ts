import { Product, Cart, CartItem, Order, OrderItem, OrderStatus, User } from "./types";

export async function fetchUserData(userId: string) {
  const res = await fetch(`/api/user/${userId}`, {
    headers: { 'Content-Type': 'application/json' },
  });
  const data = await res.json();
  return data;
}

export async function fetchProducts(): Promise<Product[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/products`);
  if (!res.ok) throw new Error("Failed to fetch products");
  return await res.json();
}

export async function fetchProduct(productId: string): Promise<Product> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/products/${productId}`);
  if (!res.ok) throw new Error("Failed to fetch product");
  return await res.json();
}

export async function addProduct(product: Omit<Product, "id">): Promise<Product> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/products`, {
    method: "POST",
    body: JSON.stringify(product),
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to add product");
  return await res.json();
}

export async function deleteProduct(id: number): Promise<boolean> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/products/${id}`, {
    method: "DELETE",
  });
  return res.ok;
}

export async function fetchCart(userId?: number): Promise<Cart> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/carts?user_id=${userId}`);
  if (!res.ok) throw new Error("Failed to fetch cart");
  const data = await res.json();
  return { id: data.id, user_id: data.user_id, items: data.items || [] };
}


export async function addToCart(cartItem: Omit<CartItem, "id">): Promise<CartItem> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/cart-items`, {
    method: "POST",
    body: JSON.stringify(cartItem),
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to add to cart");
  return await res.json();
}

export async function fetchOrders(userId: number): Promise<Order[]> {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const res = await fetch(`${baseUrl}/api/orders?user_id=${userId}`);
  if (!res.ok) throw new Error("Failed to fetch orders");
  return await res.json();
}
// lib/api.ts
export async function fetchProductById(id: string) {
  const res = await fetch(`/api/products/${id}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) return null;
  const data = await res.json();
  return data.product || null;
}



export async function removeFromCart(userId: string, productId: string) {
  await fetch(`/api/cart/${userId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId }),
  });
}