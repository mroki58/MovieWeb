import { Link } from "react-router";

export default function MovieCard({ movie }: any) {
  return (
    <div className="border rounded p-3 shadow-sm">
      <h3 className="text-lg font-semibold">
        <Link to={`/movie/${movie.id}`}>{movie.title}</Link>
      </h3>
      <div className="text-sm text-gray-600">{movie.year} • {movie.genre}</div>
    </div>
  );
}
