import type { ContentItem, Source } from "@/lib/content";

// "consumer_goods_and_services" -> "Consumer goods and services"
function formatCategory(category: string): string {
  const text = category.replaceAll("_", " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function SourceListItem({ source, number }: { source: Source; number: number }) {
  return (
    <li className="flex items-start gap-3">
      {source.favicon ? (
        // A plain <img> is enough for a 16px icon from an external service,
        // so next/image's optimisation and remotePatterns config aren't needed.
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={source.favicon}
          alt=""
          width={16}
          height={16}
          loading="lazy"
          className="mt-1 size-4 shrink-0"
        />
      ) : (
        <span className="mt-1 size-4 shrink-0" aria-hidden="true" />
      )}
      <div className="min-w-0">
        <span className="mr-1 font-semibold">[{number}]</span>
        <a
          href={source.source}
          target="_blank"
          rel="noopener noreferrer"
          className="break-words text-[#004b88] underline"
        >
          {source.title}
        </a>
        {!source.cited && (
          <span className="ml-2 rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-600">
            Not cited in the answer
          </span>
        )}
      </div>
    </li>
  );
}

export default function Content({ item }: { item: ContentItem }) {
  return (
    <article className="w-full rounded-lg bg-white p-4 text-slate-900 shadow-md sm:p-6">
      <p className="text-xs font-semibold tracking-wide text-slate-600 uppercase">
        {formatCategory(item.category)}
      </p>

      <h3 className="mt-4 text-sm font-bold text-slate-600">Question</h3>
      <p className="mt-1 rounded-md bg-slate-100 p-3">{item.question}</p>

      <h3 className="mt-6 text-sm font-bold text-slate-600">Answer</h3>
      {/* The backend escapes all HTML except <b> and its own citation links,
          so this string is safe to render as HTML. */}
      <div
        className="mt-1 leading-relaxed whitespace-pre-line [&_a]:font-semibold [&_a]:text-[#004b88] [&_a]:underline"
        dangerouslySetInnerHTML={{ __html: item.content }}
      />

      <h3 className="mt-6 text-sm font-bold text-slate-600">Sources</h3>
      <ol className="mt-2 space-y-2 text-sm">
        {item.sources.map((source, index) => (
          <SourceListItem key={source.id} source={source} number={index + 1} />
        ))}
      </ol>
    </article>
  );
}