// app/page.tsx
"use client";
import Link from "next/link";
import { fetchProducts } from "@/lib/api";
import { Product } from "@/lib/types";
import { useEffect, useState } from "react";

export default function Home() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const loadProducts = async () => {
      const products = await fetchProducts();
      setFeaturedProducts(products.slice(0, 3)); // Берем первые 3 товара как популярные
    };
    loadProducts();

    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % 3); // Смена слайдов каждые 5 секунд
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const slides = [
    {
      title: "Добро пожаловать в E-Cart",
      description: "Откройте уникальные коллекции с вдохновением от природы и традиций",
      image: "/banner1.jpg",
    },
    {
      title: "Эксклюзивные товары",
      description: "Редкие дизайны только для вас",
      image: "/banner2.jpg",
    },
    {
      title: "Поддержите местных производителей",
      description: "Каждая покупка — вклад в будущее",
      image: "/banner3.jpg",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Баннер */}
      <div className="relative w-full h-96 overflow-hidden">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`absolute w-full h-full transition-opacity duration-1000 ${
              index === currentSlide ? "opacity-100" : "opacity-0"
            }`}
            style={{ backgroundImage: `url(${slide.image})`, backgroundSize: "cover" }}
          >
            <div className="flex items-center justify-center h-full bg-black bg-opacity-50 text-white">
              <div className="text-center">
                <h1 className="text-4xl font-bold mb-4">{slide.title}</h1>
                <p className="text-xl mb-6">{slide.description}</p>
                <Link href="/products" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                  Смотреть каталог
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

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