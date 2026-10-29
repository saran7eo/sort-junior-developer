export type Source = {
  id: string;
  title: string;
  source: string;
  favicon: string | null;
  cited: boolean;
};

export type ContentItem = {
  category: string;
  question: string;
  sources: Source[];
  content: string;
};

const API_URL = process.env.API_URL ?? "http://localhost:8000";

export async function getContent(): Promise<ContentItem[]> {
  const response = await fetch(`${API_URL}/data`);
  if (!response.ok) {
    throw new Error(`Backend responded with status ${response.status}`);
  }
  return response.json();
}