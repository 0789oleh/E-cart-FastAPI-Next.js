export async function fetchUserData(userId: string) {
  const res = await fetch(`/api/user/${userId}`, {
    headers: { 'Content-Type': 'application/json' },
  });
  const data = await res.json();
  return data;
}

// src/lib/api.ts или в products/page.tsx
export interface Product {
  id: number;
  name: string;
  price: number;
  image?: string;
}

export async function fetchProducts() {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000';
  const res = await fetch(`${baseUrl}/api/products`);
  if (!res.ok) throw new Error('Failed to fetch products: ' + res.statusText);
  return (await res.json()) as Product[];
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

// lib/api.ts
export async function fetchCart(userId: string) {
  const res = await fetch(`/api/cart/${userId}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) return [];
  const data = await res.json();
  return data.cartItems || [];
}

export async function addToCart(userId: string, productId: string, quantity: number) {
  await fetch(`/api/cart/${userId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId, quantity }),
  });
}

export async function removeFromCart(userId: string, productId: string) {
  await fetch(`/api/cart/${userId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ productId }),
  });
}

export async function addProduct(product: Omit<Product, "id">) {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
  const res = await fetch(`${baseUrl}/api/products`, {
    method: "POST",
    body: JSON.stringify(product),
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to add product");
  return res.json();
}

export async function deleteProduct(id: number) {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
  const res = await fetch(`${baseUrl}/api/products/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete product");
  return res.ok;
}