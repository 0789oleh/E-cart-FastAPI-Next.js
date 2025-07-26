"uase client";
import Link from "next/link";
import { useEffect, useState } from "react";
import BannerImage1 from './banner1.jpg';
import BannerImage2 from './banner2.jpeg';


const Banner = () => {

    const [currentSlide, setCurrentSlide] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentSlide((prev) => (prev + 1) % 3);
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    const slides = [
    {
      title: "Акція на електроінструменти!",
      description: "Знижки до 40% на інструменти від нашого партнера!",
      image: BannerImage1,
    },
    {
      title: "Подобається великий теніс?",
      description: "Наші спеціалісти влаштують Вам його на задньому дворі!",
      image: BannerImage2,
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
        </div>
    );

}

export default Banner;