import { Link, Outlet } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import { performLogout } from "./slice/authSlice";
import { useNavigate } from "react-router";

export default function Layout() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isLoggedIn, isLoggingOut } = useSelector((state: any) => state.auth);

  const onLogout = async () => {
    try {
      navigate('/')
      await dispatch<any>(performLogout()).unwrap();
      window.location.reload();
    } catch (err) {
      // optionally show error
      console.error("Logout failed", err);
      window.alert("Logout failed");
    }
  };

  return (
    <>
      {isLoggingOut ? (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(255,255,255,0.9)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ marginBottom: 8 }}>Logging out...</div>
          </div>
        </div>
      ) : (
      <>
      <div>
        <nav>
          <ul style={{ display: 'flex', justifyContent:'end', gap: '20px', padding: '10px', backgroundColor: '#f0f0f0', paddingRight: 80 }}>
            <li><Link to="/">Home</Link></li>
            { !isLoggedIn ? (
              <>
                <li><Link to="/login">Login</Link></li>
                <li><Link to="/register">Register</Link></li>
              </>
            ) : (
              <>
                <li><Link to="/profile">Profile</Link></li>
                <li>
                  <button style={{cursor: "pointer"}} onClick={onLogout}>Logout</button>
                </li>
              </>
            )}
          </ul>
        </nav>
      </div>
      <div>
        <Outlet />
      </div>
      </>
      )}    
    </>
  );
}