"use client";

import dynamic from "next/dynamic";

const LazyMap = dynamic(() => import("../../components/MapLeaflet"), {
  ssr: false,
  loading: () => <p>Loading...</p>,
});

export default function Home() {
  return (
    <main>
      <LazyMap />
    </main>
  );
}
