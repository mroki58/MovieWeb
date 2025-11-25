import { Link } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "./slice/authSlice";

export default function Layout() {
    const { isLoggedIn } = useSelector((state: any) => state.auth);
    const dispatch = useDispatch();

    const onLogout = () => {
        dispatch(logout());
    }
    return (
        <div>
            <nav>
                <ul>
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
    )
}