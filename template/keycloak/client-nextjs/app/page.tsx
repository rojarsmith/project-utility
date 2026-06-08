'use client';

import { useEffect, useState } from 'react';
import { getKeycloak } from '@/lib/keycloak';

export default function Home() {
  const [userInfo, setUserInfo] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    const kc = getKeycloak();
    kc.init({ checkLoginIframe: false }).then((authenticated) => {
      if (authenticated) {
        setUserInfo(kc.tokenParsed ?? null);
      }
    });
  }, []);

  const handleLogin = () => getKeycloak().login();
  const handleLogout = () => getKeycloak().logout({ redirectUri: window.location.origin });

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <h1 className="text-2xl font-bold mb-6">Learn authentication and authorization with Keycloak</h1>
        <pre className="text-sm bg-zinc-100 dark:bg-zinc-900 rounded p-4 w-full overflow-auto mb-6">
          {JSON.stringify(userInfo, null, 2)}
        </pre>
        <div className="flex gap-4">
          <button
            onClick={handleLogin}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            login
          </button>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-zinc-400 text-white rounded hover:bg-zinc-500"
          >
            logout
          </button>
        </div>
      </main>
    </div>
  );
}
