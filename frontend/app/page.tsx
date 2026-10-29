import Image from "next/image";
import { Suspense } from "react";

import Content from "@/components/Content";
import { getContent, type ContentItem } from "@/lib/content";

async function ContentList() {
  let items: ContentItem[];
  try {
    items = await getContent();
  } catch {
    return (
      <p role="alert">
        Could not load the content. Check that the backend is running on
        http://localhost:8000.
      </p>
    );
  }

  return (
    <div className="flex w-full flex-col gap-6">
      {items.map((item) => (
        <Content key={item.question} item={item} />
      ))}
    </div>
  );
}

export default function Home() {
  return (
    <main className="mx-auto flex max-w-3xl flex-col items-center gap-8 p-4 sm:p-8">
      <div className="flex flex-col items-center text-center">
        <Image
          src="/logo.png"
          alt="Citizens Advice SORT"
          width={150}
          height={150}
          priority
        />
        <h1 className="mt-4 text-2xl font-bold">Citizens Advice SORT</h1>
        <h2 className="text-lg font-medium">Junior Developer Practical</h2>
      </div>
      {/* Anything that fetches data goes inside Suspense, which shows the fallback until it's ready */}
      <Suspense fallback={<p>Loading...</p>}>
        <ContentList />
      </Suspense>
    </main>
  );
}