// app/user/profile/page.tsx
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';// Предполагаемый хелпер для проверки сессии
import { fetchUserData } from '@/lib/api'; // Функция для получения данных пользователя
import Link from 'next/link';
import styles from './Profile.module.css'; // Стили (если используешь CSS Modules)

export default async function ProfilePage() {
  // Проверка авторизации
  const session = await getServerSession(authOptions);
  if (!session) {
    redirect('/user/login'); // Редирект на страницу логина, если пользователь не авторизован
  }

  // Получение данных пользователя с бэкенда
  const user = await fetchUserData(session.user?.email || '');

  return (
    <div className={styles.container}>
      <h1>Профиль пользователя</h1>
      <section className={styles.profileInfo}>
        <h2>Личная информация</h2>
        <p><strong>Имя:</strong> {user.name || 'Не указано'}</p>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Адрес:</strong> {user.address || 'Не указано'}</p>
        <Link href="/user/profile/edit" className={styles.editButton}>
          Редактировать профиль
        </Link>
      </section>

      <section className={styles.orderHistory}>
        <h2>История заказов</h2>
        {user.orders && user.orders.length > 0 ? (
          <ul className={styles.orderList}>
            {user.orders.map((order: any) => (
              <li key={order.id} className={styles.orderItem}>
                <Link href={`/orders/${order.id}`}>
                  Заказ #{order.id} от {new Date(order.date).toLocaleDateString()}
                </Link>
                <p>Статус: {order.status}</p>
                <p>Сумма: {order.total} ₽</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>У вас пока нет заказов.</p>
        )}
      </section>

      <section className={styles.actions}>
        <button
          onClick={async () => {
            await fetch('/api/auth/logout', { method: 'POST' });
            redirect('/user/login');
          }}
          className={styles.logoutButton}
        >
          Выйти
        </button>
      </section>
    </div>
  );
}