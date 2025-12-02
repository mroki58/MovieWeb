import { useParams, useNavigate, Link } from "react-router";
import { useEffect } from "react";
import { gql} from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";
import { useSelector } from "react-redux";

const USER_QUERY = gql`
  query User($id: ID!) {
    user(id: $id) {
      id
      username
      me
      isFriend
      isPendingFromMe
      isPendingToMe
      favoriteMovies { position movie { id title } }
      friends { id username }
      ratings { stars movie { id title } }
    }
  }
`;

const FRIEND_REQUEST = gql`
  mutation FriendRequest($friend: String!) { friendRequest(friend: $friend) }
`;
const FRIEND_ACCEPT = gql`
  mutation FriendAccept($friend: String!) { friendRequestAccept(friend: $friend) }
`;
const FRIEND_REJECT = gql`
  mutation FriendReject($friend: String!) { friendRequestReject(friend: $friend) }
`;
const DELETE_FRIEND = gql`
  mutation DeleteFriend($friend: String!) { deleteFriend(friend: $friend) }
`;

export default function UserPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, loading, error, refetch } = useQuery(USER_QUERY, { variables: { id } });
  const [friendRequest] = useMutation(FRIEND_REQUEST);
  const [accept] = useMutation(FRIEND_ACCEPT);
  const [reject] = useMutation(FRIEND_REJECT);
  const [del] = useMutation(DELETE_FRIEND);

  const {isLoggedIn} = useSelector((state: any) => state.auth);

  const user = data?.user;

  useEffect(() => {
    if (user && user.me) {
      navigate('/profile');
    }
  }, [user, navigate]);

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4">Error: {error.message}</div>;
  if (!user) return <div className="p-4">User not found</div>;



  const onInvite = async () => { await friendRequest({ variables: { friend: user.username } }); refetch(); };
  const onAccept = async () => { await accept({ variables: { friend: user.username } }); refetch(); };
  const onReject = async () => { await reject({ variables: { friend: user.username } }); refetch(); };
  const onDelete = async () => { await del({ variables: { friend: user.username } }); refetch(); };

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-3">{user.username}</h1>

      <div className="mb-4">
          { 
            isLoggedIn && (
              user.isFriend ? (
                <>
                  <button onClick={onDelete} className="p-2 bg-red-500 text-white rounded">Remove friend</button>
                </>
              ) : user.isPendingToMe ? (
                <>
                  <button onClick={onAccept} className="p-2 bg-green-600 text-white rounded mr-2">Accept</button>
                  <button onClick={onReject} className="p-2 bg-gray-400 text-white rounded">Reject</button>
                </>
              ) : user.isPendingFromMe ? (
                <button className="p-2 bg-yellow-400 text-black rounded">Invite sent</button>
              ) : (
                <button onClick={onInvite} className="p-2 bg-blue-600 text-white rounded">Send friend request</button>
              ))}
      </div>

      <section>
        <h2 className="text-xl font-semibold">Movie Ranking</h2>
        <ol className="list-decimal ml-6">
          {user.favoriteMovies.map((fm:any) => (
            <li key={fm.movie.id}><Link to={`/movie/${fm.movie.id}`}>{fm.movie.title}</Link> (place {fm.position})</li>
          ))}
        </ol>
      </section>

      <section className="text-xl font-semibold">
        <h2 className="text-xl font-semibold mt-6">Friends</h2>
        <ul>
          {user.friends.map((friend:any) => (
            <li key={friend.id}><Link to={`/user/${friend.id}`}>{friend.username}</Link></li>
          ))}
        </ul>
      </section>

      <section className="text-xl font-semibold">
        <h2 className="text-xl font-semibold mt-6">User ratings:</h2>
        <ul className="mt-4">
          {user.ratings.map((r:any) => (
            <li key={r.movie.id}><pre><Link to={`/movie/${r.movie.id}`}>{r.movie.title}</Link>: {r.stars} stars</pre></li>
          ))}
        </ul>
      </section>
    </main>
  );
}
