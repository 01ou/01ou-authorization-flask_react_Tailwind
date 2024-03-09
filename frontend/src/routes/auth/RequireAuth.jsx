import { Outlet, redirect } from "react-router-dom";
import { network } from "../..";
import { Header } from '../../components/_index';

export async function loader() {
  const homeEndpoint = '/home';
  const jwtToken = localStorage.getItem('jwtToken');
  
  // サーバーにログイン状態を確認
  try {
    const res = await fetch(network + '/check_logging', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${jwtToken}` // AuthorizationヘッダーにBearerスキームでJWTを含める
      }
    });
    if (res.ok) {
      const data = await res.json();
      console.log(`"${data?.user}" logged in.`);
      return (data);
    } else {
      throw new Error('Failed to check login status.');
    }
  } catch (error) {
    console.log(error);
    return redirect(homeEndpoint);
  }
}


const RequireAuth = () => {
    return (
      <>
        <Header />
        <Outlet />
      </>
    )
}

export default RequireAuth;