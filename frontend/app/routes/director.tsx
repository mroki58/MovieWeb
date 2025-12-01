import { useParams, Link } from "react-router";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";

const DIRECTOR_MOVIES = gql`
  query DirectorMovies($directorId: ID!) {
    directorsMovies(directorId: $directorId) {
      id
      title
    }
  }
`;

const DIRECTOR_DATA = gql`
  query Director($id: ID!) {
    director(id: $id) {
      fullname
    }
  }
`;

export default function DirectorPage() {
  const { id } = useParams();
  const { data: moviesData, loading: moviesLoading, error: moviesError } = useQuery(DIRECTOR_MOVIES, { variables: { directorId: id } });
  const { data: directorData, loading: directorLoading, error: directorError } = useQuery(DIRECTOR_DATA, { variables: { id } });

  if (moviesLoading || directorLoading) return <div className="p-4">Loading...</div>;
  if (moviesError) return <div className="p-4">Error: {moviesError.message}</div>;
  if (directorError) return <div className="p-4">Error: {directorError.message}</div>;

  const movies = moviesData?.directorsMovies || [];
  const director = directorData?.director || {};

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-3">{director.fullname}</h1>
      <div className="mb-4 text-sm text-gray-700">ID: {id}</div>

      <h2 className="text-xl font-semibold mb-2">Movies</h2>
      <ul className="list-disc ml-6">
        {movies.map((m: any) => (
          <li key={m.id}>
            <Link to={`/movie/${m.id}`}>{m.title}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
