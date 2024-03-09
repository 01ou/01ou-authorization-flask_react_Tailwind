import { useState, useEffect } from "react";
import { network } from "..";

const UserName = ({ prefix = "", suffix = "", loading="" }) => {
  const [userInfo, setUserInfo] = useState(null);

  useEffect(() => {
    const jwtToken = localStorage.getItem('jwtToken');
    const fetchUserInfo = async () => {
      try {
        const response = await fetch(network + "/get_user_info", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${jwtToken}`, // AuthorizationヘッダーにBearerスキームでJWTを含める
          },
        });
        if (response.ok) {
          try {
            const data = await response.json();
            const user = data?.user;
            setUserInfo(user);
          } catch (error) {
            console.error("Error parsing response JSON:", error);
          }
        } else {
          console.error("Failed to fetch user info:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching user info:", error);
      }
    };

    fetchUserInfo();
  }, []);

  return (
    <div>
      {userInfo ? (
        <p>{prefix}{userInfo.username}{suffix}</p>
      ) : (
        <p>{loading}</p>
      )}
    </div>
  );
};

export default UserName;
