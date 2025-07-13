import NextAuth from 'next-auth/react';

export async function getSession() {
    // Пример: получение сессии из cookies или контекста
    const session = await NextAuth.getSession(); 
    return session || null;
  }