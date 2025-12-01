import { useParams, Link } from "react-router";
import { useState, useEffect } from "react";
import { gql } from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";

const MOVIE_QUERY = gql`
  query Movie($id: ID!) {
    movie(id: $id) {
      id
      title
      year
      rating
      numberOfGrades
      genre
      director { id fullname }
      actors { id fullname }
    }
  }
`;

const ME_QUERY = gql`
  query Me { me { id } }
`;

const RATINGS_BY_USER = gql`
  query Ratings($userId: ID!) {
    ratings(userId: $userId) {
      stars
      movie { id }
    }
  }
`;

const RATE_MOVIE = gql`
  mutation RateMovie($movieId: ID!, $stars: Int!) {
    rateMovie(movieId: $movieId, stars: $stars) { stars movie { id } }
  }
`;

export default function MoviePage() {
  const { id } = useParams();
  const { data, loading, error } = useQuery(MOVIE_QUERY, { variables: { id } });
  const { data: meData } = useQuery(ME_QUERY);
  const userId = meData?.me?.id;
  const { data: ratingsData, refetch: refetchRatings } = useQuery(RATINGS_BY_USER, { variables: { userId }, skip: !userId });
  const [rateMovie] = useMutation(RATE_MOVIE);
  const [myRating, setMyRating] = useState<number | null>(null);

  useEffect(() => {
    if (ratingsData && ratingsData.ratings) {
      const rec = ratingsData.ratings.find((r: any) => r.movie?.id === id);
      setMyRating(rec ? rec.stars : null);
    }
  }, [ratingsData, id]);

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4">Error: {error.message}</div>;

  const movie = data?.movie;
  if (!movie) return <div className="p-4">Movie not found</div>;

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-2">{movie.title}</h1>
      <div className="text-sm text-gray-600 mb-4">{movie.year} • {movie.genre}</div>
      <div className="mb-4">Rating: {movie.rating ?? "—"} ({movie.numberOfGrades ?? 0} votes)</div>

      {userId ? (
        <div className="mb-4">
          <strong>Your rating:</strong>{' '}
          <select value={myRating ?? ''} onChange={(e) => setMyRating(e.target.value === '' ? null : parseInt(e.target.value))} className="ml-2 p-1 border rounded">
            <option value="">—</option>
            {Array.from({ length: 11 }).map((_, i) => (
              <option key={i} value={i}>{i}</option>
            ))}
          </select>
          <button className="ml-3 p-2 bg-blue-600 text-white rounded" onClick={async () => {
            const stars = myRating ?? 0;
            await rateMovie({ variables: { movieId: id, stars } });
            // refetch movie and ratings
            try { await refetchRatings(); } catch {}
          }}>Save</button>
        </div>
      ) : null}

      <div className="mb-4">
        <strong>Director:</strong>{" "}
        {movie.director ? (
          <Link to={`/director/${movie.director.id}`}>{movie.director.fullname}</Link>
        ) : (
          "—"
        )}
      </div>

      <div>
        <strong>Actors:</strong>
        <ul className="list-disc ml-6">
          {movie.actors?.map((a: any) => (
            <li key={a.id}>
              <Link to={`/actor/${a.id}`}>{a.fullname}</Link>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
