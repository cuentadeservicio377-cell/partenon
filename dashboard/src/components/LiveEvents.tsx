"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

type LiveEventsProps = {
  apiUrl: string;
};

export function LiveEvents({ apiUrl }: LiveEventsProps) {
  const router = useRouter();

  useEffect(() => {
    let es: EventSource | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

    function connect() {
      es = new EventSource(`${apiUrl}/api/v1/stream`, {
        withCredentials: true,
      });

      es.addEventListener('stream.connected', () => {
        // Connection handshake; no action needed.
      });

      es.addEventListener('mission.created', () => router.refresh());
      es.addEventListener('mission.updated', () => router.refresh());
      es.addEventListener('mission.deleted', () => router.refresh());
      es.addEventListener('cron.created', () => router.refresh());
      es.addEventListener('cron.updated', () => router.refresh());
      es.addEventListener('cron.deleted', () => router.refresh());
      es.addEventListener('event.created', () => router.refresh());

      es.onerror = () => {
        if (es?.readyState === EventSource.CLOSED) {
          if (reconnectTimer) clearTimeout(reconnectTimer);
          reconnectTimer = setTimeout(connect, 3000);
        }
      };
    }

    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      es?.close();
    };
  }, [apiUrl, router]);

  return null;
}
