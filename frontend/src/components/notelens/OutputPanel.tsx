import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Download, Copy, Check } from "lucide-react";
import { toast } from "sonner";

type Props = {
  topics: string;
  filtered: string;
  loading: boolean;
  error: string | null;
};

const sanitize = (text: string) => {
  return text
    .replace(/^You are a precision academic parser\..*$/gm, "")
    .replace(/^You are an inclusive academic filter.*$/gm, "")
    .replace(/^===.*===$/gm, "")
    .trim();
};

const generateReport = (topics: string, filtered: string) => {
  const cleanTopics = sanitize(topics);
  const cleanFiltered = sanitize(filtered);

  return `# CodeLens Relevancy Report\n\n## Identified Syllabus Topics\n${cleanTopics}\n\n---\n\n## Filtered Study Notes\n${cleanFiltered}`;
};

export function OutputPanel({ topics, filtered, loading, error }: Props) {
  const [copied, setCopied] = useState(false);
  const empty = !loading && !error && !topics && !filtered;

  const handleCopy = async () => {
    try {
      const content = generateReport(topics, filtered);
      await navigator.clipboard.writeText(content);
      setCopied(true);
      toast.success("Copied to clipboard");
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error("Failed to copy");
    }
  };

  const handleDownload = () => {
    const content = generateReport(topics, filtered);
    const blob = new Blob([content], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `codelens-report-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section
      className="relative rounded-md border border-border bg-card"
      style={{ boxShadow: "var(--shadow-paper)" }}
    >
      <header className="flex items-baseline justify-between border-b border-border px-6 py-4">
        <div className="flex items-baseline gap-3">
          <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-accent">03</span>
          <h2 className="font-display text-3xl">Filtered Output</h2>
        </div>
        <div className="flex items-center gap-4">
          {(topics || filtered) && (
            <>
              <button
                onClick={handleCopy}
                aria-label="Copy filtered notes to clipboard"
                className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
              >
                {copied ? (
                  <Check size={14} aria-hidden="true" className="text-accent" />
                ) : (
                  <Copy size={14} aria-hidden="true" />
                )}
                {copied ? "Copied" : "Copy text"}
              </button>
              <button
                onClick={handleDownload}
                aria-label="Download report as Markdown file"
                className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent"
              >
                <Download size={14} aria-hidden="true" />
                Download .md
              </button>
            </>
          )}
          <span className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
            {loading ? "processing…" : filtered ? "complete" : "idle"}
          </span>
        </div>
      </header>

      <div className="grid gap-0 md:grid-cols-2 min-h-[500px]">
        <aside className="border-b border-border bg-secondary/20 p-8 md:border-b-0 md:border-r">
          <div className="sticky top-8">
            <p className="mb-6 font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
              Identified topics
            </p>
            {loading && !topics ? (
              <SkeletonLines n={6} />
            ) : topics ? (
              <div className="prose prose-sm max-w-none prose-headings:font-display prose-headings:text-foreground prose-p:text-foreground/80">
                <ReactMarkdown>{topics}</ReactMarkdown>
              </div>
            ) : (
              <p className="font-mono text-[12px] text-muted-foreground">—</p>
            )}
          </div>
        </aside>

        <article className="p-8">
          <p className="mb-6 font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
            Notes · syllabus-relevant only
          </p>
          {error ? (
            <div className="rounded border border-destructive/40 bg-destructive/5 p-4 font-mono text-[12px] text-destructive">
              {error}
            </div>
          ) : loading && !filtered ? (
            <SkeletonLines n={14} />
          ) : filtered ? (
            <div className="prose prose-sm max-w-none prose-headings:font-display prose-headings:text-foreground prose-p:text-foreground/80 prose-p:leading-relaxed">
              <ReactMarkdown>{filtered}</ReactMarkdown>
            </div>
          ) : empty ? (
            <p className="font-display text-xl italic text-muted-foreground">
              Your filtered notes will appear here.
            </p>
          ) : null}
        </article>
      </div>
    </section>
  );
}

function SkeletonLines({ n }: { n: number }) {
  return (
    <div className="space-y-2" role="status" aria-label="Loading content">
      {Array.from({ length: n }).map((_, i) => (
        <div
          key={i}
          className="h-3 animate-pulse rounded bg-muted"
          style={{ width: `${60 + ((i * 13) % 40)}%` }}
        />
      ))}
    </div>
  );
}
