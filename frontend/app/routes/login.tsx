import { useNavigate } from "react-router";
import { useDispatch } from "react-redux";
import { login } from "~/slice/authSlice";

export default function Login() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const onsubmit = (e: any) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: formData.get('username'), password: formData.get('password') }),
        }).then(res => {
            return res.json();
        }).then(data => {
            if(data.success) {
                alert('Login successful');
                dispatch(login());
                navigate('/');
                
            } else {
                alert(data.msg)
            }
        })
    }


    return <form onSubmit={(e: any) => onsubmit(e)}>
        <h1>Login Form</h1>
        <label htmlFor="username">Username:</label>
        <input id="username" type="text" name="username" placeholder="Username" />
        <label htmlFor="password">Password:</label>
        <input id="password" type="password" name="password" placeholder="Password" />
        <button type="submit" style={{backgroundColor: "gray", padding: '3px'}}>Login</button>
    </form>
}