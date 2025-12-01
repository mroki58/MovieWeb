export default function ListSection({ title, children }: any) {
  return (
    <section className="mb-6">
      <h2 className="text-2xl font-bold mb-3">{title}</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">{children}</div>
    </section>
  );
}
