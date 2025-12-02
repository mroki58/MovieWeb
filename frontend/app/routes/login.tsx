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


    return (
        <div className="min-h-screen flex pb-40 items-center justify-center bg-gray-50">
            <form onSubmit={(e: any) => onsubmit(e)} className="w-full max-w-md bg-white p-6 rounded-lg shadow-md space-y-4">
                <h1 className="text-2xl font-semibold text-center">Login</h1>

                <div>
                    <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
                    <input id="username" name="username" type="text" required placeholder="Username" className="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                    <input id="password" name="password" type="password" required placeholder="Password" className="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>

                <div className="flex items-center justify-between">
                    <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">Login</button>
                </div>
            </form>
        </div>
    );
}