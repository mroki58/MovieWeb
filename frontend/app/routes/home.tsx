import type { Route } from "./+types/home";
import { gql } from "@apollo/client";
import { useQuery } from "@apollo/client/react";
import MovieCard from "../components/MovieCard";
import ListSection from "../components/ListSection";
import AsyncSelect from "react-select/async";
import { useState } from "react";
import { useApolloClient } from "@apollo/client/react";
import { useNavigate } from "react-router";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "MovieWeb" },
    { name: "description", content: "MovieWeb - newest and recommended movies" },
  ];
}

const NEW_MOVIES = gql`
  query NewMovies($limit: Int) {
    newMovies(limit: $limit) {
      id
      title
      year
      genre
    }
  }
`;

const RECOMMENDED = gql`
  query Recommended($userId: ID) {
    recommendedMovies(userId: $userId) {
      id
      title
      year
      genre
    }
  }
`;

export default function Home() {
  const { data: newestData } = useQuery(NEW_MOVIES, { variables: { limit: 10 } });
  const { data: recData } = useQuery(RECOMMENDED, { variables: { userId: null } });
  const client = useApolloClient();
  const navigate = useNavigate();
  const [kind, setKind] = useState<'movie'|'actor'|'user'>('movie');

  const loadSearch = async (inputValue: string) => {
    if (!inputValue || inputValue.length < 2) return [];
    if (kind === 'movie') {
      const res = await client.query({ query: gql`query S($prefix:String){ searchMovies(prefix:$prefix){ id title } }`, variables:{ prefix: inputValue } });
      return (res.data.searchMovies || []).map((m:any) => ({ value: m.id, label: m.title }));
    }
    if (kind === 'actor') {
      const res = await client.query({ query: gql`query S($prefix:String){ searchActors(prefix:$prefix){ id fullname } }`, variables:{ prefix: inputValue } });
      return (res.data.searchActors || []).map((a:any) => ({ value: a.id, label: a.fullname }));
    }
    // user
    const res = await client.query({ query: gql`query S($prefix:String){ searchUsers(prefix:$prefix){ id username } }`, variables:{ prefix: inputValue } });
    return (res.data.searchUsers || []).map((u:any) => ({ value: u.id, label: u.username }));
  };

  const onSelect = (opt:any) => {
    if(!opt) return;
    const id = opt.value;
    if(kind === 'movie') navigate(`/movie/${id}`);
    else if(kind === 'actor') navigate(`/actor/${id}`);
    else navigate(`/user/${id}`);
  };

  const newest = newestData?.newMovies || [];
  const recommended = recData?.recommendedMovies || [];

  return (
    <main className="container mx-auto p-4">
      <div className="mb-6 flex gap-3 items-center">
        <select value={kind} onChange={(e) => setKind(e.target.value as any)} className="p-2 border rounded">
          <option value="movie">Movie</option>
          <option value="actor">Actor</option>
          <option value="user">User</option>
        </select>
        <div style={{ minWidth: 300 }}>
          <AsyncSelect cacheOptions loadOptions={loadSearch} onChange={onSelect} isClearable placeholder={`Search ${kind} by prefix...`} />
        </div>
      </div>
      <ListSection title="Najnowsze filmy">
        {newest.map((m: any) => (
          <MovieCard key={m.id} movie={m} />
        ))}
      </ListSection>

      <ListSection title="Filmy polecane">
        {recommended.map((m: any) => (
          <MovieCard key={m.id} movie={m} />
        ))}
      </ListSection>
    </main>
  );
}
