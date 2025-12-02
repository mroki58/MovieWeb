import { useState } from "react";
import { Link } from "react-router";
import { gql } from "@apollo/client";
import { useQuery, useMutation, useApolloClient } from "@apollo/client/react";
import AsyncSelect from "react-select/async";

const ME_QUERY = gql`
  query Me {
    me {
      id
      username
      favoriteMovies { position movie { id title } }
      friends { id username }
      pendingFromMe { id username }
      pendingToMe { id username }
      ratings { stars movie { id title } }
    }
  }
`;

const SEARCH_MOVIES = gql`
  query SearchMovies($prefix: String) {
    searchMovies(prefix: $prefix) {
      id
      title
    }
  }
`;

const MODIFY_RANKING = gql`
  mutation ModifyRanking($places:[Int!]!, $movies:[ID!]!) {
    modifyUserRanking(places: $places, movies: $movies)
  }
`;

const FRIEND_ACCEPT = gql`
  mutation FriendAccept($friend: String!) { friendRequestAccept(friend: $friend) }
`;

const FRIEND_REJECT = gql`
  mutation FriendReject($friend: String!) { friendRequestReject(friend: $friend) }
`;

export default function Profile() {
  const { data, loading, error, refetch } = useQuery(ME_QUERY);
  const client = useApolloClient();
  const [editing, setEditing] = useState(false);
  const [slots, setSlots] = useState<Array<any>>([]);
  const [modifyRanking] = useMutation(MODIFY_RANKING);
  const [accept] = useMutation(FRIEND_ACCEPT);
  const [reject] = useMutation(FRIEND_REJECT);

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4">Error: {error.message}</div>;
  const me = data?.me;
  if (!me) return <div className="p-4">Not logged in</div>;

  const favorite = me.favoriteMovies || [];

  const loadOptions = async (inputValue: string) => {
    if (!inputValue || inputValue.length < 2) return [];
    const res = await client.query({ query: SEARCH_MOVIES, variables: { prefix: inputValue } });
    return (res.data.searchMovies || []).map((m: any) => ({ value: m.id, label: m.title }));
  };

  const startEdit = () => {
    // prepare slots for up to 5 places
    let s = [null, null, null, null, null];
    favorite.forEach((fm: any) => {
      if (fm.position >=1 && fm.position <=5) s[fm.position - 1] = { value: fm.movie.id, label: fm.movie.title };
    });
    setSlots(s);
    setEditing(true);
  };

  const save = async () => {
    const places: number[] = [];
    const movies: string[] = [];
    slots.forEach((s, idx) => {
      if (s) {
        places.push(idx + 1);
        movies.push(s.value);
      }
    });
    try {
      await modifyRanking({ variables: { places, movies } });
      setEditing(false);
      await refetch();
      alert('Ranking updated');
    } catch (e:any) {
      alert('Update failed: ' + e.message);
    }
  };

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-3">My profile — {me.username}</h1>

      <section className="mb-6">
        <h2 className="text-xl font-semibold">Favorite movies</h2>
        {!editing ? (
          <div>
            <ol className="list-decimal ml-6">
              {favorite.map((fm:any) => (
                <li key={fm.movie.id}><Link to={`/movie/${fm.movie.id}`}>{fm.movie.title}</Link></li>
              ))}
            </ol>
            <button onClick={startEdit} className="mt-2 p-2 bg-blue-500 text-white rounded">Edit ranking</button>
          </div>
        ) : (
          <div>
            <div className="grid grid-cols-1 gap-2">
              {slots.map((s:any, idx:number) => (
                <AsyncSelect 
                key={idx} 
                cacheOptions 
                defaultOptions 
                loadOptions={loadOptions} 
                value={s} 
                onChange={(v:any) => { const copy = [...slots]; copy[idx] = v; setSlots(copy); }} 
                placeholder={`Place ${idx+1}`} 
                isClearable
                />
              ))}
            </div>
            <div className="mt-2">
              <button onClick={save} className="p-2 bg-green-600 text-white rounded mr-2">Save</button>
              <button onClick={() => setEditing(false)} className="p-2 bg-gray-400 text-white rounded">Cancel</button>
            </div>
          </div>
        )}
      </section>

      <section className="mb-6">
        <h2 className="text-xl font-semibold">Friends</h2>
        <ul className="list-disc ml-6">
          {(me.friends || []).map((f:any) => (
            <li key={f.id}><Link to={`/user/${f.id}`}>{f.username}</Link></li>
          ))}
        </ul>
      </section>

      <section className="mb-6">
        <h2 className="text-xl font-semibold">Outgoing friend requests</h2>
        <ul className="list-disc ml-6">
          {(me.pendingFromMe || []).map((r:any) => (
            <li key={r.id}>{r.id ? <Link to={`/user/${r.id}`}>{r.username || r.name}</Link> : (r.username || r.name)}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold">Incoming friend requests</h2>
        <ul className="list-disc ml-6">
          {(me.pendingToMe || []).map((r:any) => (
            <li key={r.id} className="flex items-center gap-3">
              <span>{r.id ? <Link to={`/user/${r.id}`}>{r.username || r.name}</Link> : (r.username || r.name)}</span>
              <button onClick={async () => { try { await accept({ variables: { friend: r.username || r.name } }); await refetch(); } catch(e){ alert('Accept failed'); } }} className="p-1 bg-green-600 text-white rounded">Accept</button>
              <button onClick={async () => { try { await reject({ variables: { friend: r.username || r.name } }); await refetch(); } catch(e){ alert('Reject failed'); } }} className="p-1 bg-gray-400 text-black rounded">Reject</button>
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2 className="text-xl font-semibold">My ratings:</h2>
        <ul className="list-disc ml-6">
          {(me.ratings || []).map((r:any) => (
            <li key={r.movie.id}><pre><Link to={`/movie/${r.movie.id}`}>{r.movie.title}</Link>: {r.stars} stars</pre></li>
          ))}
        </ul>
      </section>
    </main>
  );
}
