export enum OrderStatus {
  PENDING = "pending",
  PROCESSING = "processing",
  SHIPPED = "shipped",
  DELIVERED = "delivered",
  CANCELLED = "cancelled",
}

export interface Order {
  id: number;
  user_id: number;
  status: OrderStatus;
  total_amount: number;
  delivery_address: string;
  customer_notes?: string;
  created_at: Date;
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  price_per_unit: number;
}


export interface User {
  id: string; // UUID
  full_name: string;
  password: string; // На фронте не храним, только для бэка
  phone_number: string;
  is_active: boolean;
}


// lib/api.ts или types.d.ts
export interface Product {
  id: number;
  name: string;
  price: number;
  description?: string;
  category?: "electronics" | "clothing" | "books";
  stock_quantity?: number;
  image_url?: string;
  is_active?: boolean;
}


// lib/api.ts
export interface Cart {
  id: string; // UUID
  user_id?: number | null; // Nullable для гостей
  items: CartItem[]; // Добавляем массив элементов корзины
}

export interface CartItem {
  id: string; // UUID
  cart_id: string;
  product_id: number;
  quantity: number;
  price_per_unit: number;
}