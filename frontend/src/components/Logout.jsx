import { Link } from 'react-router-dom';
import { network } from '..';

const Logout = ({ link = "/home", label = "Logout" }) => {

  const handleLogout = async () => {
  const jwtToken = localStorage.getItem('jwtToken');
  if (!jwtToken) {
    return null
  } else {
    localStorage.removeItem('jwtToken');
    try {
        const response = await fetch(network + "/logout", {
          method: 'POST',
          headers: {
            'jwtToken': jwtToken
          }
        });
        if (response.ok) {
          console.log("User logged out successfully.");
        } else {
            console.error("Failed to log out:", response.statusText);
        }
      } catch (error) {
          console.error("Error logging out:", error);
      }
    }
  }

  return (
    <Link to={link} onClick={handleLogout}>
      {label}
    </Link>
  );
};

export default Logout;
