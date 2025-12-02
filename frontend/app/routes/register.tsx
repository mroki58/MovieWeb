import { useNavigate } from 'react-router';

export default function RegisterForm() {
    const navigate = useNavigate();

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    // Tworzymy własny obiekt JSON
    const data = {
      username: formData.get('login'),
      password: formData.get('password'),
      email: formData.get('email'),
      interests: formData.getAll('interests'),
    };

    let result;

    try {
      const res = await fetch('/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      result = await res.json();

    } catch (err) {
      alert(`Błąd sieci: ${(err as Error).message}`);
      return;
    }

    if(result.success) {
        alert('Rejestracja zakończona sukcesem!');
        navigate('/login');
    }else {
        alert(`Błąd rejestracji`);
    }
  };

  const interestsOptions = [
    "COMEDY",
    "DRAMA",
    "HORROR",
    "SCIFI",
    "THRILLER", 
    "ACTION"
  ]

  return (
    <div className="min-h-screen flex pb-20 items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="w-full max-w-lg bg-white p-6 rounded-lg shadow-md space-y-4">
        <h2 className="text-2xl font-semibold text-center">Rejestracja</h2>

        <div>
          <label className="block text-sm font-medium text-gray-700">Login</label>
          <input type="text" name="login" required className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Hasło</label>
          <input type="password" name="password" required className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" name="email" required className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <p className="text-sm font-medium text-gray-700">Zainteresowania</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {interestsOptions.map((interest) => (
              <label key={interest} className="inline-flex items-center gap-2 px-2 py-1 border rounded">
                <input type="checkbox" name="interests" value={interest} className="w-4 h-4" />
                <span className="text-sm text-gray-700">{interest.toLowerCase()}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="pt-2">
          <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700">Zarejestruj</button>
        </div>
      </form>
    </div>
  );
}