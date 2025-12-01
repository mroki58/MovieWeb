import { useParams, useNavigate } from "react-router";
import { useEffect } from "react";
import { gql} from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";

const USER_QUERY = gql`
  query User($id: ID!) {
    user(id: $id) {
      id
      username
      me
      isFriend
      friendRequestFromMe
      friendRequestToMe
      favoriteMovies { position movie { id title } }
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

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4">Error: {error.message}</div>;
  const user = data?.user;
  if (!user) return <div className="p-4">User not found</div>;

  useEffect(() => {
    // if the fetched user object indicates it's the viewer, redirect to /profile
    if (user && user.me) {
      navigate('/profile');
    }
  }, [user, navigate]);

  const onInvite = async () => { await friendRequest({ variables: { friend: user.username } }); refetch(); };
  const onAccept = async () => { await accept({ variables: { friend: user.username } }); refetch(); };
  const onReject = async () => { await reject({ variables: { friend: user.username } }); refetch(); };
  const onDelete = async () => { await del({ variables: { friend: user.username } }); refetch(); };

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-3">{user.username}</h1>

      <div className="mb-4">
        {user.me ? (
          <span className="px-2 py-1 bg-gray-200 rounded">This is you</span>
        ) : user.isFriend ? (
          <>
            <button onClick={onDelete} className="p-2 bg-red-500 text-white rounded">Remove friend</button>
          </>
        ) : user.friendRequestToMe ? (
          <>
            <button onClick={onAccept} className="p-2 bg-green-600 text-white rounded mr-2">Accept</button>
            <button onClick={onReject} className="p-2 bg-gray-400 text-white rounded">Reject</button>
          </>
        ) : user.friendRequestFromMe ? (
          <button className="p-2 bg-yellow-400 text-black rounded">Invite sent</button>
        ) : (
          <button onClick={onInvite} className="p-2 bg-blue-600 text-white rounded">Send friend request</button>
        )}
      </div>

      <section>
        <h2 className="text-xl font-semibold">Favorite movies</h2>
        <ol className="list-decimal ml-6">
          {user.favoriteMovies.map((fm:any) => (
            <li key={fm.movie.id}>{fm.movie.title} (place {fm.position})</li>
          ))}
        </ol>
      </section>
    </main>
  );
}
