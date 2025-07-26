// app/page.tsx
"use client";
import Link from "next/link";
import { fetchProducts } from "@/lib/api";
import { Product } from "@/lib/types";
import { useEffect, useState } from "react";
import Banner from './components/Banner';

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const loadProducts = async () => {
      const products = await fetchProducts();
      setFeaturedProducts(products.slice(0, 3)); // Берем первые 3 товара как популярные
    };
    loadProducts();
  }, []);



  return (
    <div className="min-h-screen bg-gray-100">
      {/* Баннер */}
      <Banner/>

      {/* Категории */}
      <div className="container mx-auto py-12 px-4">
        <h2 className="text-3xl font-semibold text-center mb-8">Категории</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <Link href="/products?category=electronics" className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
            <h3 className="text-xl font-medium">Электроника</h3>
          </Link>
          <Link href="/products?category=clothing" className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
            <h3 className="text-xl font-medium">Одежда</h3>
          </Link>
          <Link href="/products?category=books" className="bg-white p-6 rounded-lg shadow-lg hover:shadow-xl transition">
            <h3 className="text-xl font-medium">Книги</h3>
          </Link>
        </div>
      </div>

      {/* Популярные товары */}
      <div className="container mx-auto py-12 px-4">
        <h2 className="text-3xl font-semibold text-center mb-8">Популярные товары</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {featuredProducts.map((product) => (
            <div key={product.id} className="bg-white p-4 rounded-lg shadow-lg hover:shadow-xl transition">
              <img
                src={product.image_url || "/placeholder.jpg"}
                alt={product.name}
                className="w-full h-48 object-cover rounded-t-lg"
              />
              <div className="p-4">
                <h3 className="text-lg font-medium">{product.name}</h3>
                <p className="text-gray-600">{product.price} ₽</p>
                <Link href={`/products/${product.id}`} className="mt-2 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                  Подробнее
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Призыв к действию */}
      <div className="bg-blue-600 text-white text-center py-12">
        <h2 className="text-3xl font-bold mb-4">Готовы начать покупки?</h2>
        <p className="mb-6">Зарегистрируйтесь или войдите, чтобы получить доступ к эксклюзивным предложениям!</p>
        <div className="space-x-4">
          <Link href="/auth/register" className="bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-gray-200">
            Регистрация
          </Link>
          <Link href="/auth/login" className="bg-white text-blue-600 px-6 py-3 rounded-lg hover:bg-gray-200">
            Вход
          </Link>
        </div>
      </div>
    </div>
  );
}