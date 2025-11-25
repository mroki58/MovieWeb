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
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          Login:
          <input type="text" name="login" required />
        </label>
      </div>

      <div>
        <label>
          Hasło:
          <input type="password" name="password" required />
        </label>
      </div>

      <div>
        <label>
          Email:
          <input type="email" name="email" required />
        </label>
      </div>

      <div>
        <p>Zainteresowania:</p>
        {
            interestsOptions.map((interest) => <label key={interest}>
              <input type="checkbox" name="interests" value={interest} /> {interest.toLowerCase()}
            </label>)
        }
      </div>

      <button type="submit">Zarejestruj</button>
    </form>
  );
}