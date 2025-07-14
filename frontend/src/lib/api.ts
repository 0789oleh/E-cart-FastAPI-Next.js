export async function fetchUserData(userId: string) {
  const res = await fetch(`/api/user/${userId}`, {
    headers: { 'Content-Type': 'application/json' },
  });
  const data = await res.json();
  return data;
}

export async function fetchProducts() {
  const res = await fetch("/api/products", {
    headers: { "Content-Type": "application/json" },
  });
  const data = await res.json();
  return data.products || [];
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