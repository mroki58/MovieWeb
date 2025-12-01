import { useParams, Link } from "react-router";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";

const ACTOR_MOVIES = gql`
  query ActorMovies($actorId: ID!) {
    actorsMovies(actorId: $actorId) {
      id
      title
    }
  }
`;

const ACTOR_DATA = gql`
  query Actor($id: ID!) {
    actor(id: $id) {
      id
      fullname
    }
  }
`;

export default function ActorPage() {
  const { id } = useParams();
  const { data: moviesData, loading: moviesLoading, error: moviesError } = useQuery(ACTOR_MOVIES, { variables: { actorId: id } });
  const { data: actorData, loading: actorLoading, error: actorError } = useQuery(ACTOR_DATA, { variables: { id } });

  if (moviesLoading || actorLoading) return <div className="p-4">Loading...</div>;
  if (moviesError) return <div className="p-4">Error: {moviesError.message}</div>;
  if (actorError) return <div className="p-4">Error: {actorError.message}</div>;

  const movies = moviesData?.actorsMovies || [];
  const actor = actorData?.actor || {};
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-3">{actor.fullname}</h1>
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
