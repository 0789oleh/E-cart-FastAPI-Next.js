// app/admin/page.tsx
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import AddProductForm from "./add-product";
import DeleteProduct from "./delete-product";
import styles from "./Admin.module.css";

export default async function AdminPage() {
  const session = await getServerSession(authOptions);
  if (!session || !session.user?.email?.endsWith("@admin.com")) {
    return <div>Доступ запрещён. Только для администраторов.</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Панель администрирования</h1>
      <AddProductForm />
      <DeleteProduct />
    </div>
  );
}