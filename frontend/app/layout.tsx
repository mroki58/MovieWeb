import { Link, Outlet } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "./slice/authSlice";

export default function Layout() {
    const { isLoggedIn } = useSelector((state: any) => state.auth);
    const dispatch = useDispatch();

    const onLogout = () => {
        dispatch(logout());
    }
    return (
        <>
        <div>
            <nav>
                <ul style={{ display: 'flex', gap: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
                    <li><Link to="/">Home</Link></li>
                    { !isLoggedIn ?
                    <>
                    <li><Link to="/login">Login</Link></li>
                    <li><Link to="/register">Register</Link></li>
                    </>
                    : 
                    <>
                    <li><Link to="/profile">Profile</Link></li>
                    <button onClick={onLogout}>Logout</button>
                    </>
                    }   
                </ul>
            </nav>
        </div>
        <div>
            <Outlet />
        </div>
        </>
    )
}